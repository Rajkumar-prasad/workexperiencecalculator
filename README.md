# workexperiencecalculator.online - static site

Plain HTML + CSS + JS. No build step.

## Deploy (GitHub + Cloudflare Pages)
1. Create a new GitHub repo and upload everything in this folder (keep the folder structure).
2. Cloudflare dashboard > Workers & Pages > Create > Pages > Connect to Git > pick the repo.
3. Build settings: Framework preset = None, Build command = (empty), Output directory = `/`.
4. After the first deploy: Custom domains > add `workexperiencecalculator.online` (and `www`).
5. Google Search Console: the verification file `google663c0df5aabba0ac.html` is included. Submit `https://workexperiencecalculator.online/sitemap.xml`.
6. AdSense: `ads.txt` is included. Turn on Auto ads and the EU consent message (Privacy & messaging) in AdSense.

## Before going live
- Change the contact email in `build.py` (EMAIL) or search/replace `contact@workexperiencecalculator.online` in all HTML files.
