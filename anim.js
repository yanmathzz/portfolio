/**
 * Portfolio — Yan Matheus
 * Comportamento: fade-in, scroll reveal, cursor glow, tilt, nav.
 * CSS vem de design.css (não mais injetado via JS).
 */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {

    requestAnimationFrame(function () { document.body.classList.add('ym-ready'); });

    var isTouch = window.matchMedia('(hover:none)').matches;
    var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* Cursor spotlight */
    if (!isTouch && !prefersReducedMotion) {
      var glow = document.createElement('div');
      glow.id = 'ym-glow';
      document.body.appendChild(glow);
      var mx = -9999, my = -9999, pending = false;
      function paintGlow() {
        var dark = document.documentElement.classList.contains('dark');
      var c = dark ? 'rgba(73,163,155,.10)' : 'rgba(15,118,110,.10)';
        glow.style.background = 'radial-gradient(700px circle at ' + mx + 'px ' + my + 'px,' + c + ',transparent 75%)';
        pending = false;
      }
      document.addEventListener('mousemove', function (e) {
        mx = e.clientX; my = e.clientY;
        if (!pending) { pending = true; requestAnimationFrame(paintGlow); }
      }, { passive: true });
    }

    /* Auto fade-up */
    var AUTO = ['main section', 'article', '.rounded-2xl', 'ol > li', '.grid > *', '.space-y-10 > *', '.flex.flex-col.gap-16 > *'];
    AUTO.forEach(function (sel) {
      try {
        document.querySelectorAll(sel).forEach(function (el) {
          if (!el.classList.contains('fade-up') && !el.closest('.fade-up')) el.classList.add('fade-up');
        });
      } catch (ex) {}
    });

    /* Scroll reveal */
    if (prefersReducedMotion || typeof IntersectionObserver === 'undefined') {
      document.querySelectorAll('.fade-up').forEach(function (el) {
        el.classList.add('in');
        el.style.transitionDelay = '0s';
      });
    } else {
      var obs = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { e.target.classList.add('in'); obs.unobserve(e.target); }
        });
      }, { threshold: 0.06, rootMargin: '0px 0px -28px 0px' });
      document.querySelectorAll('.fade-up').forEach(function (el, i) {
        if (!el.style.transitionDelay) el.style.transitionDelay = Math.min(i * 0.055, 0.45) + 's';
        obs.observe(el);
      });
    }

    /* 3D tilt */
    if (!isTouch && !prefersReducedMotion) {
      document.querySelectorAll('article, .rounded-2xl').forEach(function (el) {
        if (el.closest('nav') || el.matches('article.article-row')) return;
        el.classList.add('ym-tilt');
        el.addEventListener('mousemove', function (ev) {
          var r = el.getBoundingClientRect();
          var x = (ev.clientX - r.left) / r.width - 0.5;
          var y = (ev.clientY - r.top) / r.height - 0.5;
          el.style.transform = 'perspective(700px) rotateY(' + (x * 5) + 'deg) rotateX(' + (-y * 3.5) + 'deg) translateZ(5px)';
        });
        el.addEventListener('mouseleave', function () { el.style.transform = ''; });
      });
    }

    /* Nav active highlight */
    var page = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('nav a, footer a').forEach(function (a) {
      var href = (a.getAttribute('href') || '').replace('./', '');
      if (href === page || (page === '' && href === 'index.html')) a.classList.add('ym-nav-active');
    });

    /* Nav scroll shadow */
    var nav = document.getElementById('site-nav') || document.querySelector('header');
    if (nav) {
      var tick = false;
      window.addEventListener('scroll', function () {
        if (!tick) {
          requestAnimationFrame(function () {
            nav.classList.toggle('ym-nav-shadow', window.scrollY > 72);
            tick = false;
          });
          tick = true;
        }
      }, { passive: true });
    }

  });
})();
