#!/usr/bin/env python3
"""Render index.html from projects.json and assets/berlin.json. Run after editing either."""
import json, html, pathlib

ROOT = pathlib.Path(__file__).parent
data = json.loads((ROOT / "projects.json").read_text())
course = json.loads((ROOT / "assets/berlin.json").read_text())
GH = "https://github.com/lyhjeremy/"
PAGES = "https://lyhjeremy.github.io/"  # project sites stay on github.io
SITE = "https://lyhjeremy.com/"  # where this page is served; revert.sh flips it back
REPO = "lyhjeremy.com"  # the repo holding this page
e = html.escape
CARD, MED = "assets/shots/card/", "assets/shots/med/"
NAMES = {slug: name for g in data["groups"] for slug, name, _ in g["projects"]}
FAMILY = {slug: fam for fam, slugs in data["families"].items() for slug in slugs}
# Projects hosted somewhere other than lyhjeremy.github.io/<slug>/ (e.g. Vercel). The writeup
# lives at <site>/overview/ in every case.
SITE_OVERRIDES = data.get("site_overrides", {})
NO_WRITEUP = set(data.get("no_writeup", []))
missing = [s for s in NAMES if s not in FAMILY]
assert not missing, f"no family for {missing}"

def site(slug):
    return SITE_OVERRIDES.get(slug, f"{PAGES}{slug}/")

def links(slug, code=True):
    out = [f'<a href="{site(slug)}">Site</a>']
    if slug not in NO_WRITEUP:
        out.append(f'<a href="{site(slug)}overview/">Write-up</a>')
    if code:
        out.append(f'<a href="{GH}{slug}">Code</a>')
    return '<span class="links">' + "".join(out) + "</span>"

def tag(slug):
    f = FAMILY[slug]
    return f'<span class="fam fam-{f}">{f}</span>'

# App screens read best at the larger size; analysis projects use their headline figure.
img = lambda slug: f"{MED}{slug}.jpg" if slug in ("skill-compass", "leeway", "cantonese-learner-v2") else f"{CARD}{slug}.jpg"
selected = "".join(
    f'<article class="sel" id="w-{s["slug"]}">'
    f'<div class="sel-text"><p class="sel-no">{i:02d}</p>'
    f'<p class="kicker">{e(s["label"])} {tag(s["slug"])}</p>'
    f'<h3><a href="{site(s["slug"])}">{e(s["headline"])}</a></h3>'
    f'<p class="name">{e(NAMES[s["slug"]])}</p><p>{e(s["text"])}</p>{links(s["slug"])}</div>'
    f'<figure><a href="{site(s["slug"])}" tabindex="-1"><img src="{img(s["slug"])}" alt="{e(s["figcap"])}" '
    f'loading="lazy" width="1280" height="800"></a><figcaption>{e(s["figcap"])}</figcaption></figure></article>'
    for i, s in enumerate(data["selected"], 1))

S = data["series"]
sup = lambda m: f"<sup>{m}</sup>" if m else ""
series_rows = "".join(
    f'<tr><th scope="row"><a href="{site(r["slug"])}">{e(r["name"])}</a></th><td>{e(r["task"])}</td>'
    f'<td class="num strong">{e(r["ft"])}</td>'
    f'<td class="num">{e(r["claude"])}{sup(r["mark"])}</td>'
    f'<td>{links(r["slug"], code=False)}</td></tr>' for r in S["rows"])
series_notes = "".join(f'<li><sup>{k}</sup> {e(v)}</li>' for k, v in S["notes"].items())

stories = "".join(
    f'<article class="story{" lead" if i == 0 else ""}"><figure><a href="{site(s["slug"])}overview/" tabindex="-1">'
    f'<img src="{CARD}{s["slug"]}.jpg" alt="{e(s["figcap"])}" loading="lazy" width="720" height="450"></a>'
    f'<figcaption>{e(s["figcap"])}</figcaption></figure>'
    f'<p class="kicker">{e(NAMES[s["slug"]])} {tag(s["slug"])}</p>'
    f'<h3><a href="{site(s["slug"])}overview/">{e(s["headline"])}</a></h3><p>{e(s["text"])}</p></article>'
    for i, s in enumerate(data["stories"]))

numbers = "".join(
    f'<li><a href="{site(t["slug"])}"><span class="v">{e(t["stat"])}</span>'
    f'<span class="l">{e(t["label"])}</span></a></li>' for t in data["numbers"])

index = "".join(
    f'<section class="group" id="g-{g["id"]}"><h3>{e(g["title"])} <span>{len(g["projects"])}</span></h3><ol>'
    + "".join(f'<li>{tag(slug)}<a class="pname" href="{site(slug)}">{e(name)}</a>'
              f'<span class="sum">{e(summary)}</span>{links(slug)}</li>' for slug, name, summary in g["projects"])
    + "</ol></section>" for g in data["groups"])
legend = "".join(f'<li>{tag(slugs[0])} {len(slugs)}</li>' for fam, slugs in data["families"].items())

n = len(NAMES)
nw = sum(1 for s in NAMES if s not in NO_WRITEUP)
# Frame the drawing on the course's own bounding box plus a margin, so it fills the figure.
import re
_xy = [tuple(map(float, m)) for m in re.findall(r"(-?[\d.]+),(-?[\d.]+)", course["path"])]
PAD = 0.08
VB = [min(x for x, _ in _xy) - PAD, min(y for _, y in _xy) - PAD]
VB += [max(x for x, _ in _xy) + PAD - VB[0], max(y for _, y in _xy) + PAD - VB[1]]
VB = [round(v, 4) for v in VB]
course_json = json.dumps({"terms": course["terms"], "vb": VB}, separators=(",", ":"))

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Jeremy Lee: data science and applied AI</title>
<meta name="description" content="Jeremy Lee, data scientist. UCLA Anderson MSBA. {n} projects with live sites: RAG, agents, LoRA fine-tunes, survival analysis, Monte Carlo, and a lot of marathon data.">
<link rel="canonical" href="{SITE}">
<meta property="og:url" content="{SITE}">
<meta property="og:title" content="Jeremy Lee: data science and applied AI">
<link rel="preload" href="assets/fonts/SourceSerif4-600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/site.css">
<script>
try{{var t=localStorage.getItem("theme");if(t==="light"||t==="dark")document.documentElement.setAttribute("data-theme",t);}}catch(err){{}}
</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap">
    <a class="brand" href="{SITE}">Jeremy Lee</a>
    <nav aria-label="Page">
      <a href="#work">Work</a>
      <a class="opt" href="#series">Fine-tuning</a>
      <a class="opt" href="#stories">Stories</a>
      <a href="#index">Index</a>
      <a href="#about">About</a>
      <button type="button" id="theme-toggle" hidden aria-pressed="false">Dark</button>
    </nav>
  </div>
</header>

<main id="main">
<section class="hero wrap">
  <div class="hero-text">
    <p class="eyebrow">Data science and applied AI</p>
    <h1>Jeremy Lee</h1>
    <p class="lede">I build models, the tests that show whether they work, and the apps people open to use them. There are {n} projects here, each with a live site, and {nw} with a write-up on what it found and where it falls short.</p>
    <p class="sub">MSBA at UCLA Anderson. Before that I co-founded an education company and grew it 5.2 times over, to more than 1,000 students across six centers.</p>
    <p class="contact"><a class="btn primary" href="mailto:lyhjeremy@gmail.com">Email me</a><a class="btn" href="https://www.linkedin.com/in/jeremylyh/">LinkedIn</a><a class="btn" href="https://github.com/lyhjeremy">GitHub</a></p>
  </div>
  <figure class="course">
    <div class="course-box" style="aspect-ratio:{VB[2]:.3f}/{VB[3]:.3f}">
      <svg viewBox="{" ".join(map(str, VB))}" role="img" aria-labelledby="course-cap">
        <path class="ghost" d="{course["path"]}"/>
        <rect class="startmark" x="{course["start"][0] - 0.03:.4f}" y="{course["start"][1] - 0.03:.4f}" width="0.06" height="0.06"/>
      </svg>
      <canvas id="pen" aria-hidden="true"></canvas>
    </div>
    <figcaption id="course-cap">The Berlin Marathon course, {course["km"]:.1f} km as recorded in a public GPX of the 2023 race, redrawn by {len(course["terms"])} rotating circles: a Fourier series, the method behind <a href="{site("fourier-pen")}">Fourier Pen</a>. I ran it in 2:48. <button type="button" id="redraw" hidden>Draw it again</button></figcaption>
  </figure>
</section>

<div class="wrap"><ul class="facts" aria-label="In brief">
  <li><span class="v">14</span> marathons</li>
  <li><span class="v">2:48</span> in Berlin</li>
  <li><span class="v">WSET 3</span> in wine</li>
  <li><span class="v">MSBA</span> UCLA Anderson</li>
  <li><span class="v">BBA</span> Univ. of Hong Kong</li>
</ul></div>

<section class="wrap block" id="work">
  <div class="head"><p class="eyebrow">Selected work</p><h2>Five to start with</h2></div>
  {selected}
</section>

<section class="wrap block" id="series">
  <div class="head"><p class="eyebrow">Applied AI</p><h2>The fine-tuning series</h2><p class="intro">{e(S["intro"])}</p></div>
  <div class="scroll"><table class="bench">
    <thead><tr><th scope="col">App</th><th scope="col">What the small model does</th><th scope="col" class="num">Fine-tuned</th><th scope="col" class="num">Claude zero-shot</th><th scope="col"><span class="vh">Links</span></th></tr></thead>
    <tbody>{series_rows}</tbody>
  </table></div>
  <ol class="notes">{series_notes}</ol>
</section>

<section class="wrap block" id="stories">
  <div class="head"><p class="eyebrow">Analysis</p><h2>Data stories</h2><p class="intro">Running and wine supply most of the questions.</p></div>
  <div class="stories">{stories}</div>
  <ul class="numbers">{numbers}</ul>
</section>

<section class="wrap block" id="index">
  <div class="head"><p class="eyebrow">Index</p><h2>All {n} projects</h2>
  <p class="intro">Each project site has its own look. The tag says which of five families it belongs to.</p>
  <ul class="legend">{legend}</ul></div>
  {index}
</section>

<section class="wrap block" id="about">
  <div class="head"><p class="eyebrow">About</p><h2>Background</h2></div>
  <div class="about">
    <div class="about-text">
      <p>I spent the years before data science running a business. I co-founded Casual Ace Learning Centre and, as Chief Strategy Officer, grew enrollment 5.2 times to more than 1,000 students across six centers. I came to data science through an MSBA at UCLA Anderson, after graduate analytics coursework at Georgia Tech and a BBA in Accounting and Finance from the University of Hong Kong.</p>
      <p>Outside work I have run 14 marathons, with a best of 2:48 in Berlin, and I hold WSET Level 3 in wine. Between them they account for most of the questions on this page.</p>
      <p class="contact"><a class="btn primary" href="mailto:lyhjeremy@gmail.com">lyhjeremy@gmail.com</a><a class="btn" href="https://www.linkedin.com/in/jeremylyh/">LinkedIn</a></p>
    </div>
    <dl class="skills">
      <dt>Modeling</dt><dd>scikit-learn, PyTorch, XGBoost. Regression, classification, clustering, time series, survival analysis, causal inference, A/B testing.</dd>
      <dt>GenAI and agents</dt><dd>RAG (BM25, dense, cross-encoder reranking), embeddings and vector stores, LoRA fine-tuning, LLM-as-judge evals, LangChain, LangGraph, Anthropic and OpenAI APIs.</dd>
      <dt>Optimization</dt><dd>Gurobi; LP, IP, QP and non-convex programs; branch-and-bound, duality, Monte Carlo simulation.</dd>
      <dt>Data and deployment</dt><dd>Python, R, SQL, Snowflake, Airflow, Spark, Tableau, Power BI. FastAPI and Streamlit apps on Render, Vercel and GitHub Pages.</dd>
    </dl>
  </div>
</section>
</main>

<footer class="foot">
  <div class="wrap">
    <p>Jeremy Lee. <a href="mailto:lyhjeremy@gmail.com">Email</a> · <a href="https://www.linkedin.com/in/jeremylyh/">LinkedIn</a> · <a href="https://github.com/lyhjeremy">GitHub</a></p>
    <p class="small">Images are figures from each project's write-up or captures of its live site. No analytics, no cookies and no third-party requests; the theme choice stays in your browser. <a href="{GH}{REPO}">Source for this page</a>.</p>
  </div>
</footer>

<script>
(function(){{
  var root=document.documentElement,btn=document.getElementById("theme-toggle");
  function dark(){{var t=root.getAttribute("data-theme");return t?t==="dark":matchMedia("(prefers-color-scheme: dark)").matches;}}
  function render(){{btn.textContent=dark()?"Light":"Dark";btn.setAttribute("aria-pressed",dark()?"true":"false");}}
  btn.hidden=false;render();
  btn.addEventListener("click",function(){{
    var next=dark()?"light":"dark";root.setAttribute("data-theme",next);
    try{{localStorage.setItem("theme",next);}}catch(err){{}}
    render();if(window.redrawPen)window.redrawPen(true);
  }});
}})();
(function(){{
  var root=document.documentElement,C={course_json},cv=document.getElementById("pen"),again=document.getElementById("redraw");
  if(!cv||!cv.getContext)return;
  var ctx=cv.getContext("2d"),T=C.terms,still=matchMedia("(prefers-reduced-motion: reduce)"),raf=0,trail=[],t0=0,DUR=9000,STEPS=900;
  function at(t,upto){{var x=0,y=0,pts=[[0,0]];for(var i=0;i<upto;i++){{var a=2*Math.PI*T[i][0]*t+T[i][2];x+=T[i][1]*Math.cos(a);y+=T[i][1]*Math.sin(a);pts.push([x,y]);}}return pts;}}
  function css(n){{return getComputedStyle(root).getPropertyValue(n).trim();}}
  function size(){{var r=cv.getBoundingClientRect(),d=window.devicePixelRatio||1;cv.width=r.width*d;cv.height=r.height*d;var V=C.vb,k=cv.width/V[2];ctx.setTransform(k,0,0,k,-V[0]*k,-V[1]*k);}}
  function line(pts,col,w){{ctx.strokeStyle=col;ctx.lineWidth=w;ctx.beginPath();ctx.moveTo(pts[0][0],pts[0][1]);for(var i=1;i<pts.length;i++)ctx.lineTo(pts[i][0],pts[i][1]);ctx.stroke();}}
  function frame(now){{
    var p=Math.min((now-t0)/DUR,1),n=Math.floor(p*STEPS),px=C.vb[2]/cv.width;
    while(trail.length<=n){{var q=at(trail.length/STEPS,T.length);trail.push(q[q.length-1]);}}
    ctx.clearRect(C.vb[0],C.vb[1],C.vb[2],C.vb[3]);
    if(p<1){{
      var arms=at(n/STEPS,40);ctx.strokeStyle=css("--rule");ctx.lineWidth=px;
      for(var i=1;i<arms.length;i++){{ctx.beginPath();ctx.arc(arms[i-1][0],arms[i-1][1],T[i-1][1],0,2*Math.PI);ctx.stroke();}}
      line(arms,css("--ink-2"),1.2*px);
    }}
    line(trail,css("--signal"),2.4*px);
    if(p<1)raf=requestAnimationFrame(frame);else again.hidden=false;
  }}
  function finish(){{trail=[];for(var i=0;i<=STEPS;i++){{var q=at(i/STEPS,T.length);trail.push(q[q.length-1]);}}ctx.clearRect(C.vb[0],C.vb[1],C.vb[2],C.vb[3]);line(trail,css("--signal"),2.4*C.vb[2]/cv.width);}}
  window.redrawPen=function(keep){{
    cancelAnimationFrame(raf);size();
    if(keep||still.matches){{finish();again.hidden=still.matches;return;}}
    trail=[];again.hidden=true;t0=performance.now();raf=requestAnimationFrame(frame);
  }};
  again.addEventListener("click",function(){{window.redrawPen(false);}});
  addEventListener("resize",function(){{if(!again.hidden||still.matches)window.redrawPen(true);}});
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change",function(){{window.redrawPen(true);}});
  window.redrawPen(false);
}})();
</script>
</body>
</html>
'''
(ROOT / "index.html").write_text(page)
print(f"wrote index.html, {n} projects")
