/* KUNDE ELECTRIC — progressive enhancement layer
   No framework, no dependencies, no network calls except the lazy search index.
   Every feature degrades to usable HTML when JS is unavailable. */
(() => {
  'use strict';
  const $  = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------------------------------------------------------- toast */
  let toastTimer;
  function toast(msg) {
    let el = $('.toast');
    if (!el) { el = document.createElement('div'); el.className = 'toast';
      el.setAttribute('role', 'status'); document.body.appendChild(el); }
    el.textContent = msg;
    requestAnimationFrame(() => el.classList.add('show'));
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.remove('show'), 2400);
  }

  /* ---------------------------------------------------------------- theme */
  const themeBtn = $('#theme-toggle');
  function syncThemeLabel() {
    if (!themeBtn) return;
    const dark = document.documentElement.dataset.theme === 'dark';
    themeBtn.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
    themeBtn.setAttribute('title', dark ? 'Light theme' : 'Dark theme');
    const sun = themeBtn.querySelector('.i-sun'), moon = themeBtn.querySelector('.i-moon');
    if (sun && moon) { sun.hidden = !dark; moon.hidden = dark; }
    themeBtn.setAttribute('aria-pressed', String(dark));
  }
  themeBtn?.addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem('kunde-theme', next); } catch (_) {}
    syncThemeLabel();
    toast(next === 'dark' ? 'Dark theme on' : 'Light theme on');
  });
  syncThemeLabel();

  /* ------------------------------------------------------- mobile drawer */
  const drawer = $('#drawer');
  const backdrop = $('#drawer-backdrop');
  const burger = $('#menu-toggle');
  function setDrawer(open) {
    if (!drawer || !backdrop) return;
    drawer.classList.toggle('open', open);
    backdrop.classList.toggle('open', open);
    document.body.classList.toggle('no-scroll', open);
    burger?.setAttribute('aria-expanded', String(open));
    drawer.setAttribute('aria-hidden', String(!open));
    drawer.inert = !open;   // 离屏抽屉不进入 Tab 顺序
    if (open) { $('#drawer-close')?.focus(); }
    else { burger?.focus(); }
  }
  burger?.addEventListener('click', () => setDrawer(!drawer.classList.contains('open')));
  $('#drawer-close')?.addEventListener('click', () => setDrawer(false));
  backdrop?.addEventListener('click', () => setDrawer(false));
  $$('#drawer a').forEach(a => a.addEventListener('click', () => setDrawer(false)));

  /* ------------------------------------------------------------ mega menu */
  const megaBtn = $('#mega-toggle');
  const mega = $('#mega');
  function setMega(open) {
    if (!mega || !megaBtn) return;
    mega.hidden = !open;
    megaBtn.setAttribute('aria-expanded', String(open));
  }
  megaBtn?.addEventListener('click', e => { e.stopPropagation(); setMega(mega.hidden); });
  megaBtn?.parentElement?.addEventListener('mouseenter', () => {
    if (matchMedia('(hover: hover) and (min-width: 961px)').matches) setMega(true);
  });
  megaBtn?.parentElement?.addEventListener('mouseleave', () => setMega(false));
  mega?.addEventListener('click', () => setMega(false));
  document.addEventListener('click', e => {
    if (mega && !mega.hidden && !e.target.closest('.mega-wrap')) setMega(false);
  });

  /* ---------------------------------------------------------------- search */
  const overlay = $('#search-overlay');
  const input = $('#search-input');
  const results = $('#search-results');
  const searchFoot = $('#search-foot');
  let index = null, loading = false, activeIdx = -1;

  async function loadIndex() {
    if (index || loading) return;
    loading = true;
    if (searchFoot) searchFoot.textContent = 'Loading catalogue index…';
    try {
      const res = await fetch('assets/search-index.json', { credentials: 'same-origin' });
      if (!res.ok) throw new Error('HTTP ' + res.status);
      index = await res.json();
      if (searchFoot) searchFoot.textContent =
        index.length.toLocaleString('en-US') + ' products indexed · type to filter · ↑↓ to navigate · Esc to close';
      render('');
    } catch (err) {
      if (searchFoot) searchFoot.textContent = 'Search index unavailable — use the product catalogue instead.';
    } finally { loading = false; }
  }
  function render(q) {
    if (!results || !index) return;
    const terms = q.toLowerCase().trim().split(/\s+/).filter(Boolean);
    let hits = index;
    if (terms.length) {
      hits = index.filter(p => terms.every(t => p.k.includes(t)));
    }
    const top = hits.slice(0, 40);
    activeIdx = -1;
    if (!top.length) {
      results.innerHTML = '<div class="search-empty">No matching products. Try a shorter model or a material keyword.</div>';
      return;
    }
    results.innerHTML = top.map((p, i) =>
      `<a href="${p.u}" data-i="${i}">` +
      `<img src="${p.t}" alt="" width="46" height="46" loading="lazy" decoding="async">` +
      `<span><span class="t">${escapeHtml(p.n)}</span><br><span class="s">ID ${p.i}${p.c ? ' · ' + escapeHtml(p.c) : ''}</span></span></a>`
    ).join('');
    if (terms.length && searchFoot) searchFoot.textContent =
      `${hits.length.toLocaleString('en-US')} result${hits.length === 1 ? '' : 's'}${hits.length > 40 ? ' · showing first 40' : ''}`;
  }
  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, c =>
      ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  }
  function openSearch() {
    if (!overlay) return;
    overlay.classList.add('open');
    overlay.setAttribute('aria-hidden', 'false');
    document.body.classList.add('no-scroll');
    setMega(false); setDrawer(false);
    input?.focus();
    loadIndex();
  }
  function closeSearch() {
    if (!overlay) return;
    overlay.classList.remove('open');
    overlay.setAttribute('aria-hidden', 'true');
    if (!drawer?.classList.contains('open')) document.body.classList.remove('no-scroll');
  }
  $$('[data-open-search]').forEach(b => b.addEventListener('click', openSearch));
  $('#search-close')?.addEventListener('click', closeSearch);
  overlay?.addEventListener('click', e => { if (e.target === overlay) closeSearch(); });
  input?.addEventListener('input', () => render(input.value));
  input?.addEventListener('keydown', e => {
    const links = $$('#search-results a');
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      if (!links.length) return;
      activeIdx = (activeIdx + (e.key === 'ArrowDown' ? 1 : -1) + links.length) % links.length;
      links.forEach((a, i) => a.toggleAttribute('data-active', i === activeIdx));
      links[activeIdx].focus();
    } else if (e.key === 'Enter' && activeIdx >= 0 && links[activeIdx]) {
      e.preventDefault(); links[activeIdx].click();
    }
  });

  /* ------------------------------------------------------------- shortcuts */
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') { closeSearch(); setMega(false); setDrawer(false); }
    if (e.key === '/' && !/input|textarea/i.test(document.activeElement?.tagName || '')
        && !overlay?.classList.contains('open')) { e.preventDefault(); openSearch(); }
  });

  /* --------------------------------------------------------------- gallery */
  const mainImg = $('#gallery-main-img');
  const galleryData = (() => {
    try { return JSON.parse($('#gallery-data')?.textContent || '[]'); } catch (_) { return []; }
  })();
  $$('.thumbs button').forEach((btn, i) => {
    btn.addEventListener('click', () => {
      if (!mainImg) return;
      mainImg.src = btn.dataset.src;
      mainImg.alt = btn.dataset.alt || mainImg.alt;
      $$('.thumbs button').forEach(b => b.setAttribute('aria-current', 'false'));
      btn.setAttribute('aria-current', 'true');
      mainImg.dataset.current = String(i);
    });
  });

  const lightbox = $('#lightbox');
  const lbImg = $('#lightbox-img');
  const lbCount = $('#lightbox-count');
  let lbIdx = 0;
  function showLb(i) {
    if (!lightbox || !galleryData.length) return;
    lbIdx = (i + galleryData.length) % galleryData.length;
    if (lbImg) { lbImg.src = galleryData[lbIdx].src; lbImg.alt = galleryData[lbIdx].alt; }
    if (lbCount) lbCount.textContent = `${lbIdx + 1} / ${galleryData.length}`;
  }
  $$('[data-open-lightbox]').forEach(b => b.addEventListener('click', () => {
    if (!lightbox) return;
    showLb(Number(mainImg?.dataset.current || b.dataset.i || 0));
    if (typeof lightbox.showModal === 'function') lightbox.showModal();
    else location.href = galleryData[lbIdx].src;
  }));
  $('#lightbox-close')?.addEventListener('click', () => lightbox?.close());
  $('#lightbox-prev')?.addEventListener('click', () => showLb(lbIdx - 1));
  $('#lightbox-next')?.addEventListener('click', () => showLb(lbIdx + 1));
  lightbox?.addEventListener('click', e => { if (e.target === lightbox) lightbox.close(); });
  lightbox?.addEventListener('keydown', e => {
    if (e.key === 'ArrowLeft') showLb(lbIdx - 1);
    if (e.key === 'ArrowRight') showLb(lbIdx + 1);
  });

  /* ------------------------------------------- prefill enquiry from query */
  const qs = new URLSearchParams(location.search);
  const prefill = qs.get('product');
  if (prefill && $('#f-product')) $('#f-product').value = prefill;

  /* ------------------------------------------------------------ copy email */
  $$('[data-copy]').forEach(btn => btn.addEventListener('click', async () => {
    const value = btn.dataset.copy;
    try {
      await navigator.clipboard.writeText(value);
      toast('Copied: ' + value);
    } catch (_) {
      const ta = document.createElement('textarea');
      ta.value = value; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); toast('Copied: ' + value); }
      catch (_) { toast('Please copy manually: ' + value); }
      ta.remove();
    }
  }));

  /* ---------------------------------------------------------- inquiry form */
  const form = $('#inquiry-form');
  form?.addEventListener('submit', e => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    const fd = new FormData(form);
    const subject = `[Website enquiry] ${fd.get('product') || 'General enquiry'}`;
    const lines = [
      `Name:    ${fd.get('name') || ''}`,
      `Company: ${fd.get('company') || ''}`,
      `Email:   ${fd.get('email') || ''}`,
      `Phone:   ${fd.get('phone') || ''}`,
      `Product / ID: ${fd.get('product') || ''}`,
      `Quantity: ${fd.get('quantity') || ''}`,
      '', 'Message:', String(fd.get('message') || '')
    ];
    const body = lines.join('\n');
    const mailto = 'mailto:sales@kdelec.com?subject=' + encodeURIComponent(subject) +
                   '&body=' + encodeURIComponent(body);
    // 无后端的静态站：生成邮件草稿，用户确认后由本机邮件客户端发送。
    window.location.href = mailto;
    toast('Your email draft is ready — send it from your mail app.');
  });

  /* ----------------------------------------------------------- back to top */
  const toTop = $('.to-top');
  toTop?.addEventListener('click', () => window.scrollTo({ top: 0,
    behavior: reduceMotion ? 'auto' : 'smooth' }));
  const onScroll = () => toTop?.classList.toggle('show', window.scrollY > 700);
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* ------------------------------------------------------------ reveal */
  if (!reduceMotion && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(en => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -40px 0px' });
    $$('.reveal').forEach(el => io.observe(el));
  } else {
    $$('.reveal').forEach(el => el.classList.add('in'));
  }
})();
