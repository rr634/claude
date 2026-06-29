# Go live: DeedGuard USA → deedguardusa.com

The repo is **deploy-ready**. Pick ONE host below, connect this repo, point it at
**`titlelock/site`**, and add the domain. ~10 minutes, no build step.

> Recommended: **Netlify** (it reads the included `netlify.toml`, so it's the fewest clicks),
> or **Cloudflare** if you want domain + hosting + DNS all in one place.

---

## Step 1 — Register the domain
Buy **deedguardusa.com** at any registrar (Cloudflare ~$10, Namecheap, GoDaddy).
If you use **Cloudflare Pages** for hosting, registering the domain at Cloudflare too makes
Step 3 automatic.

## Step 2 — Connect the host (pick one)

### Option A — Netlify (uses `netlify.toml`)
1. netlify.com → **Add new site → Import from Git** → pick `rr634/claude`.
2. Set **Base directory = `titlelock`**. (Build command empty; publish dir `site` — already in `netlify.toml`.)
3. **Deploy**. You get a temporary `*.netlify.app` URL immediately.

### Option B — Cloudflare Pages
1. Cloudflare dash → **Workers & Pages → Create → Pages → Connect to Git** → `rr634/claude`.
2. Framework preset **None**, build command **empty**, **build output directory = `titlelock/site`**.
3. **Save and Deploy** → temporary `*.pages.dev` URL.

### Option C — Vercel
1. Vercel → **Add New → Project** → import `rr634/claude`.
2. Framework **Other**, **Output Directory = `titlelock/site`**, build command empty.
3. **Deploy** → temporary `*.vercel.app` URL.

## Step 3 — Add the custom domain + DNS
1. In the host: **Domains/Custom domains → Add `deedguardusa.com`** (and `www`).
2. Point DNS at the host per its instructions:
   - **Cloudflare Pages** + domain on Cloudflare → added automatically.
   - **Netlify/Vercel** → either use their nameservers, or add the **apex A/ALIAS** record (and a
     `www` CNAME) they show you at your registrar.
3. Wait for DNS to propagate (minutes–hours). HTTPS is issued automatically.

Done — `https://deedguardusa.com` is live. The site already sets `CNAME`, canonical URL,
`sitemap.xml`, and `robots.txt` to this domain.

---

## Before you point real customers at it
- ✅ **FL availability:** ALTA 49 / 49.1 is approved/available in Florida. Pull Old Republic's
  underwriting bulletin for your **endorsement cost** and any date-down requirement, and drop the
  number into `tools/economics.html`.
- ✅ Wire the free-check form to your inbox/CRM (currently a client-side demo — see `checkForm` in `site/index.html`).
- ✅ Have counsel sign off on the insurance language (it's attorney-branded and makes coverage claims).
