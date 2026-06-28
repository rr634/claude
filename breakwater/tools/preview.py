#!/usr/bin/env python3
"""
Breakwater preview/verification tool.

Renders site pages with Playwright/Chromium and emits SMALL, safe-to-attach JPEG
previews. This is the single place screenshots are produced — never attach raw
full-page PNGs; they can blow past the platform's 32MB message limit.

Guarantees for every preview:
  - JPEG, max width 1200px, quality in [65,75], metadata stripped
  - Final size confirmed UNDER 8MB (quality, then width, are reduced until it fits)
  - Large original PNG saved to a local temp dir only (never attached/committed)

Outputs preview JPEGs to breakwater/previews/preview-<name>.jpg and prints a table:
  page | original dims | compressed dims | size | PASS/FAIL (<8MB)

Usage:
  python3 tools/preview.py                 # render the default set
  python3 tools/preview.py home fort-lauderdale
  python3 tools/preview.py fort-lauderdale --mobile
"""
import os, sys, glob

SITE = os.path.join(os.path.dirname(__file__), "..", "site")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "previews")
ORIG_DIR = "/tmp/bw-preview-originals"          # local only — never attached
CHROME = next(iter(glob.glob("/opt/pw-browsers/chromium*/chrome-linux/chrome")), None)

MAX_W = 1200          # hard max width
Q_START = 75          # quality ceiling (range 65-75)
Q_FLOOR = 60
SIZE_LIMIT = 8 * 1024 * 1024   # 8MB target ceiling (platform hard limit is 32MB)

# Default render set: (name, html file, viewport width, full_page)
DEFAULTS = [
    ("home",            "index.html",          1200, True),
    ("for-lenders",     "for-lenders.html",    1200, True),
    ("fort-lauderdale", "fort-lauderdale.html",1200, True),
]


def render(html_path, out_png, width, full_page):
    from playwright.sync_api import sync_playwright
    url = "file://" + os.path.abspath(html_path)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME) if CHROME else p.chromium.launch()
        pg = b.new_page(viewport={"width": width, "height": 900}, device_scale_factor=1)
        pg.goto(url)
        pg.wait_for_timeout(900)
        pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
        pg.wait_for_timeout(250)
        pg.screenshot(path=out_png, full_page=full_page)
        b.close()


def compress(in_png, out_jpg, max_w=MAX_W, limit=SIZE_LIMIT):
    """Downscale + JPEG-compress until under `limit`. Returns a result dict."""
    from PIL import Image
    im = Image.open(in_png)
    orig = im.size
    im = im.convert("RGB")
    w, h = im.size
    if w > max_w:
        h = int(h * max_w / w); w = max_w
        im = im.resize((w, h), Image.LANCZOS)
    q = Q_START
    # save with NO exif/metadata (PIL writes none unless passed)
    im.save(out_jpg, "JPEG", quality=q, optimize=True, progressive=True)
    # reduce quality, then width, until under the limit
    while os.path.getsize(out_jpg) > limit:
        if q > Q_FLOOR:
            q -= 5
        elif w > 400:
            w = int(w * 0.85); h = int(h * 0.85)
            im = im.resize((w, h), Image.LANCZOS)
        else:
            break
        im.save(out_jpg, "JPEG", quality=q, optimize=True, progressive=True)
    size = os.path.getsize(out_jpg)
    return {"orig": orig, "comp": im.size, "q": q, "size": size, "pass": size < limit}


def human(n):
    for unit in ("B", "KB", "MB"):
        if n < 1024 or unit == "MB":
            return f"{n:.0f}{unit}" if unit == "B" else f"{n/1024**(['B','KB','MB'].index(unit)):.1f}{unit}"
        n2 = n
    return f"{n}B"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    mobile = "--mobile" in sys.argv
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(ORIG_DIR, exist_ok=True)

    if args:
        targets = []
        for name in args:
            html = name if name.endswith(".html") else name + ".html"
            base = os.path.splitext(os.path.basename(html))[0]
            if mobile:
                targets.append((base + "-mobile", html, 390, True))
            else:
                targets.append((base, html, 1200, True))
    else:
        targets = list(DEFAULTS)

    rows = []
    for name, html, width, full in targets:
        html_path = os.path.join(SITE, html)
        if not os.path.exists(html_path):
            rows.append((name, "—", "—", "MISSING", False)); continue
        orig_png = os.path.join(ORIG_DIR, name + ".png")
        out_jpg = os.path.join(OUT_DIR, f"preview-{name}.jpg")
        render(html_path, orig_png, width, full)
        r = compress(orig_png, out_jpg)
        rows.append((name,
                     f"{r['orig'][0]}x{r['orig'][1]}",
                     f"{r['comp'][0]}x{r['comp'][1]} q{r['q']}",
                     f"{r['size']/1024:.0f}KB",
                     r["pass"]))

    # report
    print(f"{'page':<22}{'original':<14}{'compressed':<18}{'size':<10}{'<8MB'}")
    print("-" * 70)
    ok = True
    for name, o, c, s, p in rows:
        print(f"{name:<22}{o:<14}{c:<18}{s:<10}{'PASS' if p else 'FAIL'}")
        ok = ok and p
    print("-" * 70)
    print("previews:", OUT_DIR, "| originals (local only):", ORIG_DIR)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
