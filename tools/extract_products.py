#!/usr/bin/env python3
"""Extracts product data from all category HTML files and writes products.json."""
import re, json, os, uuid

CATEGORIES = ['kommoden','lampen','dekoration','tische','sitzmoebel','sekretaere','schraenke','angebote']
HTML_ENTITIES = {'&amp;':'&','&uuml;':'ü','&auml;':'ä','&ouml;':'ö','&Uuml;':'Ü','&Auml;':'Ä',
                 '&Ouml;':'Ö','&szlig;':'ß','&ndash;':'–','&mdash;':'—','&nbsp;':' ','&lt;':'<','&gt;':'>'}

def clean(s):
    for e, r in HTML_ENTITIES.items():
        s = s.replace(e, r)
    return ' '.join(s.split())

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = {}

for cat in CATEGORIES:
    path = os.path.join(root, f'{cat}.html')
    if not os.path.exists(path):
        print(f'  SKIP {cat}.html (nicht gefunden)')
        data[cat] = []
        continue
    with open(path, encoding='utf-8') as f:
        html = f.read()
    cards = re.findall(r'<article class="product-card[^>]*>.*?</article>', html, re.DOTALL)
    products = []
    for card in cards:
        img  = re.search(r"background-image:\s*url\('([^']+)'\)", card)
        name = re.search(r'class="product-card-name">(.*?)</h3>', card, re.DOTALL)
        desc = re.search(r'class="product-card-desc">(.*?)</p>', card, re.DOTALL)
        if img and name:
            products.append({
                'id':   str(uuid.uuid4())[:8],
                'img':  img.group(1),
                'name': clean(name.group(1)),
                'desc': clean(desc.group(1)) if desc else ''
            })
    data[cat] = products
    print(f'  {cat}: {len(products)} Produkte')

out = os.path.join(root, 'products.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f'\n✓ {out} erstellt')
