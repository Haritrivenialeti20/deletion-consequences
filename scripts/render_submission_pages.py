from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
out=root/'docs/submission-pages'; out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':794,'height':1123}, device_scale_factor=2)
    page.goto((root/'submission.html').as_uri(), wait_until='networkidle')
    pages=page.locator('.page')
    assert pages.count()==5
    for i in range(pages.count()):
        pages.nth(i).screenshot(path=str(out/f'deletion-consequences-page-{i+1}.png'))
    browser.close()
print('rendered 5 submission pages')
