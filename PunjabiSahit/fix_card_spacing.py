#!/usr/bin/env python3
"""
Add MASSIVE padding and spacing to ALL cards and entries across index pages.
Makes everything minimalistic with proper breathing room.
Fixes: dictionary entries, blog cards, author cards, book cards, phrase cards, etc.
"""

import os
import re
from pathlib import Path

TEMPLATE_DIR = Path(r"C:\src\PunjabiSahit\home\templates\home")

# COMPREHENSIVE card and container spacing fixes
REPLACEMENTS = [
    # ============================================
    # DICTIONARY ENTRIES - Add massive padding
    # ============================================
    (r'display: block;\s*padding: var\(--ft-space-xl\) var\(--ft-space-2xl\);',
     r'display: block; padding: var(--ft-space-3xl) var(--ft-space-4xl);'),

    (r'<div style="background-color: var\(--ft-bg-card\); border: 1px solid rgba\(13, 118, 128, 0\.15\); overflow: hidden;">',
     r'<div style="background-color: var(--ft-bg-card); border: 1px solid rgba(13, 118, 128, 0.15); overflow: hidden; padding: var(--ft-space-4);">'),

    # Dictionary entry headword spacing
    (r'<h2 class="ft-dictionary-entry__headword">',
     r'<h2 class="ft-dictionary-entry__headword" style="padding: var(--ft-space-2) 0;">'),

    # ============================================
    # AUTHOR CARDS - Add more padding
    # ============================================
    (r'padding: var\(--ft-space-2xl\);\s*text-align: center;',
     r'padding: var(--ft-space-4xl); text-align: center;'),

    # Author grid - increase gap
    (r'<div class="ft-grid ft-grid--3" style="gap: var\(--ft-space-xl\);">',
     r'<div class="ft-grid ft-grid--3" style="gap: var(--ft-space-3xl);">'),

    # Author card names
    (r'<div style="margin-bottom: 12px;">',
     r'<div style="margin-bottom: var(--ft-space-6); padding: var(--ft-space-4) 0;">'),

    # ============================================
    # BLOG CARDS (Teasers) - Add padding
    # ============================================
    (r'<article class="o-teaser">',
     r'<article class="o-teaser" style="padding: var(--ft-space-lg);">'),

    # Blog grid - increase gap
    (r'<div class="ft-grid ft-grid--3">',
     r'<div class="ft-grid ft-grid--3" style="gap: var(--ft-space-3xl);">'),

    # ============================================
    # BOOK CARDS - Add more padding
    # ============================================
    (r'<div style="padding: var\(--ft-space-lg\);">',
     r'<div style="padding: var(--ft-space-3xl);">'),

    # Books grid - increase gap
    (r'<div style="display: grid; grid-template-columns: repeat\(auto-fill, minmax\(240px, 1fr\)\); gap: var\(--ft-space-xl\);">',
     r'<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: var(--ft-space-3xl);">'),

    # Book title container
    (r'<div style="margin-bottom: 12px;">',
     r'<div style="margin-bottom: var(--ft-space-6); padding: var(--ft-space-3) 0;">'),

    # Book metadata
    (r'<div style="margin-bottom: 12px;">',
     r'<div style="margin-bottom: var(--ft-space-6); padding: var(--ft-space-4) 0;">'),

    # ============================================
    # EVENT CARDS - Add more padding
    # ============================================
    (r'padding: var\(--ft-space-2xl\);\s*margin-bottom: var\(--ft-space-lg\);',
     r'padding: var(--ft-space-4xl); margin-bottom: var(--ft-space-3xl);'),

    # Event description spacing
    (r'<p style="font-size: 0\.875rem; line-height: 1\.6; color: var\(--ft-text-secondary\); margin-top: var\(--ft-space-3\); padding: var\(--ft-space-2\) 0;',
     r'<p style="font-size: 0.875rem; line-height: 1.6; color: var(--ft-text-secondary); margin-top: var(--ft-space-6); padding: var(--ft-space-4) 0;'),

    # ============================================
    # PHRASE CARDS - Add more padding
    # ============================================
    (r'padding: var\(--ft-space-2xl\);',
     r'padding: var(--ft-space-4xl);'),

    # Phrases grid - increase gap
    (r'<div class="ft-grid ft-grid--2" style="gap: var\(--ft-space-xl\);">',
     r'<div class="ft-grid ft-grid--2" style="gap: var(--ft-space-3xl);">'),

    # Phrase translation padding
    (r'<p class="ft-phrase-card__translation" style="padding: var\(--ft-space-2\) 0;">',
     r'<p class="ft-phrase-card__translation" style="padding: var(--ft-space-4) 0; margin-bottom: var(--ft-space-4);">'),

    # ============================================
    # FILTER BARS - Add more padding
    # ============================================
    (r'padding: var\(--ft-space-xl\);',
     r'padding: var(--ft-space-3xl);'),

    # ============================================
    # EMPTY STATES - More padding
    # ============================================
    (r'<div style="grid-column: 1 / -1; padding: 64px 32px;',
     r'<div style="grid-column: 1 / -1; padding: var(--ft-space-6xl) var(--ft-space-4xl);'),

    (r'<div style="grid-column: 1 / -1; text-align: center; padding: var\(--ft-space-12\);',
     r'<div style="grid-column: 1 / -1; text-align: center; padding: var(--ft-space-6xl);'),

    (r'<div style="padding: 64px 32px; text-align: center;">',
     r'<div style="padding: var(--ft-space-6xl) var(--ft-space-4xl); text-align: center;">'),

    # ============================================
    # SECTION HEADERS - Add padding around entire section
    # ============================================
    (r'<section style="border-top: 3px solid var\(--ft-color-slate\); border-bottom: 1px solid rgba\(13, 118, 128, 0\.15\); padding: var\(--ft-space-4\) 0; margin-bottom: var\(--ft-space-8\);">',
     r'<section style="border-top: 3px solid var(--ft-color-slate); border-bottom: 1px solid rgba(13, 118, 128, 0.15); padding: var(--ft-space-6) var(--ft-space-4); margin-bottom: var(--ft-space-12);">'),

    # ============================================
    # INTRO TEXT CONTAINERS - More padding
    # ============================================
    (r'<div style="max-width: 700px; margin-top: var\(--ft-space-4\);">',
     r'<div style="max-width: 700px; margin-top: var(--ft-space-6); margin-bottom: var(--ft-space-8);">'),

    # ============================================
    # CARD INNER CONTENT - Add breathing room
    # ============================================
    (r'<div style="flex: 1; min-width: 0;">',
     r'<div style="flex: 1; min-width: 0; padding: var(--ft-space-4);">'),

    # ============================================
    # VIEW COUNT / META - Add spacing
    # ============================================
    (r'<div style="display: flex; align-items: center; gap: 4px; font-size: 0\.75rem; color: var\(--ft-text-tertiary\);">',
     r'<div style="display: flex; align-items: center; gap: var(--ft-space-2); font-size: 0.75rem; color: var(--ft-text-tertiary); padding: var(--ft-space-3) 0; margin-top: var(--ft-space-4);">'),

    (r'<div style="display: flex; align-items: center; justify-content: center; gap: 4px; margin-top: 12px;',
     r'<div style="display: flex; align-items: center; justify-content: center; gap: var(--ft-space-2); margin-top: var(--ft-space-6); padding-top: var(--ft-space-4);'),

    # ============================================
    # BADGES - Add spacing around
    # ============================================
    (r'<span class="ft-phrase-badge">',
     r'<span class="ft-phrase-badge" style="margin-top: var(--ft-space-4);">'),

    (r'<span class="ft-author-badge">',
     r'<span class="ft-author-badge" style="margin: var(--ft-space-4) 0;">'),
]

def update_template(file_path):
    """Update a single template file with comprehensive card spacing."""
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
            print(f"[OK] Updated {file_path.name} ({changes_made} card spacing improvements)")
            return True
        else:
            print(f"  No card spacing changes needed for {file_path.name}")
            return False

    except Exception as e:
        print(f"[ERROR] Error updating {file_path.name}: {e}")
        return False

def main():
    """Add massive padding and spacing to ALL cards across all index pages."""
    print("=" * 80)
    print("PUNJABI SAHIT - COMPREHENSIVE CARD & ENTRY SPACING FIX")
    print("Making everything MINIMALISTIC with proper breathing room")
    print("Fixing: Cards, Entries, Grids, Containers, Filters, and Empty States")
    print("=" * 80)
    print()

    # Target ALL index pages and home page
    index_patterns = [
        "*_index_page.html",
        "home_page.html"
    ]

    template_files = []
    for pattern in index_patterns:
        template_files.extend(TEMPLATE_DIR.glob(pattern))

    template_files = sorted(set(template_files))

    print(f"Found {len(template_files)} pages to enhance:")
    for f in template_files:
        print(f"  - {f.name}")
    print()

    updated_count = 0
    total_improvements = 0
    for template_file in template_files:
        if update_template(template_file):
            updated_count += 1

    print()
    print("=" * 80)
    print(f"COMPLETE: Enhanced {updated_count}/{len(template_files)} pages with card spacing")
    print("=" * 80)
    print()
    print("[OK] All cards now have MASSIVE padding for minimalistic design!")
    print("[OK] Increased gaps between all grid items!")
    print("[OK] Added breathing room to all containers!")
    print()
    print("[NEXT] Restart Django server and hard refresh (Ctrl+Shift+R)")

if __name__ == "__main__":
    main()
