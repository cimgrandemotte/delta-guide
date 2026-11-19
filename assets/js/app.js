/* ==========================================================================
   app.js — Noyau du site : base, nav, reveal, compteurs, curseur, SFX, UI
   Delta Force — The Ultimate Operator's Guide (fan-made)
   ========================================================================== */
(function () {
  'use strict';

  /* ---------- BASE DU SITE (chemins relatifs robustes) ---------- */
  const scriptEl = document.currentScript ||
    Array.from(document.scripts).find(s => /assets\/js\/app\.js/.test(s.src));
  const DF_BASE = scriptEl ? scriptEl.src.replace(/assets\/js\/app\.js.*$/, '') : './';
  window.DF_BASE = DF_BASE;

  const $  = (s, c) => (c || document).querySelector(s);
  const $$ = (s, c) => Array.from((c || document).querySelectorAll(s));
  window.$ = $; window.$$ = $$;

  /* ---------- SFX PROCÉDURAUX (Web Audio, aucun fichier requis) ---------- */
  const SFX = (function () {
    let ctx = null, enabled = localStorage.getItem('df-sfx') !== 'off';
    const ensure = () => {
      if (!ctx) { try { ctx = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { return null; } }
      if (ctx.state === 'suspended') ctx.resume();
      return ctx;
    };
    function tone(freq, dur, type, vol, slide) {
      if (!enabled) return;
      const c = ensure(); if (!c) return;
      const o = c.createOscillator(), g = c.createGain();
      o.type = type || 'square';
      o.frequency.setValueAtTime(freq, c.currentTime);
      if (slide) o.frequency.exponentialRampToValueAtTime(Math.max(40, slide), c.currentTime + dur);
      g.gain.setValueAtTime(0.0001, c.currentTime);
      g.gain.exponentialRampToValueAtTime(vol || 0.05, c.currentTime + 0.008);
      g.gain.exponentialRampToValueAtTime(0.0001, c.currentTime + dur);
      o.connect(g); g.connect(c.destination);
      o.start(); o.stop(c.currentTime + dur + 0.02);
    }
    function noise(dur, vol) {
      if (!enabled) return;
      const c = ensure(); if (!c) return;
      const n = Math.floor(c.sampleRate * dur);
      const buf = c.createBuffer(1, n, c.sampleRate);
      const d = buf.getChannelData(0);
      for (let i = 0; i < n; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / n);
      const src = c.createBufferSource(); src.buffer = buf;
      const f = c.createBiquadFilter(); f.type = 'highpass'; f.frequency.value = 1400;
      const g = c.createGain(); g.gain.value = vol || 0.035;
      src.connect(f); f.connect(g); g.connect(c.destination); src.start();
    }
    return {
      hover:   () => tone(880, 0.045, 'square', 0.018),
      click:   () => { tone(1500, 0.05, 'square', 0.035, 700); noise(0.05, 0.022); },
      success: () => { tone(760, 0.09, 'sine', 0.05); setTimeout(() => tone(1180, 0.13, 'sine', 0.05), 85); },
      error:   () => tone(190, 0.2, 'sawtooth', 0.045, 90),
      open:    () => tone(420, 0.14, 'sine', 0.04, 920),
      close:   () => tone(920, 0.12, 'sine', 0.035, 380),
      boot:    () => { [330, 495, 660, 990].forEach((f, i) => setTimeout(() => tone(f, 0.1, 'sine', 0.035), i * 95)); },
      toggle(){ enabled = !enabled; localStorage.setItem('df-sfx', enabled ? 'on' : 'off'); if (enabled) this.success(); return enabled; },
      get on(){ return enabled; }
    };
  })();
  window.SFX = SFX;

  /* ---------- TOASTS ---------- */
  function toast(msg, ms) {
    let stack = $('.toast-stack');
    if (!stack) { stack = document.createElement('div'); stack.className = 'toast-stack'; document.body.appendChild(stack); }
    const t = document.createElement('div');
    t.className = 'toast'; t.textContent = msg; t.setAttribute('role', 'status');
    stack.appendChild(t);
    setTimeout(() => { t.style.opacity = '0'; t.style.transition = 'opacity .3s'; setTimeout(() => t.remove(), 320); }, ms || 2200);
  }
  window.toast = toast;

  /* ---------- ÉCRAN DE BOOT ---------- */
  function boot() {
    const b = $('.boot'); if (!b) return;
    const hide = () => { b.classList.add('gone'); setTimeout(() => b.remove(), 650); };
    if (document.readyState === 'complete') setTimeout(hide, 650);
    else window.addEventListener('load', () => setTimeout(hide, 500));
    setTimeout(hide, 3200); // garde-fou
  }

  /* ---------- NAVIGATION ---------- */
  function nav() {
    const bar = $('.site-nav'); if (!bar) return;
    const burger = $('.nav-burger'), links = $('.nav-links');
    if (burger && links) {
      burger.addEventListener('click', () => {
        const open = links.classList.toggle('open');
        burger.classList.toggle('open', open);
        burger.setAttribute('aria-expanded', open ? 'true' : 'false');
        SFX.click();
      });
      $$('a', links).forEach(a => a.addEventListener('click', () => {
        links.classList.remove('open'); burger.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
      }));
    }
    let last = 0;
    const onScroll = () => {
      const y = window.scrollY;
      bar.classList.toggle('scrolled', y > 24);
      last = y;
    };
    window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

    // Lien actif
    const here = location.pathname.replace(/index\.html$/, '').replace(/\/$/, '');
    $$('.nav-links a').forEach(a => {
      try {
        const p = new URL(a.href, location.href).pathname.replace(/index\.html$/, '').replace(/\/$/, '');
        if (p && p === here) a.classList.add('active');
      } catch (e) {}
    });
  }

  /* ---------- REVEAL AU SCROLL ---------- */
  function reveal() {
    const els = $$('[data-reveal]'); if (!els.length) return;
    if (!('IntersectionObserver' in window)) { els.forEach(e => e.classList.add('is-visible')); return; }
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e, i) => {
        if (e.isIntersecting) {
          const d = parseInt(e.target.dataset.delay || 0, 10);
          setTimeout(() => e.target.classList.add('is-visible'), d);
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -60px 0px' });
    els.forEach(e => io.observe(e));
  }

  /* ---------- COMPTEURS ANIMÉS ---------- */
  function counters() {
    const els = $$('[data-count]'); if (!els.length) return;
    const run = (el) => {
      const target = parseFloat(el.dataset.count);
      const dec = (el.dataset.count.split('.')[1] || '').length;
      const dur = parseInt(el.dataset.dur || 1500, 10);
      const suffix = el.dataset.suffix || '';
      const t0 = performance.now();
      const tick = (now) => {
        const p = Math.min(1, (now - t0) / dur);
        const e = 1 - Math.pow(1 - p, 3);
        el.textContent = (target * e).toLocaleString('fr-FR', { minimumFractionDigits: dec, maximumFractionDigits: dec }) + suffix;
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    };
    if (!('IntersectionObserver' in window)) { els.forEach(run); return; }
    const io = new IntersectionObserver((en) => en.forEach(e => {
      if (e.isIntersecting) { run(e.target); io.unobserve(e.target); }
    }), { threshold: 0.5 });
    els.forEach(e => io.observe(e));
  }

  /* ---------- BARRES DE STATS ---------- */
  function statbars() {
    const els = $$('.statbar .fill[data-pct]'); if (!els.length) return;
    const fill = (el) => { el.style.width = Math.min(100, Math.max(0, parseFloat(el.dataset.pct))) + '%'; };
    if (!('IntersectionObserver' in window)) { els.forEach(fill); return; }
    const io = new IntersectionObserver((en) => en.forEach(e => {
      if (e.isIntersecting) { setTimeout(() => fill(e.target), 120); io.unobserve(e.target); }
    }), { threshold: 0.35 });
    els.forEach(e => io.observe(e));
  }

  /* ---------- CURSEUR VISEUR ---------- */
  function crosshair() {
    if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;
    if (localStorage.getItem('df-cross') === 'off') return;
    const c = document.createElement('div');
    c.className = 'crosshair'; c.innerHTML = '<i></i>'; c.setAttribute('aria-hidden', 'true');
    document.body.appendChild(c); document.body.classList.add('crosshair-on');
    let x = 0, y = 0, tx = 0, ty = 0, raf = null;
    const loop = () => { x += (tx - x) * 0.4; y += (ty - y) * 0.4; c.style.transform = `translate(${x}px,${y}px)`; raf = requestAnimationFrame(loop); };
    document.addEventListener('mousemove', e => { tx = e.clientX; ty = e.clientY; if (!raf) loop(); }, { passive: true });
    document.addEventListener('mouseover', e => {
      const hot = e.target.closest('a,button,[role="button"],input,select,.chip,.tier-item,summary');
      c.classList.toggle('hot', !!hot);
    });
    document.addEventListener('mouseleave', () => c.style.opacity = '0');
    document.addEventListener('mouseenter', () => c.style.opacity = '1');
  }

  /* ---------- SONS AU SURVOL / CLIC ---------- */
  function sfxBindings() {
    document.addEventListener('mouseover', e => {
      if (e.target.closest('.btn,.chip,.nav-links a,.card,.tier-item')) SFX.hover();
    });
    document.addEventListener('click', e => {
      if (e.target.closest('.btn,.chip,button:not(.copy-btn)')) SFX.click();
    });
  }

  /* ---------- RETOUR EN HAUT ---------- */
  function toTop() {
    const b = document.createElement('button');
    b.className = 'to-top'; b.innerHTML = '▲';
    b.setAttribute('aria-label', 'Retour en haut de la page');
    document.body.appendChild(b);
    b.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
    window.addEventListener('scroll', () => b.classList.toggle('show', window.scrollY > 650), { passive: true });
  }

  /* ---------- PROGRESSION DE LECTURE ---------- */
  function readProgress() {
    const bar = document.createElement('div');
    bar.className = 'read-progress'; bar.setAttribute('aria-hidden', 'true');
    document.body.appendChild(bar);
    const upd = () => {
      const h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = h > 0 ? (window.scrollY / h * 100) + '%' : '0%';
    };
    window.addEventListener('scroll', upd, { passive: true }); upd();
  }

  /* ---------- COPIE DANS LE PRESSE-PAPIERS ---------- */
  function copyButtons() {
    document.addEventListener('click', async (e) => {
      const btn = e.target.closest('[data-copy]'); if (!btn) return;
      const txt = btn.dataset.copy || (btn.previousElementSibling && btn.previousElementSibling.textContent) || '';
      try {
        if (navigator.clipboard && window.isSecureContext) await navigator.clipboard.writeText(txt.trim());
        else {
          const ta = document.createElement('textarea'); ta.value = txt.trim();
          ta.style.position = 'fixed'; ta.style.opacity = '0';
          document.body.appendChild(ta); ta.select(); document.execCommand('copy'); ta.remove();
        }
        const old = btn.textContent;
        btn.textContent = '✓ COPIÉ'; btn.classList.add('done');
        SFX.success(); toast('Code copié dans le presse-papiers');
        setTimeout(() => { btn.textContent = old; btn.classList.remove('done'); }, 1900);
      } catch (err) { SFX.error(); toast('Copie impossible — sélectionnez le texte manuellement'); }
    });
  }

  /* ---------- ONGLETS ---------- */
  function tabs() {
    $$('.tabs').forEach(group => {
      const btns = $$('button', group);
      btns.forEach(b => b.addEventListener('click', () => {
        const id = b.dataset.tab;
        btns.forEach(x => { x.classList.toggle('active', x === b); x.setAttribute('aria-selected', x === b); });
        const scope = group.parentElement;
        $$('.tabpanel', scope).forEach(p => p.classList.toggle('active', p.dataset.panel === id));
      }));
    });
  }

  /* ---------- FILTRES (chips + recherche locale) ---------- */
  function filters() {
    $$('[data-filter-group]').forEach(group => {
      const targetSel = group.dataset.filterTarget;
      const items = $$(targetSel);
      const chips = $$('.chip', group);
      const input = $(group.dataset.filterInput || '#nope');
      const countEl = $(group.dataset.filterCount || '#nope');
      let active = 'all';
      const apply = () => {
        const q = (input && input.value || '').toLowerCase().trim();
        let n = 0;
        items.forEach(it => {
          const tags = (it.dataset.tags || '').toLowerCase();
          const txt = (it.dataset.search || it.textContent || '').toLowerCase();
          const okTag = active === 'all' || tags.split(/\s+/).includes(active);
          const okQ = !q || txt.includes(q);
          const show = okTag && okQ;
          it.style.display = show ? '' : 'none';
          if (show) n++;
        });
        if (countEl) countEl.textContent = n;
      };
      chips.forEach(c => c.addEventListener('click', () => {
        chips.forEach(x => x.classList.toggle('active', x === c));
        active = c.dataset.val || 'all'; apply();
      }));
      if (input) input.addEventListener('input', apply);
      apply();
    });
  }

  /* ---------- TRI DE TABLEAUX ---------- */
  function sortTables() {
    $$('table.df').forEach(tb => {
      $$('thead th.sortable', tb).forEach((th, idx) => {
        th.setAttribute('tabindex', '0');
        const col = Array.from(th.parentElement.children).indexOf(th);
        const doSort = () => {
          const body = $('tbody', tb);
          const rows = Array.from(body.rows);
          const asc = !th.classList.contains('asc');
          $$('thead th', tb).forEach(x => x.classList.remove('asc', 'desc'));
          th.classList.add(asc ? 'asc' : 'desc');
          rows.sort((a, b) => {
            const av = (a.cells[col]?.dataset.sort ?? a.cells[col]?.textContent ?? '').trim();
            const bv = (b.cells[col]?.dataset.sort ?? b.cells[col]?.textContent ?? '').trim();
            const an = parseFloat(av.replace(/[^\d.,-]/g, '').replace(',', '.'));
            const bn = parseFloat(bv.replace(/[^\d.,-]/g, '').replace(',', '.'));
            if (!isNaN(an) && !isNaN(bn)) return asc ? an - bn : bn - an;
            return asc ? av.localeCompare(bv, 'fr') : bv.localeCompare(av, 'fr');
          });
          rows.forEach(r => body.appendChild(r));
        };
        th.addEventListener('click', doSort);
        th.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); doSort(); } });
      });
    });
  }

  /* ---------- MODALES ---------- */
  function modals() {
    document.addEventListener('click', e => {
      const open = e.target.closest('[data-modal-open]');
      if (open) { const m = $('#' + open.dataset.modalOpen); if (m) { m.classList.add('open'); SFX.open(); } }
      if (e.target.closest('[data-modal-close]') || e.target.classList.contains('modal')) {
        const m = e.target.closest('.modal'); if (m) { m.classList.remove('open'); SFX.close(); }
      }
    });
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') $$('.modal.open').forEach(m => m.classList.remove('open'));
    });
  }

  /* ---------- FLIP 3D ---------- */
  function flips() {
    document.addEventListener('click', e => {
      const f = e.target.closest('[data-flip]');
      if (f && !e.target.closest('a,button')) { f.classList.toggle('flipped'); SFX.click(); }
    });
  }

  /* ---------- TYPEWRITER ---------- */
  function typewriter() {
    $$('[data-typewriter]').forEach(el => {
      const full = el.textContent.trim();
      el.textContent = '';
      el.classList.add('typewriter');
      const speed = parseInt(el.dataset.speed || 22, 10);
      const start = () => {
        let i = 0;
        const t = setInterval(() => {
          el.textContent = full.slice(0, ++i);
          if (i >= full.length) { clearInterval(t); el.classList.add('done'); }
        }, speed);
      };
      if ('IntersectionObserver' in window) {
        const io = new IntersectionObserver(en => en.forEach(x => { if (x.isIntersecting) { start(); io.disconnect(); } }), { threshold: .4 });
        io.observe(el);
      } else start();
    });
  }

  /* ---------- PARALLAXE ---------- */
  function parallax() {
    const els = $$('[data-parallax]'); if (!els.length) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    let ticking = false;
    const upd = () => {
      els.forEach(el => {
        const r = el.getBoundingClientRect();
        if (r.bottom < -200 || r.top > window.innerHeight + 200) return;
        const sp = parseFloat(el.dataset.parallax) || 0.18;
        const off = (r.top + r.height / 2 - window.innerHeight / 2) * sp;
        el.style.transform = `translate3d(0, ${off.toFixed(1)}px, 0)`;
      });
      ticking = false;
    };
    window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(upd); } }, { passive: true });
    upd();
  }

  /* ---------- LECTEURS AUDIO ---------- */
  function audioPlayers() {
    $$('.audio-player').forEach(p => {
      const a = $('audio', p), btn = $('.play', p); if (!a || !btn) return;
      btn.addEventListener('click', () => {
        $$('.audio-player audio').forEach(o => { if (o !== a) { o.pause(); o.parentElement.classList.remove('playing'); } });
        if (a.paused) { a.play().catch(() => toast('Audio indisponible')); p.classList.add('playing'); btn.innerHTML = '❚❚'; }
        else { a.pause(); p.classList.remove('playing'); btn.innerHTML = '▶'; }
      });
      a.addEventListener('ended', () => { p.classList.remove('playing'); btn.innerHTML = '▶'; });
      a.addEventListener('error', () => { p.style.opacity = '.5'; btn.disabled = true; btn.title = 'Fichier audio indisponible'; });
    });
  }

  /* ---------- ANNÉE AUTO + DATE DE MAJ ---------- */
  function meta() {
    $$('[data-year]').forEach(e => e.textContent = new Date().getFullYear());
  }

  /* ---------- INIT ---------- */
  function init() {
    boot(); nav(); reveal(); counters(); statbars(); crosshair(); sfxBindings();
    toTop(); readProgress(); copyButtons(); tabs(); filters(); sortTables();
    modals(); flips(); typewriter(); parallax(); audioPlayers(); meta();
    document.addEventListener('click', function once() { SFX.boot(); document.removeEventListener('click', once); }, { once: true });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  /* ---------- API DE DONNÉES ---------- */
  const cache = {};
  window.DF = {
    base: DF_BASE,
    async data(name) {
      if (cache[name]) return cache[name];
      const res = await fetch(DF_BASE + 'data/' + name + '.json');
      if (!res.ok) throw new Error('Données indisponibles : ' + name);
      const j = await res.json(); cache[name] = j; return j;
    },
    esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m])); }
  };
})();
