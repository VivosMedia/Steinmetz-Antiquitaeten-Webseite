#!/usr/bin/env python3
"""Rewrites products.json to use local optimized image paths.
Products whose image could not be recovered get img=null so the
frontend can render a graceful placeholder instead of a broken image."""
import json, os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(root, 'products.json'), encoding='utf-8') as f:
    data = json.load(f)

with open('/tmp/url_to_local.json', encoding='utf-8') as f:
    url_to_local = json.load(f)

replaced, placeholder = 0, 0
for cat, items in data.items():
    for p in items:
        if p['img'].startswith('http'):
            if p['img'] in url_to_local:
                p['img'] = url_to_local[p['img']]
                replaced += 1
            else:
                p['img'] = None
                placeholder += 1

with open(os.path.join(root, 'products.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'{replaced} Bilder auf lokale Pfade umgestellt, {placeholder} als Platzhalter markiert.')
