const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 1024 });
  await page.goto('https://web-lovat-eight-11.vercel.app', { waitUntil: 'networkidle0' });
  await page.screenshot({ path: '/home/luca/.gemini/antigravity-cli/brain/0e734859-4349-45a7-aba8-5ef03739bd06/screenshot.png', fullPage: true });
  await browser.close();
  console.log('Screenshot saved!');
})();
