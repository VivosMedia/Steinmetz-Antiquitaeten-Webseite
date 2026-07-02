#!/usr/bin/env python3
"""Comprehensive SEO optimization for all Steinmetz Antiquitäten pages."""
import os, re

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://steinmetz-antiquitaeten.de'   # update when domain goes live
OG_IMG = f'{BASE}/Gemini%20Generated%20Image%20Wohnzimmer.png'

# ── SEO data per page ────────────────────────────────────────────────
PAGES = {
    'index.html': {
        'title': 'Antiquitäten Hamburg – Steinmetz | Biedermeiermöbel kaufen',
        'desc':  'Steinmetz Antiquitäten Hamburg: Biedermeiermöbel, antike Kommoden, Lampen & Dekoration. Über 30 Jahre Erfahrung. Uhlenhorster Weg 14 – jetzt anfragen!',
        'url':   f'{BASE}/',
    },
    'kommoden.html': {
        'title': 'Antike Kommoden kaufen Hamburg | Biedermeier & Empire – Steinmetz',
        'desc':  'Antike Kommoden in Hamburg: Biedermeier, Empire & Rokoko aus Birke, Ulme, Mahagoni. Über 18 handverlesene Stücke bei Steinmetz Antiquitäten – persönlich anfragen.',
        'url':   f'{BASE}/kommoden.html',
    },
    'lampen.html': {
        'title': 'Antike Lampen & Lüster Hamburg kaufen | Steinmetz Antiquitäten',
        'desc':  'Antike Lampen in Hamburg: Kristallüster, Palmenlampen & Kerzenampeln aus Biedermeier & Empire. 12 einzigartige Stücke bei Steinmetz Antiquitäten.',
        'url':   f'{BASE}/lampen.html',
    },
    'dekoration.html': {
        'title': 'Antike Dekoration Hamburg | Spiegel, Gemälde, Uhren – Steinmetz',
        'desc':  'Antike Dekoration kaufen in Hamburg: Gemälde, Spiegel, Bronzen, Kerzenleuchter & Sammlerstücke. Kuratiert von Jon Steinmetz – Hamburgs Antiquitätenexperte.',
        'url':   f'{BASE}/dekoration.html',
    },
    'tische.html': {
        'title': 'Antike Tische Hamburg kaufen | Biedermeier Konsol- & Esstische',
        'desc':  'Antike Tische in Hamburg: Konsoltische, Sofatische & Esstische aus Biedermeier & Empire. Handverlesene Stücke bei Steinmetz Antiquitäten Hamburg.',
        'url':   f'{BASE}/tische.html',
    },
    'sitzmoebel.html': {
        'title': 'Antike Sitzmöbel Hamburg | Biedermeier Sessel & Sofas kaufen',
        'desc':  'Antike Sitzmöbel in Hamburg: Biedermeier-Sessel, Empire-Sofas & klassizistische Stühle. Einzigartiger Bestand bei Steinmetz Antiquitäten, Hamburg.',
        'url':   f'{BASE}/sitzmoebel.html',
    },
    'sekretaere.html': {
        'title': 'Antike Sekretäre & Bureaus Hamburg kaufen | Biedermeier – Steinmetz',
        'desc':  'Antike Sekretäre kaufen in Hamburg: Biedermeier-Sekretäre aus Birke & Ahorn, Zylinderbureau & Empire-Bureaus. Steinmetz Antiquitäten, Uhlenhorster Weg 14.',
        'url':   f'{BASE}/sekretaere.html',
    },
    'schraenke.html': {
        'title': 'Antike Schränke & Vitrinen Hamburg kaufen | Steinmetz Antiquitäten',
        'desc':  'Antike Schränke in Hamburg: Dielenschränke, Eckvitrinen & Aufsatzvitrinen aus Biedermeier und Barock. 25 Stücke – Steinmetz Antiquitäten Hamburg.',
        'url':   f'{BASE}/schraenke.html',
    },
    'angebote.html': {
        'title': 'Antiquitäten Ausverkauf Hamburg – Alles reduziert | Steinmetz',
        'desc':  'Ausverkauf bei Steinmetz Antiquitäten Hamburg: Biedermeiermöbel & antike Objekte zu stark reduzierten Preisen. Einmalige Gelegenheit – jetzt zugreifen!',
        'url':   f'{BASE}/angebote.html',
    },
    'kontakt.html': {
        'title': 'Kontakt & Öffnungszeiten | Steinmetz Antiquitäten Hamburg',
        'desc':  'Steinmetz Antiquitäten Hamburg – Uhlenhorster Weg 14, 22085 Hamburg. Mi–Fr 15–18 Uhr, Sa 11–13 Uhr. Tel: (0)172 450 23 87 · WhatsApp & E-Mail möglich.',
        'url':   f'{BASE}/kontakt.html',
    },
}

# ── JSON-LD LocalBusiness (only for index.html) ──────────────────────
JSONLD = '''\
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "AntiquesStore",
    "name": "Steinmetz Antiquitäten",
    "description": "Hamburgs Spezialist für Biedermeiermöbel und antike Möbel – persönlich kuratiert von Jon Steinmetz seit über 30 Jahren.",
    "url": "''' + BASE + '''",
    "telephone": "+491724502387",
    "email": "info@steinmetz-antiquitaeten.de",
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
      "https://www.instagram.com/jon_steinmetz_kunsthandel/",
      "https://www.steinmetz-antiquitaeten.de"
    ]
  }
  </script>'''

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
