#!/usr/bin/env python3
"""Replaces the static product grid in each category page with dynamic loading from products.json."""
import re, json, os

CATEGORIES = ['kommoden','lampen','dekoration','tische','sitzmoebel','sekretaere','schraenke','angebote']
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(root, 'products.json'), encoding='utf-8') as f:
    all_products = json.load(f)

LOADER_TEMPLATE = '''
  <script>
    /* ── dynamic product loader ── */
    (function() {{
      const CAT      = {cat_json};
      const FALLBACK = {fallback_json};

      function esc(s) {{
        return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
      }}

      function render(items) {{
        const grid    = document.getElementById('productGrid');
        const counter = document.querySelector('.product-count');
        if (counter) counter.textContent = items.length + ' Objekte';
        if (!items.length) {{
          grid.innerHTML = '<p style="padding:40px;color:#8B7355;text-align:center;">Keine Produkte vorhanden.</p>';
          return;
        }}
        grid.innerHTML = items.map(function(p, i) {{
          var d = ['','delay-1','delay-2'][i % 3];
          return '<article class="product-card fade-up' + (d?' '+d:'') + '">'
            + '<div class="product-card-img">'
            + '<div class="product-card-img-inner" style="background-image:url(\\'' + esc(p.img) + '\\')"></div>'
            + '</div>'
            + '<div class="product-card-info">'
            + '<h3 class="product-card-name">' + esc(p.name) + '</h3>'
            + '<p class="product-card-desc">' + esc(p.desc) + '</p>'
            + '</div></article>';
        }}).join('');
        var obs = new IntersectionObserver(function(entries) {{
          entries.forEach(function(e) {{ if (e.isIntersecting) {{ e.target.classList.add('visible'); obs.unobserve(e.target); }} }});
        }}, {{ threshold: 0.08, rootMargin: '0px 0px -20px 0px' }});
        grid.querySelectorAll('.fade-up').forEach(function(el) {{ obs.observe(el); }});
      }}

      fetch('./products.json?' + Date.now())
        .then(function(r) {{ return r.ok ? r.json() : Promise.reject(); }})
        .then(function(data) {{ render(Array.isArray(data[CAT]) ? data[CAT] : FALLBACK); }})
        .catch(function() {{ render(FALLBACK); }});
    }})();
  </script>'''

STATIC_SCRIPT = re.compile(
    r'(<script>\s*const navToggle.*?observer\.observe\(el\)\);\s*\}.*?</script>)',
    re.DOTALL
)

for cat in CATEGORIES:
    path = os.path.join(root, f'{cat}.html')
    with open(path, encoding='utf-8') as f:
        html = f.read()

    # 1. Replace all <article> product-cards with empty grid placeholder
    html = re.sub(
        r'(<div class="product-grid"[^>]*>)\s*(<article.*?</article>\s*)+',
        r'\1\n      ',
        html, flags=re.DOTALL
    )
    # Add id="productGrid" to the product-grid div if not present
    html = html.replace(
        '<div class="product-grid">',
        '<div class="product-grid" id="productGrid">'
    )

    # 2. Build loader script with fallback data
    fallback = json.dumps(all_products.get(cat, []), ensure_ascii=False)
    loader = LOADER_TEMPLATE.format(
        cat_json=json.dumps(cat),
        fallback_json=fallback
    )

    # 3. Inject loader before </body> (replacing or appending)
    if STATIC_SCRIPT.search(html):
        # Keep the nav toggle from existing script; append our loader separately
        # Actually replace the whole script block and add nav+loader combined
        def replace_script(m):
            existing = m.group(1)
            # Strip product-related observer if it exists and return nav+loader
            nav_part = re.search(r'(const navToggle.*?navLinks\.classList\.toggle\(\'open\'\)\);)', existing, re.DOTALL)
            nav = nav_part.group(1) if nav_part else ''
            hero_part = re.search(r"(setTimeout\(\(\) => document\.querySelector\('.cat-hero-bg'\).*?\), 100\);)", existing, re.DOTALL)
            hero = hero_part.group(1) if hero_part else ''
            return f'  <script>\n    {nav}\n    {hero}\n  </script>{loader}'
        html = STATIC_SCRIPT.sub(replace_script, html)
    else:
        html = html.replace('</body>', loader + '\n</body>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  ✓ {cat}.html aktualisiert')

print('\nFertig!')
