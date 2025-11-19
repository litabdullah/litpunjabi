#!/usr/bin/env python3
"""
Add BORDERS, ROUNDED CORNERS, SHADOWS, and PADDING to ALL content blocks.
Transforms plain text blocks into beautiful cards with modern design.
Fixes: headword sections, synonym/antonym boxes, origin blocks, example sections, etc.
"""

import os
import re
from pathlib import Path

TEMPLATE_DIR = Path(r"C:\src\PunjabiSahit\home\templates\home")

# COMPREHENSIVE content block styling - add borders, shadows, border-radius, padding
REPLACEMENTS = [
    # ============================================
    # HEADWORD CARD - Make it a prominent card
    # ============================================
    (r'<div class="ft-headword-card" style="background-color: var\(--ft-bg-card\); border: 1px solid rgba\(13, 118, 128, 0\.15\); padding: var\(--ft-space-3xl\);',
     r'<div class="ft-headword-card" style="background-color: var(--ft-bg-card); border: 2px solid rgba(13, 118, 128, 0.2); border-radius: var(--ft-radius-lg); box-shadow: var(--ft-shadow-lg); padding: var(--ft-space-5xl); margin-bottom: var(--ft-space-3xl);'),

    # ============================================
    # SYNONYM BOXES - Transform to cards
    # ============================================
    (r'<div class="ft-synonym-box">',
     r'<div class="ft-synonym-box" style="background-color: #e0f2e9; border: 2px solid #228B22; border-radius: var(--ft-radius-lg); padding: var(--ft-space-6); margin: var(--ft-space-4) 0; box-shadow: var(--ft-shadow-md);">'),

    (r'<div style="background-color: #e0f2e9; border-left: 4px solid #228B22; padding: var\(--ft-space-6\); margin: var\(--ft-space-4\) 0;">',
     r'<div style="background-color: #e0f2e9; border: 2px solid #228B22; border-left: 6px solid #228B22; border-radius: var(--ft-radius-lg); padding: var(--ft-space-6); margin: var(--ft-space-6) 0; box-shadow: var(--ft-shadow-md);">'),

    # ============================================
    # ANTONYM BOXES - Transform to cards
    # ============================================
    (r'<div class="ft-antonym-box">',
     r'<div class="ft-antonym-box" style="background-color: #ffe0e0; border: 2px solid var(--ft-color-error); border-radius: var(--ft-radius-lg); padding: var(--ft-space-6); margin: var(--ft-space-4) 0; box-shadow: var(--ft-shadow-md);">'),

    (r'<div style="background-color: #ffe0e0; border-left: 4px solid var\(--ft-color-error\); padding: var\(--ft-space-6\); margin: var\(--ft-space-4\) 0;">',
     r'<div style="background-color: #ffe0e0; border: 2px solid var(--ft-color-error); border-left: 6px solid var(--ft-color-error); border-radius: var(--ft-radius-lg); padding: var(--ft-space-6); margin: var(--ft-space-6) 0; box-shadow: var(--ft-shadow-md);">'),

    # ============================================
    # ETYMOLOGY / ORIGIN BOXES - Transform to cards
    # ============================================
    (r'<div class="ft-etymology-box">',
     r'<div class="ft-etymology-box" style="background-color: var(--ft-color-ft-pink); border: 2px solid var(--ft-color-oxford); border-radius: var(--ft-radius-lg); padding: var(--ft-space-6); margin: var(--ft-space-4) 0; box-shadow: var(--ft-shadow-md);">'),

    (r'<div style="background-color: var\(--ft-color-ft-pink\); border-left: 4px solid var\(--ft-color-oxford\); padding: var\(--ft-space-6\); margin: var\(--ft-space-4\) 0;">',
     r'<div style="background-color: var(--ft-color-ft-pink); border: 2px solid var(--ft-color-oxford); border-left: 6px solid var(--ft-color-oxford); border-radius: var(--ft-radius-lg); padding: var(--ft-space-6); margin: var(--ft-space-6) 0; box-shadow: var(--ft-shadow-md);">'),

    (r'<div style="background-color: #e3f2fd; border-left: 4px solid var\(--ft-color-oxford\); padding: var\(--ft-space-6\); margin: var\(--ft-space-4\) 0;">',
     r'<div style="background-color: #e3f2fd; border: 2px solid var(--ft-color-oxford); border-left: 6px solid var(--ft-color-oxford); border-radius: var(--ft-radius-lg); padding: var(--ft-space-6); margin: var(--ft-space-6) 0; box-shadow: var(--ft-shadow-md);">'),

    # ============================================
    # EXAMPLE SENTENCES - Transform to cards with teal accent
    # ============================================
    (r'<div style="font-family: var\(--ft-font-gurmukhi\); font-size: 1\.125rem; line-height: 2; padding: var\(--ft-space-4\); margin-bottom: var\(--ft-space-4\); color: rgba\(38, 42, 51, 0\.9\); background-color: var\(--ft-bg-card\); padding: var\(--ft-space-4\); border-left: 4px solid var\(--ft-color-teal\);',
     r'<div style="font-family: var(--ft-font-gurmukhi); font-size: 1.125rem; line-height: 2.2; padding: var(--ft-space-6); margin-bottom: var(--ft-space-6); color: rgba(38, 42, 51, 0.9); background-color: var(--ft-bg-card); border: 2px solid var(--ft-color-teal); border-left: 6px solid var(--ft-color-teal); border-radius: var(--ft-radius-lg); box-shadow: var(--ft-shadow-md);'),

    (r'<div style="font-family: var\(--ft-font-gurmukhi\); font-size: 1\.125rem; line-height: 2; color: var\(--ft-color-slate\); background-color: var\(--ft-bg-card\); padding: var\(--ft-space-6\); margin: var\(--ft-space-4\) 0; border-left: 4px solid var\(--ft-color-teal\);',
     r'<div style="font-family: var(--ft-font-gurmukhi); font-size: 1.125rem; line-height: 2.2; color: var(--ft-color-slate); background-color: var(--ft-bg-card); padding: var(--ft-space-6); margin: var(--ft-space-6) 0; border: 2px solid var(--ft-color-teal); border-left: 6px solid var(--ft-color-teal); border-radius: var(--ft-radius-lg); box-shadow: var(--ft-shadow-md);'),

    # ============================================
    # ROMANIZATION GRID ITEMS - Add borders and shadows
    # ============================================
    (r'<div style="padding: var\(--ft-space-6\); background-color: var\(--ft-bg-card\); border-left: 3px solid var\(--ft-color-teal\); margin-bottom: var\(--ft-space-3\);">',
     r'<div style="padding: var(--ft-space-6); background-color: var(--ft-bg-card); border: 2px solid rgba(13, 118, 128, 0.2); border-left: 5px solid var(--ft-color-teal); border-radius: var(--ft-radius-md); margin-bottom: var(--ft-space-4); box-shadow: var(--ft-shadow-sm);">'),

    # ============================================
    # TAB CONTENT - Add borders to definition tabs
    # ============================================
    (r'<div id="gurmukhi-def" class="ft-tab-content active">',
     r'<div id="gurmukhi-def" class="ft-tab-content active" style="border: 2px solid rgba(13, 118, 128, 0.15); border-radius: var(--ft-radius-lg); padding: var(--ft-space-6); background-color: var(--ft-bg-card); box-shadow: var(--ft-shadow-sm);">'),

    (r'<div id="english-def" class="ft-tab-content">',
     r'<div id="english-def" class="ft-tab-content" style="border: 2px solid rgba(13, 118, 128, 0.15); border-radius: var(--ft-radius-lg); padding: var(--ft-space-6); background-color: var(--ft-bg-card); box-shadow: var(--ft-shadow-sm);">'),

    (r'<div id="shahmukhi-def" class="ft-tab-content">',
     r'<div id="shahmukhi-def" class="ft-tab-content" style="border: 2px solid rgba(13, 118, 128, 0.15); border-radius: var(--ft-radius-lg); padding: var(--ft-space-6); background-color: var(--ft-bg-card); box-shadow: var(--ft-shadow-sm);">'),

    # ============================================
    # SECTION CONTAINERS - Add subtle borders
    # ============================================
    (r'<div style="margin-bottom: var\(--ft-space-6\);">(\s*)<h3',
     r'<div style="margin-bottom: var(--ft-space-6); padding: var(--ft-space-4); border: 1px solid rgba(13, 118, 128, 0.1); border-radius: var(--ft-radius-md); background-color: rgba(255, 255, 255, 0.5);">\1<h3'),

    # ============================================
    # INFO BLOCKS - General styling for all info blocks
    # ============================================
    (r'<div style="background-color: var\(--ft-bg-card\); border-left: 4px solid var\(--ft-color-teal\);">',
     r'<div style="background-color: var(--ft-bg-card); border: 2px solid var(--ft-color-teal); border-left: 6px solid var(--ft-color-teal); border-radius: var(--ft-radius-lg); padding: var(--ft-space-6); box-shadow: var(--ft-shadow-md);">'),

    # ============================================
    # AUTHOR DETAIL SECTIONS - Biography blocks
    # ============================================
    (r'<div style="margin-top: var\(--ft-space-3xl\); padding-top: var\(--ft-space-2xl\); border-top: 2px solid rgba\(13, 118, 128, 0\.15\);">',
     r'<div style="margin-top: var(--ft-space-3xl); padding: var(--ft-space-3xl); border: 2px solid rgba(13, 118, 128, 0.15); border-radius: var(--ft-radius-lg); background-color: var(--ft-bg-card); box-shadow: var(--ft-shadow-md);">'),

    # ============================================
    # EVENT DETAIL GRIDS - Date/time and location boxes
    # ============================================
    (r'<div style="display: flex; gap: var\(--ft-space-3\); padding: var\(--ft-space-lg\); background-color: var\(--ft-bg-card\); border-left: 4px solid var\(--ft-color-teal\);">',
     r'<div style="display: flex; gap: var(--ft-space-3); padding: var(--ft-space-xl); background-color: var(--ft-bg-card); border: 2px solid var(--ft-color-teal); border-left: 6px solid var(--ft-color-teal); border-radius: var(--ft-radius-lg); box-shadow: var(--ft-shadow-md);">'),

    # ============================================
    # BOOK/PHRASE/IDIOM INFO BLOCKS
    # ============================================
    (r'<div style="font-family: var\(--ft-font-gurmukhi\); font-size: 1\.125rem; line-height: 2; color: rgba\(38, 42, 51, 0\.9\); background-color: var\(--ft-bg-card\); border-left: 4px solid var\(--ft-color-teal\);">',
     r'<div style="font-family: var(--ft-font-gurmukhi); font-size: 1.125rem; line-height: 2.2; color: rgba(38, 42, 51, 0.9); background-color: var(--ft-bg-card); border: 2px solid var(--ft-color-teal); border-left: 6px solid var(--ft-color-teal); border-radius: var(--ft-radius-lg); padding: var(--ft-space-6); box-shadow: var(--ft-shadow-md);">'),

    # ============================================
    # SIMILAR POSTS CARDS (Blog)
    # ============================================
    (r'<a href="\{\{ post\.url \}\}" style="display: block; background-color: var\(--ft-bg-card\); border: 1px solid rgba\(13, 118, 128, 0\.15\); border-radius: var\(--ft-radius-md\);',
     r'<a href="{{ post.url }}" style="display: block; background-color: var(--ft-bg-card); border: 2px solid rgba(13, 118, 128, 0.15); border-radius: var(--ft-radius-lg); box-shadow: var(--ft-shadow-md);'),

    # ============================================
    # INDEX PAGE CARDS - Add borders to all cards
    # ============================================
    (r'background-color: var\(--ft-bg-card\);\s*border: 1px solid rgba\(13, 118, 128, 0\.15\);',
     r'background-color: var(--ft-bg-card); border: 2px solid rgba(13, 118, 128, 0.2); border-radius: var(--ft-radius-lg); box-shadow: var(--ft-shadow-md);'),
]

def update_template(file_path):
    """Add borders, shadows, and rounded corners to content blocks."""
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
            print(f"[OK] Updated {file_path.name} ({changes_made} design improvements)")
            return True
        else:
            print(f"  No design changes needed for {file_path.name}")
            return False

    except Exception as e:
        print(f"[ERROR] Error updating {file_path.name}: {e}")
        return False

def main():
    """Add borders, shadows, and rounded designs to ALL content blocks."""
    print("=" * 90)
    print("PUNJABI SAHIT - COMPREHENSIVE CONTENT BLOCK DESIGN ENHANCEMENT")
    print("Adding BORDERS, ROUNDED CORNERS, SHADOWS, and PADDING to all content blocks")
    print("=" * 90)
    print()

    # Target ALL template files (detail pages and index pages)
    template_files = sorted(TEMPLATE_DIR.glob("*.html"))

    print(f"Found {len(template_files)} template files to enhance:")
    for f in template_files:
        print(f"  - {f.name}")
    print()

    updated_count = 0
    for template_file in template_files:
        if update_template(template_file):
            updated_count += 1

    print()
    print("=" * 90)
    print(f"COMPLETE: Enhanced {updated_count}/{len(template_files)} files with modern card designs")
    print("=" * 90)
    print()
    print("[OK] All content blocks now have:")
    print("     ✓ Proper borders (2px)")
    print("     ✓ Rounded corners (border-radius)")
    print("     ✓ Box shadows for depth")
    print("     ✓ Enhanced padding")
    print("     ✓ Better visual hierarchy")
    print()
    print("[NEXT] Restart Django server and hard refresh (Ctrl+Shift+R)")

if __name__ == "__main__":
    main()
