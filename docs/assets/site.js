const dialog = document.querySelector('dialog');
let trigger;
for (const button of document.querySelectorAll('[data-enlarge]')) {
  button.addEventListener('click', () => {
    trigger = button;
    const image = dialog.querySelector('img');
    image.src = button.dataset.enlarge;
    image.alt = button.querySelector('img').alt;
    dialog.showModal();
  });
}
if (dialog) {
  dialog.querySelector('button').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => trigger?.focus());
}
for (const select of document.querySelectorAll('[data-speed]')) {
  select.addEventListener('change', () => { document.getElementById(select.dataset.speed).playbackRate = Number(select.value); });
}
for (const video of document.querySelectorAll('video')) {
  video.addEventListener('play', () => {
    for (const other of document.querySelectorAll('video')) if (other !== video) other.pause();
  });
}
const chapters = [...document.querySelectorAll('.chapter')];
const links = [...document.querySelectorAll('.chapter-list a')];
function selectChapter() {
  if (!chapters.length) return;
  const id = location.hash.slice(1);
  const chosen = chapters.find(chapter => chapter.id === id) || chapters[0];
  for (const chapter of chapters) {
    const active = chapter === chosen;
    chapter.classList.toggle('hidden', !active);
    if (!active) chapter.querySelector('video')?.pause();
  }
  if (chapters.some(chapter => chapter.id === id)) requestAnimationFrame(() => chosen.scrollIntoView({block: 'start'}));
  for (const link of links) link.setAttribute('aria-current', String(link.hash.slice(1) === chosen.id));
  for (const language of document.querySelectorAll('.languages a')) {
    const url = new URL(language.href);
    url.hash = location.hash;
    language.href = url.href;
  }
}
selectChapter();
window.addEventListener('hashchange', selectChapter);
for (const control of document.querySelectorAll('[data-play-overview]')) {
  control.addEventListener('click', () => {
    document.getElementById('video-overview')?.play().catch(() => {});
  });
}
