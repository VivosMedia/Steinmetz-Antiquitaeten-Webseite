#!/usr/bin/env python3
"""Downloads recoverable images via Wayback Machine, optimizes them
(resize + compress to JPEG), and rewrites products.json + HTML hero
references to use the local optimized copies. Missing images get a
placeholder flag so the frontend can show a graceful fallback.
"""
import os, re, json, time, hashlib, urllib.request, urllib.error

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(root, 'images', 'products')
os.makedirs(IMG_DIR, exist_ok=True)

from PIL import Image
import io

MAX_WIDTH = 1400   # covers both hero (full width) and retina grid thumbs
JPEG_QUALITY = 76

with open('/tmp/wayback_available.json', encoding='utf-8') as f:
    available = dict(json.load(f))   # {original_url: wayback_url}

with open('/tmp/wayback_missing.txt', encoding='utf-8') as f:
    missing = set(l.strip() for l in f if l.strip())

# Also fold in the extra hero URL checked separately
EXTRA = {
    'https://www.steinmetz-antiquitaeten.de/wp-content/uploads/2014/11/P1040460.jpg':
    'http://web.archive.org/web/20250121124431/https://www.steinmetz-antiquitaeten.de/wp-content/uploads/2014/11/P1040460.jpg'
}
available.update(EXTRA)

def local_filename(url):
    h = hashlib.md5(url.encode()).hexdigest()[:12]
    base = os.path.basename(url).split('?')[0]
    name = re.sub(r'[^a-zA-Z0-9._-]', '_', base)
    stem = os.path.splitext(name)[0]
    return f'{stem}-{h}.jpg'

url_to_local = {}
failed = []

print(f'Lade und optimiere {len(available)} Bilder...\n')
for i, (orig_url, wb_url) in enumerate(available.items(), 1):
    local_name = local_filename(orig_url)
    local_path = os.path.join(IMG_DIR, local_name)
    url_to_local[orig_url] = f'images/products/{local_name}'

    if os.path.exists(local_path):
        continue  # already done in a previous run

    # Force raw-content mode (no Wayback toolbar wrapper) via the "if_" flag
    raw_wb_url = re.sub(r'(/web/\d+)(/)', r'\1if_\2', wb_url, count=1)

    try:
        req = urllib.request.Request(raw_wb_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=25) as r:
            raw = r.read()
        img = Image.open(io.BytesIO(raw))
        img = img.convert('RGB')
        if img.width > MAX_WIDTH:
            ratio = MAX_WIDTH / img.width
            img = img.resize((MAX_WIDTH, int(img.height * ratio)), Image.LANCZOS)
        img.save(local_path, 'JPEG', quality=JPEG_QUALITY, optimize=True)
    except Exception as e:
        failed.append((orig_url, str(e)))
        continue
    finally:
        time.sleep(2.5)  # be gentle with archive.org rate limits

    if i % 10 == 0:
        print(f'  {i}/{len(available)} verarbeitet...')

print(f'\nFertig. {len(url_to_local) - len(failed)} erfolgreich, {len(failed)} fehlgeschlagen.')
if failed:
    for u, e in failed:
        print(f'  FEHLER: {u} -> {e}')

# Save the URL mapping for the next script step
with open('/tmp/url_to_local.json', 'w', encoding='utf-8') as f:
    json.dump(url_to_local, f, ensure_ascii=False, indent=2)
with open('/tmp/still_missing.json', 'w', encoding='utf-8') as f:
    json.dump(sorted(missing), f, ensure_ascii=False, indent=2)

print(f'\nMapping gespeichert: /tmp/url_to_local.json ({len(url_to_local)} Einträge)')
print(f'Weiterhin fehlend: {len(missing)} Bilder (Platzhalter wird verwendet)')
