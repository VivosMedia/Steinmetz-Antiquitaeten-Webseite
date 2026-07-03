#!/usr/bin/env python3
"""Surgically replaces the existing dynamic-loader <script> block (identified
by its comment marker) in each category page with the new lazy-loading
version from make_dynamic.LOADER_TEMPLATE, without touching anything else."""
import re, os, json, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_dynamic import LOADER_TEMPLATE, CATEGORIES

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(root, 'products.json'), encoding='utf-8') as f:
    all_products = json.load(f)

LOADER_BLOCK = re.compile(
    r'\n?  <script>\s*/\* ── dynamic product loader.*?</script>',
    re.DOTALL
)

for cat in CATEGORIES:
    path = os.path.join(root, f'{cat}.html')
    with open(path, encoding='utf-8') as f:
        html = f.read()

    fallback = json.dumps(all_products.get(cat, []), ensure_ascii=False)
    new_loader = LOADER_TEMPLATE.format(cat_json=json.dumps(cat), fallback_json=fallback)

    if LOADER_BLOCK.search(html):
        html = LOADER_BLOCK.sub(new_loader, html, count=1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  ✓ {cat}.html Loader aktualisiert')
    else:
        print(f'  ! {cat}.html: kein bestehender Loader gefunden — übersprungen')

print('\nFertig!')
