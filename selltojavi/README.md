# Sell to Javi: selltojavi.com

A friendly, founder-led, one-page site for buying South Florida commercial property for cash, with listing through the brokerage as a second option. It's static, with no build step. Everything lives in `site/`.

## Before launch
Search `site/index.html` for `TODO` and `[`.
- **Phone:** replace `(305) 000-0000` / `tel:+13050000000`. It appears in the nav, the bottom call-to-action, the footer, and the phone call bar.
- **Email:** `hello@selltojavi.com`, also set as `TO_EMAIL` in the script.
- **Javi's photo:** save it as `assets/javi.jpg`, then:
  - hero avatar: `.avatar{background-image:url(assets/javi.jpg)}` and remove the "J"
  - Meet Javi: `.photo{background-image:url(assets/javi.jpg)}` and delete the placeholder `<div class="ph">`
- **Javi's story:** the "Meet Javi" text is a placeholder written in first person. Make it true and specific.
- **Promises to confirm:**
  - offer in 48 hours
  - close in 2 weeks
  - "I cover the usual closing costs"
  - "Legal know-how on our side"
  - the comparison-table ranges
- **Legal footer:** the brokerage's legal name and DBPR license number, and the buying LLC.
- **Form:** paste a Formspree, Basin or Getform URL into `FORM_ENDPOINT`. Until then, the form opens the visitor's email app.

## Name / trademark note
SELL TO BOBBY is a registered mark (Sell To Bobby LLC, Miami) for real estate brokerage and investment services. "Sell to Javi" uses the same "Sell to [first name]" pattern for overlapping services in the same market. Clear it before you buy the domain or spend on marketing.

## Deploy
This repository's Pages site already serves brkwatercap.com, and Pages allows one custom domain per repository. Either put `site/` in its own repository and turn on Pages there, or use Netlify or Cloudflare Pages with the publish directory set to `selltojavi/site`.
