#!/usr/bin/env python3
"""Build the game from src/game.template.html + assets/.

  python3 tools/build.py            -> index.html  (full page for GitHub Pages: share tags, icon, viewport)
  python3 tools/build.py --bare OUT -> OUT          (page body only, for publishing as a claude.ai artifact)

Every PNG under assets/ is inlined, so index.html runs on its own.
"""
import base64, json, pathlib, sys

root = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://amaddaofficial.github.io/alligator/"   # GitHub Pages address (owner.github.io/repo/)
TITLE = "악어악어 점령"
DESC = "아이가 연필로 그린 악어들이 토성을 지키는 타워디펜스. 폰은 옆으로 돌려서."

HEAD = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, maximum-scale=1, user-scalable=no">
<meta name="description" content="{DESC}">
<meta name="theme-color" content="#fbfaf5">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="{TITLE}">
<link rel="icon" type="image/png" href="icon.png">
<link rel="manifest" href="manifest.json">
<link rel="apple-touch-icon" href="icon.png">
<!-- 링크를 보낼 때 뜨는 제목·그림 (카카오톡, 문자, 슬랙 등) -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="{TITLE}">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{SITE}">
<meta property="og:image" content="{SITE}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="연필로 그린 악어와 개구리, 손글씨 제목 악어 점령">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="{SITE}og.png">
<style>html,body{{margin:0;height:100%;background:#fbfaf5}}</style>
</head>
<body>
"""
FOOT = "\n</body>\n</html>\n"

def sprites():
    spr = {}
    for sub in ("assets/sprites", "assets/bosses"):
        for f in sorted((root / sub).glob("*.png")):
            spr[f.stem] = "data:image/png;base64," + base64.b64encode(f.read_bytes()).decode()
    return spr

def build(bare: bool) -> str:
    t = (root / "src/game.template.html").read_text(encoding="utf-8")
    body = t.replace("__SPRITES__", json.dumps(sprites(), ensure_ascii=False))
    if bare:
        return body
    # the template opens with <title>/<meta>/<link>/<style>: on Pages those belong in <head>
    cut = body.index('<div id="frame">')
    head_part = body[:cut].replace('<meta name="claude:viewport-fit-sides" content="cover">', "")
    return HEAD.replace("</head>", head_part + "</head>") + body[cut:] + FOOT

if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--bare":
        out = pathlib.Path(sys.argv[2]); out.write_text(build(True), encoding="utf-8")
    else:
        out = root / "index.html"; out.write_text(build(False), encoding="utf-8")
    print(f"{out}: {out.stat().st_size // 1024} KB")
