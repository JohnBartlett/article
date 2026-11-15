/* How far readers get through an article (John, Nov 15, 2026).
   Sends GA4 events: article_open when the page loads, then article_read_25 / _50 / _75 / _100 the first time
   the bottom of the screen passes that share of the article text (.article-body; 100 = its last line seen).
   The event names alone carry the milestone, so no GA4 custom definitions are needed; the page path names the
   article. Milestones are only checked after the reader scrolls or has had the page visible for 15 seconds, so
   a short article that fits on one screen is not counted as finished the moment it opens.
   Without GA4 (dev/dev2) it does nothing. No personal data: only the page and the milestone. */
(function () {
  'use strict';
  function send(name) {
    if (typeof window.gtag === 'function') window.gtag('event', name, { transport_type: 'beacon' });
  }
  function start() {
    var body = document.querySelector('.article-body');
    if (!body) return;
    send('article_open');
    var marks = [25, 50, 75, 100], sent = {}, pending = false, armed = false;

    function check() {
      pending = false;
      var r = body.getBoundingClientRect();
      if (r.height <= 0) return;
      var seen = (window.innerHeight - r.top) / r.height * 100;
      for (var i = 0; i < marks.length; i++) {
        var m = marks[i];
        if (!sent[m] && seen >= m) { sent[m] = 1; send('article_read_' + m); }
      }
      if (sent[100]) {
        window.removeEventListener('scroll', onScroll);
        window.removeEventListener('resize', onScroll);
      }
    }
    function onScroll() {
      armed = true;
      if (!pending) { pending = true; window.requestAnimationFrame(check); }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll, { passive: true });

    // A reader of a short piece may never scroll: check once after 15 visible seconds.
    var visibleMs = 0, last = Date.now();
    var timer = window.setInterval(function () {
      var now = Date.now();
      if (document.visibilityState === 'visible') visibleMs += now - last;
      last = now;
      if (visibleMs >= 15000) { window.clearInterval(timer); if (!armed) check(); }
    }, 1000);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
