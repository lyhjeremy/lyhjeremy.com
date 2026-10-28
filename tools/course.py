"""Turn the Berlin Marathon GPX into Fourier terms for the hero drawing.

Resamples the course to N points evenly spaced along its length, projects to a
flat plane, takes a direct DFT and keeps the largest K terms. Writes
assets/berlin.json, which build.py inlines into the page.

    python3 tools/course.py
"""
import cmath, json, math, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
N, K = 512, 160

s = (ROOT / "tools/berlin-2023.gpx").read_text()
ll = [(float(a), float(b)) for a, b in re.findall(r'lat="([-\d.]+)"\s+lon="([-\d.]+)"', s)]
lat0 = sum(a for a, _ in ll) / len(ll)
xy = [(b * 111.32 * math.cos(math.radians(lat0)), -a * 110.57) for a, b in ll]  # km, y down

seg = [0.0]
for (x0, y0), (x1, y1) in zip(xy, xy[1:]):
    seg.append(seg[-1] + math.hypot(x1 - x0, y1 - y0))
total = seg[-1]

pts, j = [], 0
for i in range(N):
    t = total * i / N
    while seg[j + 1] < t:
        j += 1
    f = (t - seg[j]) / (seg[j + 1] - seg[j])
    pts.append(complex(xy[j][0] + f * (xy[j + 1][0] - xy[j][0]), xy[j][1] + f * (xy[j + 1][1] - xy[j][1])))

c = complex((max(p.real for p in pts) + min(p.real for p in pts)) / 2,
            (max(p.imag for p in pts) + min(p.imag for p in pts)) / 2)  # bbox center, so the drawing fills the frame
pts = [p - c for p in pts]
scale = 1 / max(max(abs(p.real), abs(p.imag)) for p in pts)
pts = [p * scale for p in pts]

terms = []
for k in range(-N // 2, N // 2):
    z = sum(p * cmath.exp(-2j * math.pi * k * n / N) for n, p in enumerate(pts)) / N
    terms.append((k, z))
terms.sort(key=lambda t: -abs(t[1]))
terms = [[k, round(abs(z), 5), round(cmath.phase(z), 4)] for k, z in terms[:K]]

path = "M" + " L".join(f"{p.real:.4f},{p.imag:.4f}" for p in pts) + "Z"
out = {"km": round(total, 2), "terms": terms, "path": path,
       "start": [round(pts[0].real, 4), round(pts[0].imag, 4)]}
(ROOT / "assets/berlin.json").write_text(json.dumps(out, separators=(",", ":")))
print(f"course {total:.2f} km, {len(ll)} GPX points, kept {len(terms)} of {N} terms")
