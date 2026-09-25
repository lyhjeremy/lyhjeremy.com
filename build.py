#!/usr/bin/env python3
"""Render index.html from projects.json. Run after editing the JSON."""
import json, html, pathlib

ROOT = pathlib.Path(__file__).parent
data = json.loads((ROOT / "projects.json").read_text())
ed = data["editorial"]
GH = "https://github.com/lyhjeremy/"
PAGES = "https://lyhjeremy.github.io/"  # project sites stay on github.io
SITE = "https://lyhjeremy.com/"  # where this page is served; revert.sh flips it back
REPO = "lyhjeremy.com"  # the repo holding this page
e = html.escape
CARD, MED = "assets/shots/card/", "assets/shots/med/"
NAMES = {slug: name for sec in data["sections"] for slug, name, _ in sec["projects"]}

TONES = {"leeway": "blue", "world-record-half-lives": "green", "marathon-heat-tax": "orange",
         "cantonese-learner-v2": "pink", "cellar-scanner": "pink", "menu-decoder": "orange",
         "receipt-auditor": "green", "race-day-copilot": "blue",
         "marathon-pacing-decay": "purple", "love-island-lexical-analysis": "teal"}
GROUP_TONES = {"featured": "blue", "applied-ai": "orange", "genai": "purple", "running": "green",
               "language": "pink", "consumer": "teal", "tools": "blue"}
STAT_TONES = ["blue", "green", "orange", "purple", "pink"]

def links(slug, code=False, short=False):
    a, b = ("Site", "Writeup") if short else ("Open the site", "Read the writeup")
    out = [f'<a class="chev" href="{PAGES}{slug}/">{a}</a>', f'<a class="chev" href="{PAGES}{slug}/overview/">{b}</a>']
    if code:
        out.append(f'<a class="chev" href="{GH}{slug}">Code</a>')
    return "".join(out)

def card(slug, eyebrow, headline, text="", *, tone="", big=False, stat=None, img=MED, cls="", code=False):
    c = " ".join(x for x in ["card", tone, "big" if big else "", cls] if x)
    st = f'<div class="stat">{e(stat)}</div>' if stat else ""
    p = f'<p>{e(text)}</p>' if text else ""
    return (f'<article class="{c}"><a class="pic" href="{PAGES}{slug}/">'
            f'<img class="shot" src="{img}{slug}.jpg" alt="{e(headline)}" loading="lazy" width="720" height="450"></a>'
            f'<div class="body"><p class="eyebrow">{e(eyebrow)}</p>{st}'
            f'<h3><a href="{GH}{slug}">{e(headline)}</a></h3>{p}'
            f'<div class="links">{links(slug, code, short=cls=="mini")}</div></div></article>')

L = ed["lead"]
lead_card = card(L["slug"], "SkillCompass", L["headline"], L["deck"], tone="dark", big=True, cls="wide", code=True)
briefs = "".join(card(b["slug"], b["kicker"].split("/")[-1].strip().capitalize(), b["headline"], b["text"],
                      tone=TONES[b["slug"]], img=CARD) for b in ed["briefs"])
S = ed["series"]
series = "".join(card(r["slug"], r["name"], r["short"], r["note"][0].upper() + r["note"][1:] + ".",
                      tone=TONES[r["slug"]], stat=r["stat"], img=CARD) for r in S["rows"])
ST = ed["stories"]; m = ST["main"]
stories = (card(m["slug"], NAMES[m["slug"]], m["headline"], m["text"], tone="dark-purple", img=CARD)
           + "".join(card(x["slug"], NAMES[x["slug"]], x["headline"], x["text"], tone=TONES[x["slug"]], img=CARD) for x in ST["side"]))
stats = "".join(
    f'<a class="{STAT_TONES[i % 5]}" href="{PAGES}{t["slug"]}/"><span class="v">{e(t["stat"])}</span>'
    f'<span class="l">{e(t["label"])}</span></a>' for i, t in enumerate(ed["numbers"]["tiles"]))

groups = "".join(
    f'<div class="group-head {GROUP_TONES.get(s["id"], "")}"><h3>{e(s["title"])}</h3><span>{len(s["projects"])}</span></div>'
    f'<div class="grid cols-4">'
    + "".join(card(slug, "", name, tone=GROUP_TONES.get(s["id"], ""), img=CARD, cls="mini") for slug, name, _ in s["projects"])
    + '</div>' for s in data["sections"])
chips = "".join(
    f'<a class="chip {GROUP_TONES.get(s["id"], "")}" href="#g-{s["id"]}">{e(s["title"])} · {len(s["projects"])}</a>'
    for s in data["sections"])
# anchor ids on group heads
for s in data["sections"]:
    groups = groups.replace(f'<div class="group-head {GROUP_TONES.get(s["id"], "")}"><h3>{e(s["title"])}</h3>',
                            f'<div class="group-head {GROUP_TONES.get(s["id"], "")}" id="g-{s["id"]}"><h3>{e(s["title"])}</h3>', 1)
mosaic = "".join(f'<img src="{CARD}{s}.jpg" alt="" loading="lazy">' for s in
                 ["marathon-heat-tax", "wine-score-inflation", "podcastify", "world-record-half-lives", "love-island-lexical-analysis", "epub-to-audiobook"])
n = sum(len(s["projects"]) for s in data["sections"])

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Jeremy Lee</title>
<meta name="description" content="Data scientist and UCLA Anderson MSBA. {n} live projects across generative AI, statistical modeling and machine learning.">
<link rel="canonical" href="{SITE}">
<meta property="og:url" content="{SITE}">
<link rel="stylesheet" href="assets/site.css">
<script>
try{{var t=localStorage.getItem("theme");if(t==="light"||t==="dark")document.documentElement.setAttribute("data-theme",t);}}catch(err){{}}
</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<nav class="nav" aria-label="Page">
  <div class="wrap">
    <a class="brand" href="{PAGES}">Jeremy Lee</a>
    <a href="#featured">Featured</a>
    <a href="#series">Fine-tuning</a>
    <a href="#stories">Data stories</a>
    <a href="#index">All projects</a>
    <a href="https://github.com/lyhjeremy">GitHub</a>
    <button type="button" id="theme-toggle" hidden aria-pressed="false">Dark</button>
  </div>
</nav>

<main id="main">
<header class="hero wrap">
  <div>
    <h1>Jeremy Lee</h1>
    <p class="sub">Data scientist, UCLA Anderson MSBA. Models, decision tools and data stories: <b>{n} projects, all live.</b></p>
    <div class="cta"><a class="chev" href="#featured">See the work</a><a class="chev" href="https://github.com/lyhjeremy">github.com/lyhjeremy</a><a class="chev" href="#colophon">About</a></div>
    <div class="chips">{chips}</div>
  </div>
  <div class="mosaic" aria-hidden="true">{mosaic}</div>
</header>

<section class="section wrap" id="featured">
  <div class="section-head"><p class="section-eyebrow blue">Selected work</p><h2>Featured</h2><p>A product, a decision tool, two data stories, a language app.</p></div>
  {lead_card}
  <div class="grid cols-4" style="margin-top:14px">{briefs}</div>
</section>

<div class="band"><section class="section wrap" id="series">
  <div class="section-head"><p class="section-eyebrow orange">Applied AI</p><h2>The fine-tuning series</h2><p>Four photo-to-data apps, each with a locally fine-tuned LoRA benchmarked against Claude zero-shot.</p></div>
  <div class="grid cols-4">{series}</div>
</section></div>

<section class="section wrap" id="stories">
  <div class="section-head"><p class="section-eyebrow purple">Analysis</p><h2>Data stories</h2><p>Findings from the analysis projects, with the chart that carries each.</p></div>
  <div class="grid cols-3">{stories}</div>
  <div class="grid cols-5 stats" style="margin-top:14px">{stats}</div>
</section>

<div class="band"><section class="section wrap" id="index">
  <div class="section-head"><p class="section-eyebrow green">The index</p><h2>All {n} projects</h2><p>Grouped the way I file them. The name opens the code.</p></div>
  {groups}
</section></div>
</main>

<footer class="footer" id="colophon">
  <div class="wrap">
    <div class="cols">
      <div><h4>Modeling</h4><ul><li>scikit-learn, PyTorch, XGBoost</li><li>Regression, classification, clustering</li><li>Time series, neural networks</li><li>Causal inference, survival analysis</li><li>A/B testing</li></ul></div>
      <div><h4>Optimization</h4><ul><li>Gurobi</li><li>LP / IP / QP, non-convex</li><li>Branch-and-bound, LP duality</li><li>Gradient descent</li><li>Simulation, Monte Carlo</li></ul></div>
      <div><h4>GenAI and agents</h4><ul><li>LLM prompting, RAG, embeddings</li><li>Vector databases, fine-tuning</li><li>OpenAI and Anthropic APIs</li><li>LangChain, LangGraph</li><li>Tool use, retrieval pipelines</li></ul></div>
      <div><h4>Data and deployment</h4><ul><li>Python, R, SQL</li><li>Snowflake, Airflow, Spark</li><li>Tableau, Power BI</li><li>Git, GitHub Pages, Streamlit</li></ul></div>
    </div>
    <div class="about">
      <p>Co-founder and Chief Strategy Officer at Casual Ace Learning Centre: grew enrollment 5.2x to over 1,000 students across six centers. MSBA, UCLA Anderson; BBA, University of Hong Kong. 14 marathons, Berlin personal best 2:48. WSET Level 3 in wine.</p>
      <p><a href="https://www.linkedin.com/in/jeremylyh/">LinkedIn</a> · <a href="mailto:lyhjeremy@gmail.com">Email</a> · <a href="https://github.com/lyhjeremy">GitHub</a></p>
    </div>
    <div class="legal">
      <span>Screenshots are captures of the live sites. No analytics, no third-party requests.</span>
      <span><a href="{GH}{REPO}">Source for this page</a></span>
    </div>
  </div>
</footer>

<script>
(function(){{
  var root=document.documentElement,btn=document.getElementById("theme-toggle");
  if(!btn)return;
  function current(){{return root.getAttribute("data-theme")==="dark"?"dark":"light";}}
  function render(){{var dark=current()==="dark";btn.textContent=dark?"Light":"Dark";btn.setAttribute("aria-pressed",dark?"true":"false");}}
  btn.hidden=false;render();
  btn.addEventListener("click",function(){{
    var next=current()==="dark"?"light":"dark";
    root.setAttribute("data-theme",next);
    try{{localStorage.setItem("theme",next);}}catch(err){{}}
    render();
  }});
}})();
</script>
</body>
</html>
'''
(ROOT / "index.html").write_text(page)
print(f"wrote index.html, {n} projects")
