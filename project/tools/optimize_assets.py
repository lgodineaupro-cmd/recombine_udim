#!/usr/bin/env python3
"""Optimise les images et minifie les SVG dans presentation_brassart/assets/images/logos

Usage: python optimize_assets.py
"""
import os
from pathlib import Path

try:
    from PIL import Image
except Exception:
    raise SystemExit("Pillow requis. Exécutez: python -m pip install pillow")

ROOT = Path(__file__).resolve().parents[1] / 'assets' / 'images' / 'logos'
if not ROOT.exists():
    raise SystemExit(f"Dossier non trouvé: {ROOT}")

def opt_image(p: Path):
    orig = p.stat().st_size
    try:
        img = Image.open(p)
    except Exception as e:
        print(f"Skip (not image): {p} ({e})")
        return
    if img.mode not in ('RGB','RGBA','P'):
        img = img.convert('RGB')
    if p.suffix.lower() in ('.jpg','.jpeg'):
        # recompress JPEG
        tmp = p.with_suffix('.opt.jpg')
        img.save(tmp, format='JPEG', quality=85, optimize=True, progressive=True)
        tmp.replace(p)
    elif p.suffix.lower() == '.png':
        # quantize PNG to reduce colors then save optimized
        tmp = p.with_suffix('.opt.png')
        try:
            q = img.convert('P', palette=Image.ADAPTIVE, colors=256)
            q.save(tmp, format='PNG', optimize=True)
            tmp.replace(p)
        except Exception:
            img.save(tmp, format='PNG', optimize=True)
            tmp.replace(p)
    else:
        print(f"Unsupported image format: {p}")
        return
    new = p.stat().st_size
    print(f"Optimized {p.name}: {orig//1024}KB -> {new//1024}KB")

def minify_svg(p: Path):
    txt = p.read_text(encoding='utf-8')
    orig = len(txt)
    # simple minify: remove XML comments and collapse whitespace between tags
    import re
    txt = re.sub(r'<!--.*?-->', '', txt, flags=re.S)
    txt = re.sub(r'>\s+<', '><', txt)
    txt = txt.strip()
    p.write_text(txt, encoding='utf-8')
    new = len(txt)
    print(f"Minified {p.name}: {orig//1} -> {new//1} bytes")

def main():
    for p in sorted(ROOT.iterdir()):
        if p.suffix.lower() in ('.jpg','.jpeg','.png'):
            opt_image(p)
        elif p.suffix.lower() == '.svg':
            minify_svg(p)
        else:
            print(f"Ignored: {p.name}")

if __name__ == '__main__':
    main()
