#!/usr/bin/env python3
"""Comprehensive SEO optimization for all Steinmetz Antiquitäten pages.

Regenerates title/description/canonical/OG/Twitter tags and JSON-LD
(AntiqueStore on index.html, CollectionPage+ItemList on category pages)
from the data below and from public/products.json. Safe to re-run any
time page copy or the product catalog changes.
"""
import os, re, json

root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'public')
BASE = 'https://www.steinmetz-antiquitaeten.de'
OG_IMG = f'{BASE}/Gemini%20Generated%20Image%20Wohnzimmer.jpg'

with open(os.path.join(root, 'products.json'), encoding='utf-8') as f:
    ALL_PRODUCTS = json.load(f)

CATEGORY_LABELS = {
    'kommoden': 'Kommoden', 'lampen': 'Lampen', 'dekoration': 'Dekoration',
    'tische': 'Tische', 'sitzmoebel': 'Sitzmöbel', 'sekretaere': 'Sekretäre',
    'schraenke': 'Schränke', 'angebote': 'Angebote',
}

# ── SEO data per page (title <=60 chars, desc <=155 chars, CTA included) ──
PAGES = {
    'index.html': {
        'title': 'Antiquitäten Hamburg – Steinmetz | Biedermeiermöbel kaufen',
        'desc':  'Steinmetz Antiquitäten Hamburg: Biedermeiermöbel, antike Kommoden, Lampen & Dekoration. Über 30 Jahre Erfahrung. Uhlenhorster Weg 14 – jetzt anfragen!',
        'url':   f'{BASE}/',
    },
    'kommoden.html': {
        'title': 'Antike Kommoden kaufen Hamburg | Biedermeier – Steinmetz',
        'desc':  'Antike Kommoden in Hamburg: Biedermeier, Empire & Rokoko aus Birke, Ulme, Mahagoni. 18 handverlesene Stücke – jetzt persönlich anfragen!',
        'url':   f'{BASE}/kommoden',
        'category': 'kommoden',
    },
    'lampen.html': {
        'title': 'Antike Lampen & Lüster Hamburg kaufen – Steinmetz',
        'desc':  'Antike Lampen in Hamburg: Kristallüster, Palmenlampen & Kerzenampeln aus Biedermeier & Empire. 12 einzigartige Stücke – jetzt anfragen!',
        'url':   f'{BASE}/lampen',
        'category': 'lampen',
    },
    'dekoration.html': {
        'title': 'Antike Dekoration Hamburg | Spiegel & Gemälde – Steinmetz',
        'desc':  'Antike Dekoration in Hamburg: Gemälde, Spiegel, Bronzen & Kerzenleuchter, kuratiert von Jon Steinmetz. Jetzt Sammlerstücke persönlich anfragen!',
        'url':   f'{BASE}/dekoration',
        'category': 'dekoration',
    },
    'tische.html': {
        'title': 'Antike Tische Hamburg kaufen | Biedermeier – Steinmetz',
        'desc':  'Antike Tische in Hamburg: Konsoltische, Sofatische & Esstische aus Biedermeier & Empire. Handverlesene Stücke – jetzt persönlich anfragen!',
        'url':   f'{BASE}/tische',
        'category': 'tische',
    },
    'sitzmoebel.html': {
        'title': 'Antike Sitzmöbel Hamburg | Sessel & Sofas – Steinmetz',
        'desc':  'Antike Sitzmöbel in Hamburg: Biedermeier-Sessel, Empire-Sofas & klassizistische Stühle. Einzigartiger Bestand – jetzt persönlich anfragen!',
        'url':   f'{BASE}/sitzmoebel',
        'category': 'sitzmoebel',
    },
    'sekretaere.html': {
        'title': 'Antike Sekretäre Hamburg kaufen | Biedermeier – Steinmetz',
        'desc':  'Antike Sekretäre in Hamburg: Biedermeier aus Birke & Ahorn, Zylinderbureau & Empire-Bureaus. Uhlenhorster Weg 14 – jetzt persönlich anfragen!',
        'url':   f'{BASE}/sekretaere',
        'category': 'sekretaere',
    },
    'schraenke.html': {
        'title': 'Antike Schränke & Vitrinen Hamburg – Steinmetz',
        'desc':  'Antike Schränke in Hamburg: Dielenschränke, Eckvitrinen & Aufsatzvitrinen, Biedermeier bis Barock. 25 Stücke – jetzt persönlich anfragen!',
        'url':   f'{BASE}/schraenke',
        'category': 'schraenke',
    },
    'angebote.html': {
        'title': 'Antiquitäten Ausverkauf Hamburg – Steinmetz',
        'desc':  'Ausverkauf bei Steinmetz Antiquitäten Hamburg: Biedermeiermöbel & antike Objekte stark reduziert. Einmalige Gelegenheit – jetzt zugreifen!',
        'url':   f'{BASE}/angebote',
        'category': 'angebote',
    },
    'kontakt.html': {
        'title': 'Kontakt & Öffnungszeiten | Steinmetz Antiquitäten',
        'desc':  'Steinmetz Antiquitäten Hamburg – Uhlenhorster Weg 14, 22085 Hamburg. Mi–Fr 15–18 Uhr, Sa 11–13 Uhr. Tel: (0)172 450 23 87 · jetzt anfragen!',
        'url':   f'{BASE}/kontakt',
        'faq': True,
    },
    'impressum.html': {
        'title': 'Impressum | Steinmetz Antiquitäten Hamburg',
        'desc':  'Impressum von Steinmetz Antiquitäten Hamburg. Angaben gemäß § 5 TMG, Kontaktdaten und rechtliche Hinweise.',
        'url':   f'{BASE}/impressum',
    },
}

# ── JSON-LD AntiqueStore (only for index.html) ────────────────────────
JSONLD = '''\
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "AntiqueStore",
    "name": "Steinmetz Antiquitäten",
    "description": "Hamburgs Spezialist für Biedermeiermöbel und antike Möbel – persönlich kuratiert von Jon Steinmetz seit über 30 Jahren.",
    "url": "''' + BASE + '''",
    "telephone": "+491724502387",
    "email": "info@steinmetz-antiquitaeten.de",
    "founder": {
      "@type": "Person",
      "name": "Jon Steinmetz"
    },
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "Uhlenhorster Weg 14",
      "postalCode": "22085",
      "addressLocality": "Hamburg",
      "addressCountry": "DE"
    },
    "geo": {
      "@type": "GeoCoordinates",
      "latitude": 53.5741,
      "longitude": 10.0305
    },
    "openingHoursSpecification": [
      {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Wednesday","Thursday","Friday"],
       "opens": "15:00", "closes": "18:00"},
      {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday",
       "opens": "11:00", "closes": "13:00"}
    ],
    "priceRange": "€€€",
    "image": "''' + OG_IMG + '''",
    "sameAs": [
      "https://www.instagram.com/jon_steinmetz_kunsthandel/"
    ]
  }
  </script>'''


FAQ_ITEMS = [
    ('Kaufen Sie auch Antiquitäten an?',
     'Aktuell kaufen wir nur selten Möbelstücke an, eine Anfrage können Sie uns aber jederzeit stellen – gerne mit Fotos und Maßen, wir melden uns mit einer ehrlichen Einschätzung zurück.'),
    ('Sind die Möbel restauriert?',
     'Das ist unterschiedlich: Viele Stücke bewahren wir bewusst mit ihrer gewachsenen, originalen Patina, andere restaurieren wir fachgerecht für den täglichen Gebrauch. Auf Wunsch restaurieren wir auch einzelne Stücke gezielt für Sie. Den jeweiligen Zustand nennen wir Ihnen immer transparent.'),
    ('Kann ich die Möbel vor Ort besichtigen?',
     'Ja, unsere Ausstellung am Uhlenhorster Weg 14 in Hamburg-Uhlenhorst ist Mi–Fr 15–18 Uhr und Sa 11–13 Uhr geöffnet, außerhalb dieser Zeiten gerne nach Vereinbarung.'),
    ('Liefern Sie die Möbel auch?',
     'Ja, wir organisieren auf Wunsch eine fachgerechte Spedition oder einen persönlichen Liefertermin – sprechen Sie uns einfach darauf an.'),
    ('Was macht Biedermeiermöbel besonders wertvoll?',
     'Biedermeiermöbel überzeugen durch klare, zeitlose Formen, hochwertige Hölzer wie Kirschbaum, Birke und Mahagoni sowie handwerkliche Verarbeitung, die auch nach fast 200 Jahren noch alltagstauglich ist.'),
    ('Kann ich einzelne Stücke reservieren lassen?',
     'Ja, rufen Sie uns an oder schreiben Sie uns per WhatsApp – wir halten Ihnen ein Stück für einen fairen Zeitraum zurück.'),
]


def build_faq_jsonld():
    ld = {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [
            {
                '@type': 'Question',
                'name': q,
                'acceptedAnswer': {'@type': 'Answer', 'text': a},
            }
            for q, a in FAQ_ITEMS
        ],
    }
    body = json.dumps(ld, ensure_ascii=False, indent=2)
    return f'  <script type="application/ld+json">\n{body}\n  </script>'


def build_category_jsonld(cat, data):
    """CollectionPage + ItemList JSON-LD generated from products.json."""
    label = CATEGORY_LABELS.get(cat, cat)
    products = ALL_PRODUCTS.get(cat, [])

    items = []
    for i, p in enumerate(products):
        item = {
            '@type': 'Product',
            'name': p.get('name') or label,
            'url': f'{BASE}/produkt?cat={cat}&id={p.get("id", "")}',
            'itemCondition': 'https://schema.org/UsedCondition',
            'brand': {'@type': 'Organization', 'name': 'Steinmetz Antiquitäten'},
        }
        if p.get('img'):
            item['image'] = f'{BASE}/{p["img"]}'
        if p.get('desc'):
            item['description'] = p['desc']
        items.append({'@type': 'ListItem', 'position': i + 1, 'item': item})

    ld = {
        '@context': 'https://schema.org',
        '@type': 'CollectionPage',
        'name': data['title'],
        'url': data['url'],
        'isPartOf': {'@type': 'WebSite', 'name': 'Steinmetz Antiquitäten', 'url': f'{BASE}/'},
        'about': {'@type': 'Thing', 'name': label},
        'mainEntity': {
            '@type': 'ItemList',
            'name': f'{label} – Steinmetz Antiquitäten',
            'numberOfItems': len(items),
            'itemListElement': items,
        },
    }
    body = json.dumps(ld, ensure_ascii=False, indent=2)
    return f'  <script type="application/ld+json">\n{body}\n  </script>'


def build_head_tags(page, data):
    url   = data['url']
    title = data['title']
    desc  = data['desc']
    is_index = (page == 'index.html')

    lines = []

    # Robots (index all pages except admin)
    lines.append('  <meta name="robots" content="index, follow">')

    # Canonical
    lines.append(f'  <link rel="canonical" href="{url}">')

    # Open Graph
    lines.append(f'  <meta property="og:type" content="{"website" if is_index else "article"}">')
    lines.append(f'  <meta property="og:locale" content="de_DE">')
    lines.append(f'  <meta property="og:site_name" content="Steinmetz Antiquitäten Hamburg">')
    lines.append(f'  <meta property="og:url" content="{url}">')
    lines.append(f'  <meta property="og:title" content="{title}">')
    lines.append(f'  <meta property="og:description" content="{desc}">')
    lines.append(f'  <meta property="og:image" content="{OG_IMG}">')

    # Twitter Card
    lines.append('  <meta name="twitter:card" content="summary_large_image">')
    lines.append(f'  <meta name="twitter:title" content="{title}">')
    lines.append(f'  <meta name="twitter:description" content="{desc}">')
    lines.append(f'  <meta name="twitter:image" content="{OG_IMG}">')

    if is_index:
        lines.append(JSONLD)
    elif 'category' in data:
        lines.append(build_category_jsonld(data['category'], data))
    if data.get('faq'):
        lines.append(build_faq_jsonld())

    return '\n'.join(lines)

# ── Process each file ────────────────────────────────────────────────
for page, data in PAGES.items():
    path = os.path.join(root, page)
    if not os.path.exists(path):
        print(f'  SKIP {page}')
        continue

    with open(path, encoding='utf-8') as f:
        html = f.read()

    # 1. Replace title
    html = re.sub(r'<title>.*?</title>', f'<title>{data["title"]}</title>', html, flags=re.DOTALL)

    # 2. Replace meta description
    html = re.sub(
        r'<meta\s+name="description"\s+content="[^"]*"\s*/?>',
        f'<meta name="description" content="{data["desc"]}" />',
        html
    )

    # 3. Remove any existing OG/canonical/robots/ld+json tags (avoid duplication)
    html = re.sub(r'\s*<meta\s+(?:property="og:[^"]*"|name="robots"|name="twitter:[^"]*")[^>]*/?>','', html)
    html = re.sub(r'\s*<link\s+rel="canonical"[^>]*/?>','', html)
    html = re.sub(r'\s*<script\s+type="application/ld\+json">.*?</script>','', html, flags=re.DOTALL)

    # 4. Inject new tags before </head>
    new_tags = build_head_tags(page, data)
    html = html.replace('</head>', f'{new_tags}\n</head>', 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  ✓ {page}')

print('\nSEO-Optimierung abgeschlossen!')
