import hashlib, json, re
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent
current = json.loads((OUT.parent/'Dream-夏日像素明信片.json').read_text(encoding='utf-8'))
before = json.loads((OUT/'before-fix.json').read_text(encoding='utf-8'))
cdn = json.loads((OUT/'Dream-夏日像素明信片-CDN.json').read_text(encoding='utf-8'))
assert {k:v for k,v in current.items() if k != 'custom_css'} == {k:v for k,v in before.items() if k != 'custom_css'}
assert 'data:' not in cdn['custom_css']
assert '@@' not in cdn['custom_css']
manifest = json.loads((OUT/'asset-manifest.json').read_text(encoding='utf-8'))
assert len(manifest) == len({x['file'] for x in manifest}) == 22
for row in manifest:
    raw = (OUT/'assets'/row['file']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == row['sha256']
    if row['file'].endswith('.svg'):
        import xml.etree.ElementTree as ET
        ET.fromstring(raw)

markup = '''<!doctype html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box}body{margin:0;background:white}.plugin{font-family:sans-serif}
.plugin button{background:rgb(240,220,210);border:0;border-radius:12px;box-shadow:none;color:rgb(80,60,50);padding:10px}
.plugin input{background:white;border:1px solid rgb(180,160,150);border-radius:8px}
#chat{width:100%;display:flex;flex-direction:column}.mes{display:grid}.mes_text iframe{display:block;width:100%;height:100px;border:0}
</style></head><body><div class="plugin popup"><button id="plugin">插件按钮</button><input id="plugin-input"></div>
<div id="top-settings-holder"><div class="drawer"><div class="drawer-content"><div id="extensions_settings" class="plugin"><button id="extension">脚本工具</button><button class="menu_button" id="extension-native-class">插件原生类</button></div></div></div></div>
<div id="right-nav-panel"><button class="menu_button" id="native">原生按钮</button></div>
<div id="chat"><div class="mes" is_user="false"><div class="mesAvatarWrapper"><div class="avatar"><img></div></div><div class="mes_block"><div class="ch_name"><span>角色</span></div><div class="mes_text"><p>正文内容</p><div class="plugin"><button id="frontend-button">前端按钮</button></div><iframe srcdoc="<body style='margin:0;background:#eee'>嵌入前端</body>"></iframe></div></div></div></div>
</body></html>'''

results = []
with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge')
    page = browser.new_page()
    # All browser checks use embedded assets, no network dependency.
    page.route('http**/*', lambda route: route.abort())
    for width in [1440,390,430]:
        page.set_viewport_size(dict(width=width,height=900))
        pair = {}
        for label, theme in [('before',before),('after',current)]:
            page.set_content(markup)
            page.add_style_tag(content=theme['custom_css'])
            page.evaluate('document.fonts.ready')
            pair[label] = page.evaluate('''() => {
              const styles = {};
              for(const id of ['plugin','plugin-input','extension','extension-native-class','frontend-button','native']) {
                const s = getComputedStyle(document.getElementById(id));
                styles[id] = {background:s.backgroundColor,radius:s.borderRadius,shadow:s.boxShadow,border:s.borderWidth};
              }
              const text=document.querySelector('.mes_text'),s=getComputedStyle(text);
              return {styles,frameWidth:text.querySelector('iframe').getBoundingClientRect().width,margin:s.margin,padding:s.padding};
            }''')
            if label == 'after':
                page.screenshot(path=str(OUT/f'preview-{width}.png'),full_page=True)
        for id in ['plugin','extension','extension-native-class','frontend-button']:
            assert pair['after']['styles'][id]['background']=='rgb(240, 220, 210)',(width,id,pair['after'])
            assert pair['after']['styles'][id]['radius']=='12px'
        assert pair['after']['frameWidth'] > pair['before']['frameWidth'],pair
        results.append(dict(width=width,**pair))
    browser.close()
(OUT/'validation.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([dict(width=x['width'],before=x['before']['frameWidth'],after=x['after']['frameWidth']) for x in results]))
