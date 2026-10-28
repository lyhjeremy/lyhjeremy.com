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

- `projects.json` is the content source. `families` maps every project to one of the five Ledger families (road, track, cellar, language, workshop) used by the project sites; `build.py` refuses to build if a project has none. `groups` lists all 33 projects (slug, display name, one-line summary) in six groups for the index. `selected`, `series`, `stories` and `numbers` hold the curated sections. `site_overrides` maps a slug to a site URL for projects not on GitHub Pages (Fourier Pen is on Vercel); `no_writeup` lists projects without an `/overview/` page.
- `assets/berlin.json` holds the hero drawing: the Berlin Marathon course from `tools/berlin-2023.gpx` (a public GPX of the 2023 race), resampled to 512 points and reduced to its 160 largest Fourier terms by `tools/course.py`. The page draws the course with those terms as a chain of rotating circles, the method behind Fourier Pen. Under `prefers-reduced-motion` it draws the finished line with no animation.
- `build.py` renders `index.html` from both files. The About section and the footer are inline in the template. Run `python3 build.py` after any edit and commit both files.
- `assets/site.css` is all of the styling. `tools/thumbs.py` makes card images (below).

Page structure, top to bottom: sticky top bar; hero (name, positioning line, contact buttons, the course drawing); a strip of five facts; Selected work (five numbered rows, text beside a figure); the fine-tuning series as a table with footnoted caveats; Data stories (one large figure and two small, then five numbers); the index of all 33 projects, each tagged with its family; About; footer.

## Images

Three asset tiers under `assets/shots/`:

- `card/<slug>.jpg`, 720x450: each project's most interesting figure from its writeup (a chart, an app screen or a pipeline diagram), padded to 16:10 on a corner-sampled background, never cropped. Two projects have no writeup figures (`epub-to-audiobook`, `podcastify`) and use a crop of their live page.
- `med/<slug>.jpg`: larger versions. Selected work uses these for the three app screens (SkillCompass, Leeway, Cantonese Learner) and the `card` figure for the analysis projects.
- `<slug>.png`, 1600px wide: full captures of each live site's top, kept as raw material.

To refresh one project's thumbnail: pick a figure from `https://lyhjeremy.github.io/<slug>/overview/`, then

    python3 tools/thumbs.py <slug> <figure-url> [--wide]

## Styling and theme

Since 2026-10-27 the page uses the Ledger base identity from [DESIGN_STANDARDS.md](https://github.com/lyhjeremy/lyhjeremy/blob/main/DESIGN_STANDARDS.md) (paper ground, Source Serif 4, IBM Plex Sans and Mono, oxide and pine, square corners, no shadows), so it now passes `designcheck.py` like every project site. Each project's family shows up as a small tag in that family's accent and display face, which previews the look of the site the link opens. All ten font files are self-hosted in `assets/fonts/`.

The theme follows the visitor's system setting; the toggle in the top bar overrides it and is stored in `localStorage`, applied before first paint. Colors are custom properties on bare `:root`, redefined for dark under `prefers-color-scheme` and `[data-theme="dark"]`. Layout holds at 320px and up; below 600px the top bar drops Fine-tuning and Stories.

## Adding a project

1. Add the row to the right group in `projects.json` (plus an `editorial` entry if it should be featured).
2. Make its thumbnail with `tools/thumbs.py` (figure from the writeup, not the page top).
3. Give it a family in `families`.
4. `python3 build.py`, open `index.html` locally in light and dark, commit `projects.json`, `index.html` and the new image.

## History

Built 2026-08-23/24, four iterations in one sitting: a dark Ledger-style mirror of the profile README; an editorial "data journal" front page; an apple.com-style restyle; and a compact image-first card grid. On 2026-10-27 it was rebuilt in the Ledger style with the Berlin course drawing, a benchmark table and a one-line-per-project index. The git log carries the sequence.
