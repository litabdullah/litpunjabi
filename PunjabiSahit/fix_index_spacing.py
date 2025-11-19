#!/usr/bin/env python3
"""
Fix spacing issues in ALL index pages (listing pages).
Adds padding to page.intro richtext and improves empty state text spacing.
"""

import os
import re
from pathlib import Path

TEMPLATE_DIR = Path(r"C:\src\PunjabiSahit\home\templates\home")

# Spacing fixes specifically for index/listing pages
REPLACEMENTS = [
    # Fix page.intro richtext - add padding
    (r'<div style="font-size: 1rem; line-height: 1\.6; color: var\(--ft-text-secondary\);">\s*\{\{\s*page\.intro\|richtext\s*\}\}',
     r'<div style="font-size: 1rem; line-height: 1.8; color: var(--ft-text-secondary); padding: var(--ft-space-4);">{{ page.intro|richtext }}'),

    (r'<div style="font-size: 1\.125rem; line-height: 1\.6; color: rgba\(38, 42, 51, 0\.9\);">\s*\{\{\s*page\.intro\|richtext\s*\}\}',
     r'<div style="font-size: 1.125rem; line-height: 1.8; color: rgba(38, 42, 51, 0.9); padding: var(--ft-space-4);">{{ page.intro|richtext }}'),

    # Fix empty state headings - replace hardcoded margins with CSS variables and add padding
    (r'<h3 style="font-family: var\(--ft-font-headline\); font-size: 1\.25rem; margin-bottom: 12px; color: var\(--ft-color-slate\);">',
     r'<h3 style="font-family: var(--ft-font-headline); font-size: 1.25rem; margin-bottom: var(--ft-space-4); padding-bottom: var(--ft-space-2); color: var(--ft-color-slate);">'),

    (r'<h3 style="font-family: var\(--ft-font-headline\); font-size: 1\.5rem; margin-bottom: var\(--ft-space-4\); color: var\(--ft-color-slate\);">',
     r'<h3 style="font-family: var(--ft-font-headline); font-size: 1.5rem; margin-bottom: var(--ft-space-6); padding: var(--ft-space-2) 0; color: var(--ft-color-slate);">'),

    # Fix empty state paragraphs - add padding
    (r'<p style="color: var\(--ft-text-tertiary\); margin-bottom: var\(--ft-space-6\);">',
     r'<p style="color: var(--ft-text-tertiary); margin-bottom: var(--ft-space-6); padding: var(--ft-space-2) var(--ft-space-4);">'),

    # Fix description text in event cards and similar
    (r'<p style="font-size: 0\.875rem; line-height: 1\.5; color: var\(--ft-text-secondary\); margin-top: 12px;',
     r'<p style="font-size: 0.875rem; line-height: 1.6; color: var(--ft-text-secondary); margin-top: var(--ft-space-3); padding: var(--ft-space-2) 0;'),

    # Fix phrase translation text
    (r'<p class="ft-phrase-card__translation">',
     r'<p class="ft-phrase-card__translation" style="padding: var(--ft-space-2) 0;">'),

    # Fix section headers in index pages - add more spacing
    (r'<h1 style="font-family: var\(--ft-font-headline\); font-size: 2rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0\.5px; color: var\(--ft-color-slate\);">',
     r'<h1 style="font-family: var(--ft-font-headline); font-size: 2rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: var(--ft-color-slate); padding: var(--ft-space-4) 0;">'),

    # Fix date badge text in event cards
    (r'<p style="font-size: 0\.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0\.5px;">',
     r'<p style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; padding: var(--ft-space-1) 0;">'),

    (r'<p style="font-size: 2\.5rem; font-weight: 700; line-height: 1; margin: 8px 0;">',
     r'<p style="font-size: 2.5rem; font-weight: 700; line-height: 1; margin: var(--ft-space-2) 0; padding: var(--ft-space-2) 0;">'),

    (r'<p style="font-size: 0\.875rem; font-weight: 600;">',
     r'<p style="font-size: 0.875rem; font-weight: 600; padding: var(--ft-space-1) 0;">'),
]

def update_template(file_path):
    """Update a single template file with index page spacing improvements."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        changes_made = 0

        # Apply all replacements
        for pattern, replacement in REPLACEMENTS:
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                changes_made += re.subn(pattern, replacement, content)[1]
                content = new_content

        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] Updated {file_path.name} ({changes_made} spacing improvements)")
            return True
        else:
            print(f"  No spacing changes needed for {file_path.name}")
            return False

    except Exception as e:
        print(f"[ERROR] Error updating {file_path.name}: {e}")
        return False

def main():
    """Update all index page templates with proper text spacing."""
    print("=" * 70)
    print("PUNJABI SAHIT - INDEX PAGES SPACING FIX")
    print("Adding padding to page.intro richtext and empty state messages")
    print("=" * 70)
    print()

    # Target only index pages and home page
    index_patterns = [
        "*_index_page.html",
        "home_page.html"
    ]

    template_files = []
    for pattern in index_patterns:
        template_files.extend(TEMPLATE_DIR.glob(pattern))

    template_files = sorted(set(template_files))

    print(f"Found {len(template_files)} index/main page files to update:")
    for f in template_files:
        print(f"  - {f.name}")
    print()

    updated_count = 0
    for template_file in template_files:
        if update_template(template_file):
            updated_count += 1

    print()
    print("=" * 70)
    print(f"COMPLETE: Added spacing to {updated_count}/{len(template_files)} index pages")
    print("=" * 70)
    print()
    print("[OK] All index pages now have proper text padding!")
    print("[OK] Restart Django server and hard refresh (Ctrl+Shift+R)")

if __name__ == "__main__":
    main()
