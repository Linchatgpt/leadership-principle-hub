(() => {
  const cfg = JSON.parse(document.getElementById('chapter-config')?.textContent || '{}');
  const key = `LPIPage:v2:${location.pathname}`;
  const saved = JSON.parse(localStorage.getItem(key) || '{}');
  if (saved.html) document.querySelector('main')?.replaceChildren(...new DOMParser().parseFromString(saved.html, 'text/html').body.childNodes);
  const root = document.documentElement;
  if (saved.fontSize) root.style.setProperty('--reader-font-size', saved.fontSize);
  if (saved.textColor) root.style.setProperty('--reader-text-color', saved.textColor);
  window.LPIEditor = { key, saved, config: cfg };
})();
