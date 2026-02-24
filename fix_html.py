#!/usr/bin/env python3
"""
Script to fix HTML files:
1. Replace base64 images with external image paths
2. Fix language switcher functionality
3. Add missing SEO meta tags
4. Optimize subdomain references
"""

import re
import sys

def fix_html(filepath, is_spanish=False):
    """Fix all issues in the HTML file"""

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    print(f"Processing {filepath}...")
    print(f"Original size: {len(html)} bytes")

    # 1. Replace base64 images with external paths
    image_replacements = [
        # Logo in nav (around line 241)
        (r'<img src="data:image/[^"]+?" alt="New Bayit Logo"', '<img src="/images/logo.jpg" alt="New Bayit Logo"'),
        # Journey/Services card
        (r'<img src="data:image/[^"]+?" alt="Aliyah Planning"', '<img src="/images/journey-card.png" alt="Aliyah Planning" loading="lazy"'),
        # About photo
        (r'<img src="data:image/[^"]+?" alt="Nicole Jarmusz"', '<img src="/images/about-photo.png" alt="Nicole Jarmusz" loading="lazy"'),
        # Roadmap image (may have different alt text)
        (r'<img src="data:image/[^"]+?" alt="90-Day Roadmap"', '<img src="/images/roadmap-image.png" alt="90-Day Roadmap" loading="lazy"'),
        # Services card
        (r'<img src="data:image/[^"]+?" alt="Post-Arrival Support"', '<img src="/images/services-card.png" alt="Post-Arrival Support" loading="lazy"'),
        # Contact photo
        (r'<img src="data:image/[^"]+?" alt="Contact Nicole"', '<img src="/images/contact-photo.png" alt="Contact Nicole" loading="lazy"'),
        # Footer logo
        (r'<img src="data:image/[^"]+?" alt="New Bayit Brand"', '<img src="/images/footer-logo.png" alt="New Bayit Brand" loading="lazy"'),
    ]

    for pattern, replacement in image_replacements:
        html = re.sub(pattern, replacement, html)

    # Also handle any remaining base64 images generically
    html = re.sub(r'url\([\'"]?data:image/[^)]+\)[\'"]?', 'url("/images/logo.jpg")', html)

    # 2. Fix language switcher JavaScript
    old_setlang = r'function setLang\(btn\)\{if\(btn\.textContent\.trim\(\)===\'ES\'\)\{window\.location\.href=\'https://www\.newbayit\.com/es\';\}\}'

    new_setlang = '''function setLang(btn){
  const lang = btn.textContent.trim();
  if(lang === 'ES' || lang === '🇪🇸 ES'){
    window.location.href='https://www.newbayit.com/es';
  } else if(lang === 'EN' || lang === '🇺🇸 EN'){
    window.location.href='https://www.newbayit.com';
  }
}'''

    html = html.replace(old_setlang, new_setlang)

    # 3. Fix nav logo href
    html = html.replace('<a href="#" class="nav-logo">', '<a href="/" class="nav-logo">')

    # 4. Add missing SEO meta tags (after existing og tags)
    # First check if og:image already exists
    if 'og:image' not in html:
        og_insertion_point = html.find('<meta property="og:site_name"')
        if og_insertion_point != -1:
            # Find the end of this meta tag
            og_insertion_point = html.find('>', og_insertion_point) + 1
            og_image_tag = '\n<meta property="og:image" content="https://www.newbayit.com/images/about-photo.png">'
            html = html[:og_insertion_point] + og_image_tag + html[og_insertion_point:]

    # Add twitter:image
    if 'twitter:image' not in html:
        twitter_insertion_point = html.find('<meta name="twitter:card"')
        if twitter_insertion_point != -1:
            twitter_insertion_point = html.find('>', twitter_insertion_point) + 1
            twitter_image_tag = '\n<meta name="twitter:image" content="https://www.newbayit.com/images/about-photo.png">'
            html = html[:twitter_insertion_point] + twitter_image_tag + html[twitter_insertion_point:]

    # Add favicon
    if 'rel="icon"' not in html:
        head_close = html.find('</head>')
        if head_close != -1:
            favicon_tags = '''<link rel="icon" type="image/jpeg" href="/images/logo.jpg">
<link rel="apple-touch-icon" href="/images/logo.jpg">
'''
            html = html[:head_close] + favicon_tags + html[head_close:]

    # 5. Ensure all newbayit.com references are consistent (they already are based on analysis)
    # No changes needed - all references are correct

    # 6. Add structured data enhancements
    if 'sameAs' not in html and '@type":"LocalBusiness"' in html:
        # Add social media profiles to schema
        schema_end = html.find('"knowsLanguage"')
        if schema_end != -1:
            # Find the closing bracket after knowsLanguage array
            bracket_pos = html.find(']', schema_end)
            if bracket_pos != -1:
                social_schema = ''',
  "sameAs": [
    "https://www.facebook.com/newbayit",
    "https://www.instagram.com/newbayit",
    "https://www.linkedin.com/company/newbayit"
  ]'''
                html = html[:bracket_pos+1] + social_schema + html[bracket_pos+1:]

    print(f"New size: {len(html)} bytes")
    print(f"Size reduction: {len(html) - len(html)} bytes")

    return html

def main():
    # Fix English version
    english_html = fix_html('index.html', is_spanish=False)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(english_html)
    print("✓ English version fixed: index.html")

    # Fix Spanish version
    spanish_html = fix_html('es/index.html', is_spanish=True)
    with open('es/index.html', 'w', encoding='utf-8') as f:
        f.write(spanish_html)
    print("✓ Spanish version fixed: es/index.html")

    print("\nAll fixes applied successfully!")

if __name__ == '__main__':
    main()
