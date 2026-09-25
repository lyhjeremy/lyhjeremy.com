# lyhjeremy.com

Portfolio landing page at [lyhjeremy.com](https://lyhjeremy.com/). Plain HTML and CSS, one Python build script, self-contained: no framework, no third-party requests, no analytics. The profile README at [lyhjeremy/lyhjeremy](https://github.com/lyhjeremy/lyhjeremy) links here.

## Domain setup

Only this page lives on the custom domain. Every project card links to its own site at `lyhjeremy.github.io/<slug>/`, and those sites, their backends and their repos are unchanged. The domain is attached to this repo alone (the `CNAME` file), which is why it does not pull the project sites along with it. A custom domain on the `lyhjeremy.github.io` repo would have moved all of them.

- DNS at Spaceship: four A records for `@` (185.199.108.153 to 185.199.111.153), a CNAME `www` to `lyhjeremy.github.io`, and the `_github-pages-challenge-lyhjeremy` TXT record that keeps the domain verified to this GitHub account.
- `lyhjeremy.github.io/` holds a one-file redirect to here. Its history up to the move is intact, and this repo was created from that history on 2026-09-24.
- `SITE` and `REPO` at the top of `build.py` set the canonical URL and the footer's source link.

To go back to `lyhjeremy.github.io` (for example, before letting the domain lapse), follow [REVERT.md](REVERT.md). Do it before the domain expires, not after.

## How the page is built

`index.html` is generated. Do not edit it by hand.

- `projects.json` is the content source. `sections` lists all 30 projects (slug, display name, one-line summary) in seven groups. `editorial` holds the curated front: the lead project, the four featured briefs, the fine-tuning series rows (each with `stat`, `short` headline and `note`), the three data stories and the five numbers tiles. All links derive from the slug: code at `github.com/lyhjeremy/<slug>`, site at `lyhjeremy.github.io/<slug>/`, writeup at `.../<slug>/overview/`.
- `build.py` renders `index.html` from the JSON. The category color maps live at the top (`TONES`, `STAT_TONES`, `GROUP_TONES`); the footer (skills, about, contact) is inline in the template. Run `python3 build.py` after any edit and commit both files.
- `assets/site.css` is all of the styling. `tools/thumbs.py` makes card images (below).

Page structure, top to bottom: sticky nav; hero (name, one-liner, category chips, a 2x3 mosaic of thumbnails); Featured (one wide SkillCompass card plus four cards); The fine-tuning series (four stat cards on a gray band); Data stories (three chart cards plus five stat tiles); All 30 projects (mini cards grouped by category, on a gray band); footer.

## Images

Three asset tiers under `assets/shots/`:

- `card/<slug>.jpg`, 720x450: the thumbnail used everywhere. Each is the most interesting figure from that project's writeup (a chart, an app screen or a pipeline diagram), padded to 16:10 on a corner-sampled background, never cropped, so no axis or label is lost. Two projects have no writeup figures (`epub-to-audiobook`, `podcastify`) and use a crop of their live page instead.
- `med/<slug>.jpg`, 1280x800: same treatment for the two wide cards (`skill-compass`, `wine-score-inflation`).
- `<slug>.png`, 1600px wide: full captures of each live site's top, kept as raw material.

To refresh one project's thumbnail: pick a figure from `https://lyhjeremy.github.io/<slug>/overview/`, then

    python3 tools/thumbs.py <slug> <figure-url> [--wide]

To recapture a live page (Leeway's map does not render headless; use its writeup images instead):

    chrome --headless=new --window-size=1100,800 --force-device-scale-factor=2 \
        --screenshot=assets/shots/<slug>.png https://lyhjeremy.github.io/<slug>/
    sips -Z 1600 assets/shots/<slug>.png

## Styling and theme

Apple.com idiom: system sans (SF on Apple devices, Helvetica/Arial elsewhere), white page with `#f5f5f7` bands, rounded cards, chevron links, compact type. Every screenshot sits in a white 10px mat with a hairline border, which is what keeps 30 visually different thumbnails looking like one set. Card bodies carry one of six tints (blue, green, orange, purple, pink, teal) mapped to project categories; each section opens with a colored kicker; the two anchor cards use a dark gradient body.

Light is the default for every visitor. Dark is opt-in via the nav toggle, stored in `localStorage` and applied before first paint; dark uses `#1c1c1e` bordered cards on black with brightened accents, and the white image mats stay white by design. All colors are custom properties on `:root` and `:root[data-theme="dark"]` in `assets/site.css`. Layout holds at 390px; hover motion is disabled under `prefers-reduced-motion`.

This repo is a recorded exception to [DESIGN_STANDARDS.md](https://github.com/lyhjeremy/lyhjeremy/blob/main/DESIGN_STANDARDS.md) (see its Exceptions section): do not run `designcheck.py` here. Commits carry no AI attribution trailers.

## Adding a project

1. Add the row to the right group in `projects.json` (plus an `editorial` entry if it should be featured).
2. Make its thumbnail with `tools/thumbs.py` (figure from the writeup, not the page top).
3. `python3 build.py`, open `index.html` locally in light and dark, commit `projects.json`, `index.html` and the new image.

## History

Built 2026-08-23/24, four iterations in one sitting: a dark Ledger-style mirror of the profile README; an editorial "data journal" front page; an apple.com-style restyle (dark, then light); and the current compact image-first card grid with writeup-figure thumbnails and white mats. The git log carries the sequence.
