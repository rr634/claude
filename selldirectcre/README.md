# Sell Direct CRE: selldirectcre.com

A friendly, one-page site for buying South Florida commercial property for cash, with listing through the brokerage as a second option. It's static, with no build step. Everything lives in `site/`.

## Before launch
Search `site/index.html` for `TODO` and `[`.
- **Phone:** replace `(305) 000-0000` / `tel:+13050000000`. It appears in the nav, the bottom call-to-action, the footer, and the phone call bar.
- **Email:** `hello@selldirectcre.com`, also set as `TO_EMAIL` in the script.
- **Team photo (optional):** save it as `assets/team.jpg`, then use `.photo{background-image:url(assets/team.jpg)}` in the "Who you'll talk to" section and delete the placeholder `<div class="ph">`.
- **About text:** the "Who you'll talk to" wording is a placeholder. Make it true and specific.
- **Promises to confirm:**
  - offer in 48 hours
  - close in 2 weeks
  - "I cover the usual closing costs"
  - "Legal know-how on our side"
  - the comparison-table ranges
- **Legal footer:** the brokerage's legal name and DBPR license number, and the buying LLC.
- **Form:** paste a Formspree, Basin or Getform URL into `FORM_ENDPOINT`. Until then, the form opens the visitor's email app.

## Name
A quick web search found no other business using "Sell Direct CRE". Run a USPTO/Sunbiz check and confirm the domain is available before you buy it.

## Deploy
This repository's Pages site already serves brkwatercap.com, and Pages allows one custom domain per repository. Either put `site/` in its own repository and turn on Pages there, or use Netlify or Cloudflare Pages with the publish directory set to `selldirectcre/site`.
