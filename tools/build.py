#!/usr/bin/env python3
"""Build index.html: inlines every PNG under assets/ into src/game.template.html at the __SPRITES__ marker.
Run:  python3 tools/build.py
"""
import base64, json, os, pathlib
root=pathlib.Path(__file__).resolve().parent.parent
spr={}
for sub in ('assets/sprites','assets/bosses'):
    for f in sorted((root/sub).glob('*.png')):
        spr[f.stem]='data:image/png;base64,'+base64.b64encode(f.read_bytes()).decode()
t=(root/'src/game.template.html').read_text(encoding='utf-8')
out=t.replace('__SPRITES__',json.dumps(spr,ensure_ascii=False))
(root/'index.html').write_text(out,encoding='utf-8')
print(f'index.html written: {len(out)//1024} KB, {len(spr)} sprites')
