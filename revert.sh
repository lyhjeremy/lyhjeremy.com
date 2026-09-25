#!/usr/bin/env bash
# Move the portfolio back to lyhjeremy.github.io. See REVERT.md.
# Dry run by default; pass --apply to make changes.
set -euo pipefail

OWNER=lyhjeremy
FACADE=lyhjeremy.com
USERSITE=lyhjeremy.github.io

if [[ "${1:-}" != "--apply" ]]; then
  cat <<PLAN
Plan (nothing changed; rerun with --apply):
  1. Copy the current page from $OWNER/$FACADE into $OWNER/$USERSITE, remove CNAME,
     set SITE/REPO in build.py back to github.io, rebuild, commit, push.
  2. Disable GitHub Pages on $OWNER/$FACADE and archive the repo.
  3. Point the portfolio link in $OWNER/$OWNER README.md back at https://$USERSITE/.
  4. Check https://$USERSITE/ serves the full page.
Then by hand: remove the verified domain at github.com/settings/pages,
and turn off auto-renew at Spaceship.
PLAN
  exit 0
fi

for cmd in git gh python3 curl; do command -v "$cmd" >/dev/null || { echo "missing: $cmd"; exit 1; }; done
work=$(mktemp -d)
echo "working in $work"

# 1. Restore the full page on the user site.
git clone -q "https://github.com/$OWNER/$USERSITE.git" "$work/site"
cd "$work/site"
git config user.name "Jeremy Lee"; git config user.email "lyhjeremy@gmail.com"
git fetch -q "https://github.com/$OWNER/$FACADE.git" main
git rm -rq .
git checkout FETCH_HEAD -- .
git rm -qf CNAME
perl -pi -e 's#^SITE = "https://lyhjeremy\.com/"#SITE = "https://lyhjeremy.github.io/"#; s#^REPO = "lyhjeremy\.com"#REPO = "lyhjeremy.github.io"#' build.py
grep -q '^SITE = "https://lyhjeremy.github.io/"' build.py || { echo "SITE line not updated; stopping before any push"; exit 1; }
grep -q '^REPO = "lyhjeremy.github.io"' build.py || { echo "REPO line not updated; stopping before any push"; exit 1; }
python3 build.py
git add -A
git commit -qm "Move the portfolio back to lyhjeremy.github.io"
git push -q origin main
echo "1/4 user site restored"

# 2. Retire the domain repo.
gh api -X DELETE "repos/$OWNER/$FACADE/pages" >/dev/null && echo "2/4 Pages disabled on $FACADE"
gh repo archive "$OWNER/$FACADE" --yes && echo "    $FACADE archived"

# 3. Profile README link.
git clone -q "https://github.com/$OWNER/$OWNER.git" "$work/profile"
cd "$work/profile"
git config user.name "Jeremy Lee"; git config user.email "lyhjeremy@gmail.com"
perl -pi -e 's#\[lyhjeremy\.com\]\(https://lyhjeremy\.com/\)#[lyhjeremy.github.io](https://lyhjeremy.github.io/)#' README.md
if git diff --quiet; then echo "3/4 profile README had no lyhjeremy.com link; left as is"
else git commit -qam "Portfolio link back to lyhjeremy.github.io" && git push -q origin main && echo "3/4 profile README updated"; fi
gh repo edit "$OWNER/$USERSITE" --homepage "https://$USERSITE/" --description "Portfolio landing page for $USERSITE" >/dev/null

# 4. Check. Pages can take a few minutes to serve the new build.
for i in $(seq 1 30); do
  body=$(curl -sS "https://$USERSITE/?check=$RANDOM" || true)
  if grep -q 'class="legal"' <<<"$body" && ! grep -qi 'http-equiv="refresh"' <<<"$body"; then
    echo "4/4 https://$USERSITE/ serves the full page"; break; fi
  [[ $i == 30 ]] && echo "4/4 not confirmed after 5 min; check https://$USERSITE/ by hand"
  sleep 10
done

echo "Left to do by hand: remove lyhjeremy.com at github.com/settings/pages, and turn off auto-renew at Spaceship."
