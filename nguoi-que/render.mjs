// Xuất kịch bản Neoptolemus thành video MP4 1920x1080, 30 khung/giây.
//
// Cần: Node 18+, ffmpeg, và Playwright (npm i playwright).
// Chạy:  node nguoi-que/render.mjs [thư-mục-ra]
// Ra:    neoptolemus.mp4 (nền giấy) và neoptolemus-greenscreen.mp4 (phông xanh để tách nền)
//
// Nếu Chromium đã cài sẵn ở chỗ khác, đặt CHROMIUM_PATH=/đường/dẫn/chromium.

import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const FPS = 30;
const here = path.dirname(fileURLToPath(import.meta.url));
const outDir = path.resolve(process.argv[2] || here);
const page = pathToFileURL(path.join(here, 'index.html')).href;

const browser = await chromium.launch({
  executablePath: process.env.CHROMIUM_PATH || undefined,
  args: ['--headless=new'],
  headless: false,
});

async function render(query, outFile) {
  const tab = await browser.newPage({ viewport: { width: 960, height: 540 }, deviceScaleFactor: 2 });
  await tab.goto(`${page}?${query}`);
  await tab.evaluate(() => Promise.all([document.fonts.ready, window.NQ.ready]));
  await tab.evaluate(() => window.NQ.play());

  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', outFile],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  const finished = new Promise((ok, fail) => ff.on('close', c => (c === 0 ? ok() : fail(new Error('ffmpeg lỗi ' + c)))));

  let frames = 0;
  for (;;) {
    const { url, done } = await tab.evaluate(fps => {
      window.NQ.step(1 / fps);
      return { url: document.getElementById('cv').toDataURL('image/png'), done: window.NQ.done };
    }, FPS);
    const buf = Buffer.from(url.slice(url.indexOf(',') + 1), 'base64');
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    frames++;
    if (done || frames > FPS * 60) break;
  }
  ff.stdin.end();
  await finished;
  await tab.close();
  console.log(`${outFile}: ${frames} khung (${(frames / FPS).toFixed(1)} giây)`);
}

await render('render', path.join(outDir, 'neoptolemus.mp4'));
await render('render&bg=green', path.join(outDir, 'neoptolemus-greenscreen.mp4'));
await browser.close();
