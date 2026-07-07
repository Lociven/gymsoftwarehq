# GymSoftwareHQ

Independent gym & studio software comparison site (gymsoftwarehq.com).

- `data/gym_software.json` — the single source of truth (tools, pricing, complaints, affiliate links)
- `build.py` — static site generator → outputs `site/` (40+ pages, sitemap, robots)
- Deployed on Netlify (auto-build: `python3 build.py`, publish `site/`)

To update: edit `data/gym_software.json`, commit, push → Netlify rebuilds automatically.
