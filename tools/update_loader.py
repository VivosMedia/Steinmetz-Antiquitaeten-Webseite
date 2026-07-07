#!/usr/bin/env python3
"""Removes ALL existing dynamic-loader <script> blocks (there were duplicates
from earlier runs) and inserts exactly one fresh copy from
make_dynamic.LOADER_TEMPLATE before </body>, without touching anything else."""
import re, os, json, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_dynamic import LOADER_TEMPLATE, CATEGORIES

root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'public')

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

    n_found = len(LOADER_BLOCK.findall(html))
    html = LOADER_BLOCK.sub('', html)  # alle bisherigen Kopien entfernen

    fallback = json.dumps(all_products.get(cat, []), ensure_ascii=False)
    new_loader = LOADER_TEMPLATE.format(cat_json=json.dumps(cat), fallback_json=fallback)
    html = html.replace('</body>', new_loader + '\n</body>', 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  ✓ {cat}.html: {n_found} alte Kopie(n) entfernt, 1 neue eingefügt')

print('\nFertig!')
