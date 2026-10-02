"""Build the CDN theme and the local embedded theme from the same CSS."""
from pathlib import Path
import base64, json

OUT = Path(__file__).resolve().parent
theme = json.loads((OUT/'theme-settings.json').read_text(encoding='utf-8'))
css = (OUT/'theme.css').read_text(encoding='utf-8')
manifest = json.loads((OUT/'asset-manifest.json').read_text(encoding='utf-8'))
assert 'data:' not in css and '@@' not in css
theme['custom_css'] = css
(OUT/'Dream-夏日像素明信片-CDN.json').write_text(json.dumps(theme,ensure_ascii=False,indent=2),encoding='utf-8')
embedded = css
for row in manifest:
    path = OUT/'assets'/row['file']
    mime = {'.svg':'image/svg+xml','.png':'image/png','.webp':'image/webp','.woff2':'font/woff2'}[path.suffix]
    assert row['cdn'] in embedded, row['file']
    uri = 'data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode()
    embedded = embedded.replace(row['cdn'],uri)
theme['custom_css'] = embedded
(OUT.parent/'Dream-夏日像素明信片.json').write_text(json.dumps(theme,ensure_ascii=False,indent=2),encoding='utf-8')
print('Built CDN theme and embedded theme.')
