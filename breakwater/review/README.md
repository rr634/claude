# Review build — NOT published

These are **private, non-live review copies** of the Breakwater site.

- `index.review.html` — homepage
- `investors.review.html` — gated investor page

**Why they're safe to share for review but not "live":**
- Each carries `<meta name="robots" content="noindex, nofollow">`, so search
  engines won't index them even if hosted.
- Each shows a fixed red **"Private draft — not live · review copy"** ribbon.
- They live OUTSIDE `breakwater/site/`, so the GitHub Pages workflow
  (`.github/workflows/pages.yml`, which only publishes `breakwater/site/`)
  will **never** deploy them.

**How to review:** open either file directly in a browser (double-click).
The cross-links between them work locally. No server needed.

When you're ready to go live, the source of truth is `breakwater/site/` —
the review copies are generated from it. Re-generate after any change to the
live files; do not edit these by hand.
