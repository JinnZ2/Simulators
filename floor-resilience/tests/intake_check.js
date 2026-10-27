// Drives intake.html in headless Chromium: fill a little, skip a lot, save,
// print the produced site file to stdout. Run by tests/test_intake.py.
const path = require('path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');

(async () => {
  const browser = await chromium.launch(
    process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
  const page = await browser.newPage();
  const file = path.resolve(__dirname, '..', 'floor_resilience', 'intake', 'intake.html');
  await page.goto('file://' + file);
  const reqs = [];
  page.on('request', r => { if (!r.url().startsWith('file:') && !r.url().startsWith('blob:')) reqs.push(r.url()); });
  await page.click('[data-choice=screen] button[data-v=hands_on_trial]');
  await page.click('text=+ Add a person');
  const p = page.locator('#people .card').first();
  await p.locator('[data-k=name]').fill('Marta K.');
  await p.locator('[data-k=years]').fill('20');
  await p.locator('[data-choice=titled] button[data-v=no]').click();
  await p.locator('[data-k=manual]').fill('mill-1, lathe-1');
  await page.click('text=+ Add a person');            // left entirely blank
  await page.click('text=+ Add a repair');
  const r = page.locator('#repairs .card').first();
  await r.locator('[data-k=fixed]').fill('Marta K.');
  await r.locator('[data-k=wrote]').fill('Tom B.');
  await r.locator('[data-choice=ff] button[data-v=yes]').click();
  await r.locator('[data-k=memo]').setInputFiles({ name: 'memo-1.m4a', mimeType: 'audio/mp4', buffer: Buffer.from('x') });
  await page.click('text=+ Add scrap');
  const s = page.locator('#scrap .card').first();
  await s.locator('[data-k=date]').fill('2025-04-02');
  await s.locator('[data-choice=code] button[data-v=calibration_drift]').click();
  await s.locator('[data-k=units]').fill('12');
  await page.click('text=+ Add scrap');                // no date: must be left out
  const sizes = await page.$$eval('button', bs => bs.map(b => b.getBoundingClientRect().height));
  await page.click('text=Save site file');
  const out = await page.inputValue('#out');
  console.log(JSON.stringify({ out, minButton: Math.min(...sizes), external: reqs }));
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
