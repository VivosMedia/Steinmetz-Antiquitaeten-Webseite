#!/usr/bin/env python3
"""Update opening hours, phone and email across all HTML pages."""
import os, re

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALL_FILES = [
    'index.html','kommoden.html','lampen.html','dekoration.html','tische.html',
    'sitzmoebel.html','sekretaere.html','schraenke.html','angebote.html','kontakt.html'
]

NEW_HOURS_FOOTER = (
    'Mi – Fr: 15:00 – 18:00 Uhr<br>Sa: 11:00 – 13:00 Uhr<br>'
    'Sonst auf Anfrage<br><br>'
    'Tel: (0)172 450 23 87<br>info@steinmetz-antiquitaeten.de'
)

# ── 1. Fix footer opening-hours block in every file ──────────────────
# Matches the <p> inside the Öffnungszeiten footer-col (any variant)
FOOTER_P = re.compile(
    r'(Di\s*[–-]\s*Fr[^<]*<br[^>]*>.*?Tel:[^<]*(?:<br[^>]*>)?[^<]*)',
    re.DOTALL | re.IGNORECASE
)

# index.html has a placeholder instead of a real phone number
INDEX_P = re.compile(
    r'(Di\s*[–-]\s*Fr[^<]*<br[^>]*>.*?Tel:\s*\[Telefonnummer\])',
    re.DOTALL | re.IGNORECASE
)

for fn in ALL_FILES:
    path = os.path.join(root, fn)
    with open(path, encoding='utf-8') as f:
        html = f.read()

    original = html

    # Fix the index.html placeholder variant first
    html = INDEX_P.sub(NEW_HOURS_FOOTER, html)

    # Fix all standard footer paragraphs
    html = FOOTER_P.sub(NEW_HOURS_FOOTER, html)

    # ── 2. kontakt.html — hours table ────────────────────────────────
    if fn == 'kontakt.html':
        html = html.replace(
            '<tr><td>Dienstag – Freitag</td><td>11:00 – 18:00 Uhr</td></tr>',
            '<tr><td>Mittwoch – Freitag</td><td>15:00 – 18:00 Uhr</td></tr>'
        )
        html = html.replace(
            '<tr><td>Samstag</td><td>10:00 – 16:00 Uhr</td></tr>',
            '<tr><td>Samstag</td><td>11:00 – 13:00 Uhr</td></tr>'
        )
        html = html.replace(
            '<tr><td>Montag &amp; Sonntag</td><td>Geschlossen</td></tr>',
            '<tr><td>Sonst</td><td>Auf Anfrage</td></tr>'
        )
        # phone sub-label
        html = html.replace(
            'Anruf – Di bis Sa während der Öffnungszeiten',
            'Anruf – Mi bis Sa während der Öffnungszeiten'
        )

    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  ✓ {fn}')
    else:
        print(f'  – {fn}: nichts geändert')

print('\nFertig!')
