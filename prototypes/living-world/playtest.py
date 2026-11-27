from playwright.sync_api import sync_playwright
from pathlib import Path
import json
root=Path(__file__).parent
html=(root/'index.html').read_text().replace('<script src="world.js"></script>','<script>'+ (root/'world.js').read_text()+'</script>')
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content(html)
    page.locator('#map .node').first.wait_for()
    assert page.locator('#map .node').count()==8
    page.wait_for_timeout(3200)
    assert int(page.locator('#stats strong').first.inner_text())>=2
    page.locator('#run').click(); day=page.locator('#stats strong').first.inner_text();page.wait_for_timeout(1700);assert page.locator('#stats strong').first.inner_text()==day
    page.locator('#reset').click();page.screenshot(path=str(root/'01-start.png'),full_page=True)
    page.locator('#scenario').select_option('cutoff');[page.locator('#step').click() for _ in range(3)]
    assert '航線中斷' in page.locator('#events').inner_text()
    assert page.locator('#map polyline[stroke-dasharray="5 8"]').count()==1
    page.screenshot(path=str(root/'02-cutoff.png'),full_page=True)
    page.locator('#mode').select_option('player');page.locator('#system').select_option('g');assert '戰前記錄' in page.locator('#info').inner_text() and '未知' in page.locator('#info').inner_text();assert '航線中斷' not in page.locator('#events').inner_text()
    page.locator('#mode').select_option('observer');page.locator('#scenario').select_option('extreme');[page.locator('#step').click() for _ in range(2)];assert page.locator('#map polyline[stroke-dasharray="5 8"]').count()==2
    page.locator('#scenario').select_option('normal');page.locator('#supply').click();assert '補給交易完成' in page.locator('#toast').inner_text()
    for x in ['b','d','e','f']:
        page.locator('#system').select_option(x);page.locator('#travel').click();page.locator('#step').click();assert '目前位於' in page.locator('#mission').inner_text() or '國防艦隊已接應' in page.locator('#mission').inner_text()
    assert '國防艦隊已接應' in page.locator('#mission').inner_text();assert '從這裡開始，由我們護航' in page.locator('#events').inner_text()
    page.screenshot(path=str(root/'03-escort.png'),full_page=True)
    # The browser prohibits file/localhost navigation. About:blank has an opaque
    # origin: verify the UI's graceful storage denial, not real persistence.
    page.locator('#save').click();assert '不允許本地保存' in page.locator('#toast').inner_text()
    page.locator('#system').select_option('g');page.locator('#travel').click();page.locator('#step').click();assert '歸航完成' in page.locator('#mission').inner_text();assert page.locator('#run').is_disabled();assert page.locator('#step').is_disabled()
    page.screenshot(path=str(root/'04-home.png'),full_page=True)
    page.locator('#load').click();assert '沒有可讀快照' in page.locator('#toast').inner_text() and '歸航完成' in page.locator('#mission').inner_text()
    mobile=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1,is_mobile=True,has_touch=True);mobile.on('pageerror',lambda e:errors.append(str(e)));mobile.set_content(html);mobile.locator('#run').click();assert mobile.locator('#map .node').count()==8;assert mobile.evaluate('document.documentElement.scrollWidth<=innerWidth');mobile.screenshot(path=str(root/'05-mobile.png'),full_page=True)
    assert not errors,errors
    print(json.dumps({'desktop':'PASS','mobile_width_390':'PASS','autonomous_ticks':'PASS','pause':'PASS','cutoff_and_extreme':'PASS','intel_filter':'PASS','supply_and_travel':'PASS','escort_and_ending':'PASS','storage_denied_gracefully':'PASS','actual_persistence':'BLOCKED','page_errors':errors,'screenshots':5},ensure_ascii=False))
    browser.close()
