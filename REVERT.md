# Moving the portfolio back to lyhjeremy.github.io

Use this if the domain is no longer wanted. It takes about ten minutes and nothing is rebuilt from scratch.

## When

Before `lyhjeremy.com` expires. Auto-renew is on at Spaceship, so the renewal reminder email is the natural prompt. After expiry the domain can be bought by anyone, and until this is done the old `lyhjeremy.github.io` homepage still redirects visitors there.

## Steps

1. Run `./revert.sh` to see the plan, then `./revert.sh --apply` to carry it out. It needs `git`, `gh` (logged in as lyhjeremy) and `python3`. It:
   - copies the current page from this repo into `lyhjeremy/lyhjeremy.github.io`, replacing the redirect, drops the `CNAME` file, points `SITE` and `REPO` in `build.py` back at github.io, rebuilds and pushes. New projects added here since the move come along.
   - turns off GitHub Pages for this repo and archives it (read-only, history kept).
   - changes the portfolio link in the profile README back to `lyhjeremy.github.io`.
   - checks that `https://lyhjeremy.github.io/` serves the full page again.
2. By hand, GitHub: Settings, Pages, Verified domains, remove `lyhjeremy.com`.
3. By hand, Spaceship: turn off auto-renew for `lyhjeremy.com`. The DNS records can stay until it expires.
4. Update `PROJECTS_SUMMARY.md` in the local projects folder, and the LinkedIn or resume link if it uses the domain.

Project sites, their backends (Render) and the verified-domain protection are unaffected by steps 1 to 3 apart from the last item in step 2.
