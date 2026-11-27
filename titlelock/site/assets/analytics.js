/* DeedGuard demand analytics — shared across all pages.
   Inert until you fill in an ID below: no tracking, no cookies, no errors otherwise.
   Set ONE place here and every page is measured. */
(function () {
  var CFG = {
    plausibleDomain: "", // privacy-friendly, no cookie banner: set to "deedguard.us" (plausible.io)
    ga4Id: "",           // or Google Analytics 4: "G-XXXXXXXXXX"
    metaPixelId: ""      // Meta Pixel for FB/IG ad conversions: "123456789012345"
  };
  window.__DG_ANALYTICS__ = CFG;
  function inject(src, attrs) { var s = document.createElement('script'); s.async = true; s.src = src; if (attrs) { for (var k in attrs) { s.setAttribute(k, attrs[k]); } } document.head.appendChild(s); }
  if (CFG.plausibleDomain) { inject('https://plausible.io/js/script.js', { 'data-domain': CFG.plausibleDomain }); window.plausible = window.plausible || function () { (window.plausible.q = window.plausible.q || []).push(arguments); }; }
  if (CFG.ga4Id) { inject('https://www.googletagmanager.com/gtag/js?id=' + CFG.ga4Id); window.dataLayer = window.dataLayer || []; window.gtag = function () { dataLayer.push(arguments); }; gtag('js', new Date()); gtag('config', CFG.ga4Id); }
  if (CFG.metaPixelId) { !function (f, b, e, v, n, t, s) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); }; if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = []; t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s); }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js'); fbq('init', CFG.metaPixelId); fbq('track', 'PageView'); }
  window.dgTrack = function (name, props) {
    try {
      if (CFG.plausibleDomain && window.plausible) { window.plausible(name, { props: props || {} }); }
      if (CFG.ga4Id && window.gtag) { window.gtag('event', name, props || {}); }
      if (CFG.metaPixelId && window.fbq) { window.fbq('trackCustom', name, props || {}); }
    } catch (e) {}
  };
})();
