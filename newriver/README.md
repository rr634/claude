# New River Realty: newriverrealty.com

A one-page static site: `site/index.html` plus `site/assets/`. It has no build step and no dependencies other than Google Fonts.

## Before launch (placeholders to replace)

Search `index.html` for `TODO`. The placeholders are:

- **Phone:** `(954) 000-0000` / `tel:+19540000000`, which appears in the contact section and the footer.
- **Email:** `hello@newriverrealty.com`. Set it up once the domain is live. It's also set as `TO_EMAIL` in the script at the bottom of the page.
- **Legal footer:** the brokerage's legal name and Florida DBPR license number (`License #[XXXXXXX]`).
- **Form delivery (optional):** right now the form opens the visitor's email app with the message pre-filled. To receive submissions directly, create a free form endpoint (Formspree, Basin, Getform) and paste its URL into `FORM_ENDPOINT`.

## Adding photos

The page uses illustrated gradients, so it looks finished without photos. You can add real photography:

- **Hero:** save `site/assets/hero.jpg` (about 2400×1600), then uncomment the `.hero-bg` photo line in the CSS.
- **Approach panel:** add `site/assets/approach.jpg` (portrait, 4:5) and set `.visual{background:url(assets/approach.jpg) center/cover}`.
- **Neighborhood tiles (`.h1` to `.h6`):** add, for example, `.h1{--bg:url(assets/fort-lauderdale.jpg) center/cover}`.

## Deploying

GitHub Pages serves only one custom domain per repository, and this repository already serves brkwatercap.com. Use one of these options:

1. **Own repository (matches how DeedGuard is set up):** copy `newriver/site/` into a new repository such as `rr634/newriver`, enable Pages under Settings → Pages → Source: GitHub Actions or the branch root, and keep `CNAME`.
2. **Netlify or Cloudflare Pages:** connect this repository and set the publish directory to `newriver/site`. No build command is needed.

DNS at your registrar for GitHub Pages:

- `A` records for `@` pointing to 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
- a `CNAME` record for `www` pointing to `rr634.github.io`
