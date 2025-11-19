#!/usr/bin/env python3
"""
Update CSS class definitions in <style> blocks to add more padding.
Makes card classes more minimalistic with proper spacing.
"""

import os
import re
from pathlib import Path

TEMPLATE_DIR = Path(r"C:\src\PunjabiSahit\home\templates\home")

# CSS class definition updates for better padding
CSS_REPLACEMENTS = [
    # Dictionary entry cards
    (r'\.ft-dictionary-entry \{\s*display: block;\s*padding: var\(--ft-space-xl\) var\(--ft-space-2xl\);',
     r'.ft-dictionary-entry { display: block; padding: var(--ft-space-4xl) var(--ft-space-5xl);'),

    # Author cards
    (r'\.ft-author-card \{\s*background-color: var\(--ft-bg-card\);\s*border: 1px solid rgba\(13, 118, 128, 0\.15\);\s*padding: var\(--ft-space-2xl\);',
     r'.ft-author-card { background-color: var(--ft-bg-card); border: 1px solid rgba(13, 118, 128, 0.15); padding: var(--ft-space-4xl);'),

    # Book cards info section
    (r'\.ft-book-card:hover \.ft-book-cover img \{',
     r'.ft-book-card:hover .ft-book-cover img {'),

    # Event cards
    (r'\.ft-event-card \{\s*display: block;\s*background-color: var\(--ft-bg-card\);\s*border: 1px solid rgba\(13, 118, 128, 0\.15\);\s*padding: var\(--ft-space-2xl\);',
     r'.ft-event-card { display: block; background-color: var(--ft-bg-card); border: 1px solid rgba(13, 118, 128, 0.15); padding: var(--ft-space-4xl);'),

    # Phrase cards
    (r'\.ft-phrase-card \{\s*display: block;\s*padding: var\(--ft-space-2xl\);',
     r'.ft-phrase-card { display: block; padding: var(--ft-space-4xl);'),

    # Filter bars
    (r'\.ft-filter-bar \{\s*position: sticky;\s*top: 60px;\s*z-index: 30;\s*background-color: var\(--ft-bg-card\);\s*border: 1px solid rgba\(13, 118, 128, 0\.15\);\s*padding: var\(--ft-space-xl\);',
     r'.ft-filter-bar { position: sticky; top: 60px; z-index: 30; background-color: var(--ft-bg-card); border: 1px solid rgba(13, 118, 128, 0.15); padding: var(--ft-space-3xl);'),

    # Dictionary entry headword - add more bottom spacing
    (r'\.ft-dictionary-entry__headword \{\s*font-family: var\(--ft-font-gurmukhi\);\s*font-size: 2rem;\s*font-weight: 700;\s*color: var\(--ft-color-slate\);\s*margin-bottom: var\(--ft-space-xs\);',
     r'.ft-dictionary-entry__headword { font-family: var(--ft-font-gurmukhi); font-size: 2rem; font-weight: 700; color: var(--ft-color-slate); margin-bottom: var(--ft-space-lg); padding-bottom: var(--ft-space-md);'),

    # Dictionary entry roman
    (r'\.ft-dictionary-entry__roman \{\s*font-family: var\(--ft-font-body\);\s*font-size: 1rem;\s*font-weight: 500;\s*color: var\(--ft-text-tertiary\);\s*margin-bottom: var\(--ft-space-sm\);',
     r'.ft-dictionary-entry__roman { font-family: var(--ft-font-body); font-size: 1rem; font-weight: 500; color: var(--ft-text-tertiary); margin-bottom: var(--ft-space-lg); padding: var(--ft-space-sm) 0;'),

    # Dictionary entry definition
    (r'\.ft-dictionary-entry__definition \{\s*font-size: 0\.9375rem;\s*line-height: 1\.5;\s*color: var\(--ft-text-secondary\);\s*margin-bottom: var\(--ft-space-md\);',
     r'.ft-dictionary-entry__definition { font-size: 0.9375rem; line-height: 1.7; color: var(--ft-text-secondary); margin-bottom: var(--ft-space-xl); padding: var(--ft-space-md) 0;'),

    # Author name Gurmukhi
    (r'\.ft-author-name-gurmukhi \{\s*font-family: var\(--ft-font-gurmukhi\);\s*font-size: 1\.5rem;\s*font-weight: 700;\s*color: var\(--ft-color-slate\);\s*margin-bottom: 4px;',
     r'.ft-author-name-gurmukhi { font-family: var(--ft-font-gurmukhi); font-size: 1.5rem; font-weight: 700; color: var(--ft-color-slate); margin-bottom: var(--ft-space-md); padding: var(--ft-space-sm) 0;'),

    # Author bio
    (r'\.ft-author-bio \{\s*font-size: 0\.875rem;\s*line-height: 1\.5;\s*color: var\(--ft-text-secondary\);\s*margin-bottom: var\(--ft-space-lg\);',
     r'.ft-author-bio { font-size: 0.875rem; line-height: 1.7; color: var(--ft-text-secondary); margin-bottom: var(--ft-space-2xl); padding: var(--ft-space-lg) var(--ft-space-md);'),

    # Phrase card Gurmukhi
    (r'\.ft-phrase-card__gurmukhi \{\s*font-family: var\(--ft-font-gurmukhi\);\s*font-size: 1\.75rem;\s*font-weight: 700;\s*color: var\(--ft-color-slate\);\s*margin-bottom: var\(--ft-space-xs\);',
     r'.ft-phrase-card__gurmukhi { font-family: var(--ft-font-gurmukhi); font-size: 1.75rem; font-weight: 700; color: var(--ft-color-slate); margin-bottom: var(--ft-space-lg); padding-bottom: var(--ft-space-sm);'),

    # Phrase card roman
    (r'\.ft-phrase-card__roman \{\s*font-family: var\(--ft-font-body\);\s*font-size: 1rem;\s*font-weight: 500;\s*color: var\(--ft-text-tertiary\);\s*margin-bottom: var\(--ft-space-md\);',
     r'.ft-phrase-card__roman { font-family: var(--ft-font-body); font-size: 1rem; font-weight: 500; color: var(--ft-text-tertiary); margin-bottom: var(--ft-space-lg); padding: var(--ft-space-sm) 0;'),

    # Phrase card translation
    (r'\.ft-phrase-card__translation \{\s*font-size: 0\.9375rem;\s*line-height: 1\.5;\s*color: var\(--ft-text-secondary\);\s*margin-bottom: var\(--ft-space-md\);',
     r'.ft-phrase-card__translation { font-size: 0.9375rem; line-height: 1.7; color: var(--ft-text-secondary); margin-bottom: var(--ft-space-xl); padding: var(--ft-space-md) 0;'),

    # Event title
    (r'\.ft-event-title \{\s*font-family: var\(--ft-font-headline\);\s*font-size: 1\.5rem;\s*font-weight: 600;\s*color: var\(--ft-color-slate\);\s*margin-bottom: var\(--ft-space-sm\);',
     r'.ft-event-title { font-family: var(--ft-font-headline); font-size: 1.5rem; font-weight: 600; color: var(--ft-color-slate); margin-bottom: var(--ft-space-lg); padding-bottom: var(--ft-space-sm);'),

    # Book title Gurmukhi
    (r'\.ft-book-title-gurmukhi \{\s*font-family: var\(--ft-font-gurmukhi\);\s*font-size: 1\.125rem;\s*font-weight: 700;\s*color: var\(--ft-color-slate\);\s*margin-bottom: 4px;',
     r'.ft-book-title-gurmukhi { font-family: var(--ft-font-gurmukhi); font-size: 1.125rem; font-weight: 700; color: var(--ft-color-slate); margin-bottom: var(--ft-space-md); padding: var(--ft-space-xs) 0;'),
]

def update_template(file_path):
    """Update CSS classes in style blocks for better spacing."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        changes_made = 0

        # Apply all CSS replacements
        for pattern, replacement in CSS_REPLACEMENTS:
            new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            if new_content != content:
                changes_made += re.subn(pattern, replacement, content, flags=re.MULTILINE)[1]
                content = new_content

        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] Updated CSS classes in {file_path.name} ({changes_made} improvements)")
            return True
        else:
            print(f"  No CSS class changes needed for {file_path.name}")
            return False

    except Exception as e:
        print(f"[ERROR] Error updating {file_path.name}: {e}")
        return False

def main():
    """Update CSS class definitions across all index pages."""
    print("=" * 80)
    print("PUNJABI SAHIT - CSS CLASS SPACING ENHANCEMENTS")
    print("Updating <style> blocks with better padding definitions")
    print("=" * 80)
    print()

    # Target index pages with CSS style blocks
    index_patterns = [
        "*_index_page.html",
    ]

    template_files = []
    for pattern in index_patterns:
        template_files.extend(TEMPLATE_DIR.glob(pattern))

    template_files = sorted(set(template_files))

    print(f"Found {len(template_files)} pages to update:")
    for f in template_files:
        print(f"  - {f.name}")
    print()

    updated_count = 0
    for template_file in template_files:
        if update_template(template_file):
            updated_count += 1

    print()
    print("=" * 80)
    print(f"COMPLETE: Updated CSS classes in {updated_count}/{len(template_files)} pages")
    print("=" * 80)
    print()
    print("[OK] All CSS card classes now have enhanced padding!")
    print("[OK] Restart Django server and hard refresh to see changes!")

if __name__ == "__main__":
    main()
