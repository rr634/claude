# Vendí: vendicre.com 

A one-page static site in `site/`. It has no build step.

The site works two ways: owners can sell their South Florida commercial property to us for cash, or list it with our brokerage.

## Before launch: replace placeholders (search `TODO` and `[` in index.html)
- Phone `(305) 000-0000` / `tel:+13050000000`. It appears in the nav, the call-to-action band, the footer and the sticky phone bar.
- Email `offers@vendicre.com`, also set as `TO_EMAIL` in the script.
- Founder name, title and photo (`assets/founder.jpg`) for the "Who you're dealing with" section.
- Legal footer: the brokerage's legal name and DBPR license number, and the LLC that makes the cash purchases.
- Service promises to confirm or change:
  - "48 hours to a written offer"
  - "as little as 14 days to close"
  - "we cover typical closing costs"
  - "legal & title expertise in-house"
  - the comparison table's commission and timing ranges
- Form delivery: paste a Formspree, Basin or Getform URL into `FORM_ENDPOINT`. Until then, the form opens the visitor's email app with the details pre-filled.
- Name and domain: no conflicting "Vendí" business turned up in a web search, but run a USPTO and Sunbiz check. Register vendicre.com, and vendi.com if it's available.

## Photos (optional)
- Hero: uncomment the `.hero::before` photo line and add `assets/hero.jpg`.
- Founder: set `.portrait{background:url(assets/founder.jpg) center/cover}`.

## Going live

GitHub Pages serves one custom domain per repository, and this repository already serves brkwatercap.com, so Vendí gets its own repository.

1. **Create the repository.** Create an empty repository named `rr634/vendi` on GitHub. Public is fine, and you don't need a README.
2. **I push the site.** That covers the site files at the root plus `deploy/pages.yml` as `.github/workflows/pages.yml`. The workflow turns Pages on and deploys automatically. The site is first live at https://rr634.github.io/vendi/.
3. **Buy the domain** (for example vendicre.com). At the registrar, add:
   - `A` records for `@` pointing to `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - a `CNAME` record for `www` pointing to `rr634.github.io`
4. **Connect the domain.** In the vendi repository, go to Settings → Pages → Custom domain, enter the domain and save. Tick "Enforce HTTPS" once the certificate is issued, which usually takes minutes and can take up to a day.
   - Deploying through Actions ignores the CNAME file, so this step is required.
   - If you buy a different domain than vendicre.com, tell me and I'll update `CNAME`, `robots.txt`, `sitemap.xml`, and the canonical and Open Graph tags.

## Leads
Create a free Formspree form and paste its endpoint into `FORM_ENDPOINT` at the bottom of `index.html`. Until then, the form opens the visitor's email app addressed to `offers@vendicre.com`, which you'll also need to set up once you own the domain.
