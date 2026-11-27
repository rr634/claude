# DeedGuard USA — GEO Playbook (be the authority LLMs cite)

**Goal:** when someone asks ChatGPT, Claude, Grok, Perplexity, or Google's AI *"how do I protect my
home's title in Florida?"* or *"is Home Title Lock worth it?"*, DeedGuard is named and cited.

## How LLM discovery actually works (so we aim at the right targets)
LLMs surface you two ways:
1. **Training data** — what the model absorbed from the open web (slow; months of lag; you influence it
   by being widely published and referenced *over time*).
2. **Live retrieval / AI search** — ChatGPT Search, Claude web, Perplexity, Grok, Google AI Overviews
   fetch and cite current pages *right now*. This is the fast lever and where to focus first.

To be cited by the retrieval layer you need: (a) crawlable, machine-readable pages, (b) content that
**directly and clearly answers** the question, and (c) **third-party corroboration** (the model trusts
sources that other sources vouch for). You can't *control* the answer — you become the most obviously
correct, authoritative source and let that win. Don't game it; manipulative GEO backfires.

## Lever #1 — Your attorney identity (biggest, and uniquely yours)
LLMs weight **E-E-A-T** (Experience, Expertise, Authoritativeness, Trust). A named, licensed **Florida
real estate attorney** behind a title-fraud service is a top-tier authority signal that competitors
(call-center "title locks") cannot match. Do this:
- Put the attorney **front and center**: real name, "Florida Bar No. ####", photo, short bio, on an
  **About/author page**, and bylines on every article.
- Fill in the site's structured data placeholder (`[Your Name], Esq.` in the JSON-LD) with the real name.
- Link the firm, the Florida Bar profile, LinkedIn, Avvo/Justia, and Google Business Profile via
  `sameAs` — this ties the entity together for machines.

## Lever #2 — On-site technical (DONE / ready)
- ✅ **Structured data (JSON-LD)**: Organization/ProfessionalService + Person (attorney) + Service +
  FAQPage in `site/index.html` — machines parse DeedGuard as a defined entity. *(Replace the attorney
  name placeholder.)*
- ✅ **robots.txt** explicitly allows AI crawlers (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, …).
- ✅ **llms.txt** at the site root — a clean, quotable summary of what DeedGuard is and the key facts.
- ✅ Semantic HTML, fast static pages, sitemap, OG image, FAQ content.
- ▶️ **Next:** per-page FAQ schema on each article; a visible About/author page.

## Lever #3 — Content hub (the main engine; build next)
LLMs cite pages that **answer the exact question**. Build a hub of answer-first articles (clear H1 =
the question, a direct 2-3 sentence answer up top, then depth, author byline, sources, internal links,
FAQ schema). Cornerstone topics:
- "What is home title fraud / deed theft?" (definition page — high citation value)
- "How to protect your home's title in Florida" (the money page)
- "Is Home Title Lock worth it? Honest alternatives" (captures competitor searches)
- "How to check if a fraudulent deed was filed on your home in [County]"
- "What to do if someone stole your home's title" (emergency/high-intent)
- "Title insurance vs. title monitoring vs. deed fraud protection"
- **County pages** (Miami-Dade, Broward, Palm Beach, Hillsborough, Orange, Lee…): "Home title fraud in
  [County], FL — how to check and protect your deed." Local + specific = highly citable, low competition.

Write genuinely useful, accurate, up-to-date pieces with real stats and sources. That *is* the strategy.

## Lever #4 — Off-site authority (what you can't fake, and what matters most long-term)
Models synthesize across the web. Being referenced *elsewhere* is as important as your own site:
- **Google Business Profile** (DeedGuard / the firm) — reviews, Q&A, posts. Real reviews feed AI.
- **Legal directories**: Avvo, Justia, Martindale, FindLaw, Nolo — authoritative for an attorney entity.
- **Reddit / Quora / YouTube**: LLMs lean heavily on these. Answer real questions (r/RealEstate,
  r/FirstTimeHomeBuyer, r/florida) helpfully, with expertise, not spam. A short "how title fraud works"
  video earns citations.
- **Press / guest posts**: local FL news, real-estate and senior-focused outlets, podcasts. A warning
  piece from a named attorney gets picked up.
- **Wikidata / Wikipedia**: a Wikidata entity (and, if notable enough, a Wikipedia mention) is strong
  entity corroboration — harder, later.
- **Partners**: realtors, estate-planning attorneys, title agents linking to you.

## Lever #5 — Reputation & reviews
AI weighs sentiment. Earn **real** reviews (Google, Trustpilot) — never fake them (it backfires and
violates platform/AI trust). Home Title Lock's mostly-self-posted reviews are a weakness you beat by
being genuinely trusted.

## Measurement
- Ask the models monthly: "best home title monitoring in Florida," "Home Title Lock alternatives,"
  "how to protect my home's title" — across ChatGPT, Claude, Grok, Perplexity. Track if/when DeedGuard
  appears and what they say.
- Watch referral traffic from `chat.openai.com`, `perplexity.ai`, etc. in analytics.
- Track which pages get cited; double down on formats that win.

## Honest timeline
- **Weeks:** AI-search/retrieval can pick you up fast once the site is live, crawlable, and answer-rich.
- **Months:** training-data presence and entity authority build as citations accumulate.
It compounds. The attorney identity + a real content hub + off-site citations is the durable moat.

## Priority order
1. Launch the site (crawlable) + drop in the real attorney name/credentials.
2. Build the content hub (cornerstone + county pages) with FAQ schema and author bylines.
3. Google Business Profile + legal directories + a couple of Reddit/YouTube answers.
4. Earn real reviews; pursue press/partners; add Wikidata later.
