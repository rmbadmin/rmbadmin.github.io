(() => {
  const $ = (q) => document.querySelector(q);
  const theme = () => document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light';
  const button = $('[data-theme-toggle]');
  function themeLabel() { button.setAttribute('aria-label', theme() === 'dark' ? '切换浅色主题' : '切换深色主题'); }
  themeLabel();
  button.addEventListener('click', () => {
    document.documentElement.dataset.theme = theme() === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem('blog-theme', theme()); } catch {}
    themeLabel();
    const frame = $('iframe.giscus-frame');
    if (frame) frame.contentWindow.postMessage({giscus: {setConfig: {theme: theme()}}}, 'https://giscus.app');
  });
  $('.menu-toggle').addEventListener('click', (event) => {
    const expanded = $('.navigation').classList.toggle('open');
    event.currentTarget.setAttribute('aria-expanded', String(expanded));
  });
  $('[data-top]').addEventListener('click', event => { event.preventDefault(); window.scrollTo({top: 0, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'}); });
  const dialog = $('#search-dialog'), input = $('#search-input'), results = $('#search-results'), status = $('#search-status');
  let records = null, pending = null;
  function renderSearch() {
    results.replaceChildren();
    const query = input.value.trim().toLocaleLowerCase();
    if (!query) { status.textContent = '输入关键词搜索'; return; }
    if (!records) return;
    const found = records.filter(p => `${p.title} ${p.categories.join(' ')} ${p.text}`.toLocaleLowerCase().includes(query));
    status.textContent = found.length ? `找到 ${found.length} 篇文章` : '没有找到匹配文章，换个关键词试试。';
    found.forEach(p => { const li = document.createElement('li'), a = document.createElement('a'), small = document.createElement('small'); a.href = p.url; a.textContent = p.title; small.textContent = `${p.date} · ${p.categories.join(' / ')}`; a.append(small); li.append(a); results.append(li); });
  }
  async function openSearch() {
    dialog.showModal(); input.focus();
    if (!records) { status.textContent = '正在加载文章索引…';
      try { pending ||= fetch('/search.json').then(r => { if (!r.ok) throw Error('search'); return r.json(); }); records = await pending; renderSearch(); }
      catch { pending = null; status.textContent = '索引加载失败，请关闭后重试。'; }
    } else renderSearch();
  }
  $('[data-search-open]').addEventListener('click', openSearch);
  $('[data-search-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', e => { if (e.target === dialog) { const box = dialog.getBoundingClientRect(); if (e.clientX < box.left || e.clientX > box.right || e.clientY < box.top || e.clientY > box.bottom) dialog.close(); } });
  input.addEventListener('input', renderSearch);
  document.addEventListener('keydown', e => { if (e.key === '/' && !dialog.open && !e.ctrlKey && !e.metaKey && !/input|textarea|select/i.test(e.target.tagName) && !e.target.isContentEditable) { e.preventDefault(); openSearch(); } });
  const outline = $('#outline');
  if (outline) {
    const headings = [...document.querySelectorAll('#article-body h2, #article-body h3')];
    headings.forEach((h, i) => { if (!h.id) h.id = `section-${i + 1}`; const li = document.createElement('li'), a = document.createElement('a'); a.href = `#${encodeURIComponent(h.id)}`; a.textContent = h.textContent; li.append(a); outline.append(li); });
    if (!headings.length) $('.outline').hidden = true;
  }
  async function loadComments() {
    const target = $('#github-comments'); if (!target) return;
    try {
      const response = await fetch('/assets/comments.json'); if (!response.ok) throw Error('config'); const config = await response.json();
      if (!config.enabled) return;
      if (!config.repo || !config.repoId || !config.categoryId) { target.textContent = 'GitHub 留言配置未完成。'; return; }
      const script = document.createElement('script'); script.src = 'https://giscus.app/client.js'; script.async = true; script.crossOrigin = 'anonymous';
      const values = {repo: config.repo, 'repo-id': config.repoId, category: config.category, 'category-id': config.categoryId, mapping: 'pathname', strict: '1', 'reactions-enabled': '1', 'emit-metadata': '0', 'input-position': 'top', theme: theme(), lang: 'zh-CN', loading: 'lazy'};
      Object.entries(values).forEach(([k,v]) => script.setAttribute(`data-${k}`, v));
      target.replaceChildren(script);
    } catch { target.textContent = '暂时无法加载留言配置，请稍后重试。'; }
  }
  loadComments();
})();
