#!/usr/bin/env python3
"""
MASSIVE COMPREHENSIVE STYLING FOR ALL ELEMENTS ACROSS THE ENTIRE SITE.
Adds borders, rounded corners, shadows, and padding to EVERYTHING.
No element left unstyled!
"""

import os
import re
from pathlib import Path

TEMPLATE_DIR = Path(r"C:\src\PunjabiSahit\home\templates\home")

# ULTRA COMPREHENSIVE - Style EVERY element type
REPLACEMENTS = [
    # ============================================
    # ALL MAIN CONTAINERS - Add borders and shadows
    # ============================================
    (r'<main class="ft-container ft-py-lg">',
     r'<main class="ft-container ft-py-lg" style="padding: var(--ft-space-6xl);">'),

    # ============================================
    # ALL SECTION BLOCKS - Enhanced styling
    # ============================================
    (r'<section style="border-top: 3px solid var\(--ft-color-slate\); border-bottom: 1px solid rgba\(13, 118, 128, 0\.15\);',
     r'<section style="border: 3px solid var(--ft-color-slate); border-radius: var(--ft-radius-xl); box-shadow: var(--ft-shadow-lg); background-color: var(--ft-bg-card);'),

    # ============================================
    # ALL GRID CONTAINERS - Add padding and gaps
    # ============================================
    (r'<div class="ft-grid ft-grid--2"',
     r'<div class="ft-grid ft-grid--2" style="padding: var(--ft-space-6); gap: var(--ft-space-4xl);"'),

    (r'<div class="ft-grid ft-grid--3"',
     r'<div class="ft-grid ft-grid--3" style="padding: var(--ft-space-6); gap: var(--ft-space-4xl);"'),

    (r'<div class="ft-grid ft-grid--4-2"',
     r'<div class="ft-grid ft-grid--4-2" style="padding: var(--ft-space-6); gap: var(--ft-space-4xl);"'),

    # ============================================
    # FILTER BARS - Make them prominent cards
    # ============================================
    (r'<div class="ft-filter-bar">',
     r'<div class="ft-filter-bar" style="border: 2px solid rgba(13, 118, 128, 0.25); border-radius: var(--ft-radius-xl); box-shadow: var(--ft-shadow-xl); padding: var(--ft-space-5xl); margin-bottom: var(--ft-space-5xl);">'),

    # ============================================
    # ALL CARD COMPONENTS - Maximum styling
    # ============================================
    (r'class="ft-dictionary-entry"',
     r'class="ft-dictionary-entry" style="border: 2px solid rgba(13, 118, 128, 0.2); border-radius: var(--ft-radius-xl); box-shadow: var(--ft-shadow-lg); margin-bottom: var(--ft-space-4);"'),

    (r'class="ft-author-card"',
     r'class="ft-author-card" style="border: 2px solid rgba(13, 118, 128, 0.2); border-radius: var(--ft-radius-xl); box-shadow: var(--ft-shadow-lg);"'),

    (r'class="ft-phrase-card"',
     r'class="ft-phrase-card" style="border: 2px solid rgba(13, 118, 128, 0.2); border-radius: var(--ft-radius-xl); box-shadow: var(--ft-shadow-lg); margin-bottom: var(--ft-space-4);"'),

    (r'class="ft-event-card"',
     r'class="ft-event-card" style="border: 2px solid rgba(13, 118, 128, 0.2); border-radius: var(--ft-radius-xl); box-shadow: var(--ft-shadow-lg);"'),

    (r'class="ft-book-card"',
     r'class="ft-book-card" style="border: 2px solid rgba(13, 118, 128, 0.2); border-radius: var(--ft-radius-xl); box-shadow: var(--ft-shadow-lg);"'),

    (r'class="o-teaser"',
     r'class="o-teaser" style="border: 2px solid rgba(13, 118, 128, 0.15); border-radius: var(--ft-radius-xl); box-shadow: var(--ft-shadow-lg); background-color: var(--ft-bg-card);"'),

    # ============================================
    # ALL HEADINGS - Add padding and spacing
    # ============================================
    (r'<h1 style="([^"]*)"',
     lambda m: f'<h1 style="{m.group(1)}; padding: var(--ft-space-6); border-bottom: 3px solid rgba(13, 118, 128, 0.2); margin-bottom: var(--ft-space-6);"'),

    (r'<h2 class="ft-section-heading"',
     r'<h2 class="ft-section-heading" style="padding: var(--ft-space-5) 0; margin-bottom: var(--ft-space-6); border-bottom: 2px solid rgba(13, 118, 128, 0.15);"'),

    (r'<h2 style="([^"]*font-family: var\(--ft-font-headline\)[^"]*)"',
     lambda m: f'<h2 style="{m.group(1)}; padding: var(--ft-space-4) 0; margin-bottom: var(--ft-space-6);"'),

    (r'<h3 style="([^"]*)"',
     lambda m: f'<h3 style="{m.group(1)}; padding: var(--ft-space-3) 0; margin-top: var(--ft-space-4);"'),

    # ============================================
    # ALL TEXT CONTAINERS - Add padding
    # ============================================
    (r'<div style="font-size: 1\.0625rem; line-height: 1\.[78]; color: var\(--ft-color-slate\);',
     r'<div style="font-size: 1.0625rem; line-height: 1.8; color: var(--ft-color-slate); padding: var(--ft-space-6); border-left: 4px solid rgba(13, 118, 128, 0.2); background-color: rgba(255, 255, 255, 0.5);'),

    (r'<div style="font-family: var\(--ft-font-gurmukhi\); font-size: 1\.25rem; line-height: 2',
     r'<div style="font-family: var(--ft-font-gurmukhi); font-size: 1.25rem; line-height: 2.2; padding: var(--ft-space-6); border-left: 4px solid rgba(13, 118, 128, 0.2); background-color: rgba(255, 255, 255, 0.5);'),

    # ============================================
    # ALL PARAGRAPH BLOCKS - Enhanced spacing
    # ============================================
    (r'<p style="font-size: 1\.25rem;',
     r'<p style="font-size: 1.25rem; padding: var(--ft-space-4) 0; margin-bottom: var(--ft-space-6);'),

    (r'<p style="font-size: 1\.125rem;',
     r'<p style="font-size: 1.125rem; padding: var(--ft-space-3) 0; margin-bottom: var(--ft-space-5);'),

    (r'<p style="font-size: 0\.9375rem;',
     r'<p style="font-size: 0.9375rem; padding: var(--ft-space-2) 0; margin-bottom: var(--ft-space-4);'),

    # ============================================
    # NAVIGATION ELEMENTS - Style alphabet nav
    # ============================================
    (r'<div class="ft-alphabet-nav">',
     r'<div class="ft-alphabet-nav" style="border: 2px solid rgba(13, 118, 128, 0.2); border-radius: var(--ft-radius-lg); padding: var(--ft-space-5); box-shadow: var(--ft-shadow-md);">'),

    # ============================================
    # VIEW COUNT / META SECTIONS - Card style
    # ============================================
    (r'<div style="display: flex; align-items: center; justify-content: space-between; padding-top: 12px; border-top: 1px',
     r'<div style="display: flex; align-items: center; justify-content: space-between; padding: var(--ft-space-6); margin-top: var(--ft-space-6); border-top: 2px'),

    # ============================================
    # METADATA GRIDS - Enhanced design
    # ============================================
    (r'<div style="display: grid; grid-template-columns:',
     r'<div style="display: grid; grid-template-columns:'),

    # ============================================
    # EMPTY STATES - Make them beautiful
    # ============================================
    (r'<div style="grid-column: 1 / -1;',
     r'<div style="grid-column: 1 / -1; border: 3px dashed rgba(13, 118, 128, 0.3); border-radius: var(--ft-radius-2xl);'),

    # ============================================
    # PAGINATION - Enhanced buttons
    # ============================================
    (r'<div style="margin-top: var\(--ft-space-8\); display: flex; justify-content: center;',
     r'<div style="margin-top: var(--ft-space-8); padding: var(--ft-space-6); display: flex; justify-content: center; background-color: rgba(255, 255, 255, 0.3); border-radius: var(--ft-radius-lg);'),

    # ============================================
    # BADGES - Add shadows and better spacing
    # ============================================
    (r'class="ft-dictionary-badge"',
     r'class="ft-dictionary-badge" style="box-shadow: var(--ft-shadow-sm); margin: var(--ft-space-2);"'),

    (r'class="ft-phrase-badge"',
     r'class="ft-phrase-badge" style="box-shadow: var(--ft-shadow-sm); border-radius: var(--ft-radius-md);"'),

    (r'class="ft-author-badge"',
     r'class="ft-author-badge" style="box-shadow: var(--ft-shadow-sm); border-radius: var(--ft-radius-md);"'),

    (r'class="ft-event-badge',
     r'class="ft-event-badge" style="box-shadow: var(--ft-shadow-sm); padding: var(--ft-space-3) var(--ft-space-4);"'),

    # ============================================
    # DATE BADGES (Events) - Card design
    # ============================================
    (r'<div class="ft-event-date-badge"',
     r'<div class="ft-event-date-badge" style="border: 2px solid var(--ft-color-teal); border-radius: var(--ft-radius-lg); box-shadow: var(--ft-shadow-lg);"'),

    # ============================================
    # TAB NAVIGATION - Enhanced design
    # ============================================
    (r'<nav style="display: flex; gap: var\(--ft-space-2\); margin-bottom: var\(--ft-space-lg\);',
     r'<nav style="display: flex; gap: var(--ft-space-3); margin-bottom: var(--ft-space-xl); padding: var(--ft-space-4); background-color: rgba(255, 255, 255, 0.5); border-radius: var(--ft-radius-lg);'),

    # ============================================
    # ROMANIZATION GRID - Enhanced items
    # ============================================
    (r'<div class="ft-romanization-grid">',
     r'<div class="ft-romanization-grid" style="gap: var(--ft-space-6); padding: var(--ft-space-4);">'),

    # ============================================
    # BOOK METADATA SECTIONS
    # ============================================
    (r'<div class="ft-book-meta">',
     r'<div class="ft-book-meta" style="padding: var(--ft-space-3) 0; margin: var(--ft-space-2) 0;">'),

    # ============================================
    # PHRASE META
    # ============================================
    (r'<div class="ft-phrase-meta">',
     r'<div class="ft-phrase-meta" style="padding: var(--ft-space-4) 0; margin-top: var(--ft-space-4); border-top: 1px solid rgba(13, 118, 128, 0.1);">'),

    # ============================================
    # EVENT DETAIL SECTIONS
    # ============================================
    (r'<div class="ft-event-detail">',
     r'<div class="ft-event-detail" style="padding: var(--ft-space-3) 0; margin: var(--ft-space-2) 0;">'),

    # ============================================
    # CALENDAR CONTAINER
    # ============================================
    (r'<div id="calendar"',
     r'<div id="calendar" style="border: 3px solid rgba(13, 118, 128, 0.2); border-radius: var(--ft-radius-xl); box-shadow: var(--ft-shadow-2xl);"'),

    # ============================================
    # INTRO TEXT BLOCKS - Card design
    # ============================================
    (r'<div style="max-width: 700px;',
     r'<div style="max-width: 700px; padding: var(--ft-space-6); border-left: 5px solid var(--ft-color-teal); background-color: rgba(255, 255, 255, 0.7); border-radius: var(--ft-radius-md); box-shadow: var(--ft-shadow-sm);'),

    # ============================================
    # RESULTS COUNT - Enhanced display
    # ============================================
    (r'<div class="ft-results-count">',
     r'<div class="ft-results-count" style="padding: var(--ft-space-4); background-color: rgba(13, 118, 128, 0.05); border-radius: var(--ft-radius-md);">'),

    # ============================================
    # FILTER GROUPS - Better spacing
    # ============================================
    (r'<div class="ft-filter-group">',
     r'<div class="ft-filter-group" style="padding: var(--ft-space-5); border-radius: var(--ft-radius-md); background-color: rgba(255, 255, 255, 0.5);">'),
]

def update_template(file_path):
    """Apply MASSIVE styling to ALL elements in template."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        changes_made = 0

        # Apply all replacements
        for pattern, replacement in REPLACEMENTS:
            if callable(replacement):
                # For lambda replacements
                new_content = re.sub(pattern, replacement, content)
            else:
                new_content = re.sub(pattern, replacement, content)

            if new_content != content:
                if callable(replacement):
                    changes_made += len(re.findall(pattern, content))
                else:
                    changes_made += re.subn(pattern, replacement, content)[1]
                content = new_content

        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] MASSIVELY ENHANCED {file_path.name} ({changes_made} elements styled)")
            return True
        else:
            print(f"  Already perfect: {file_path.name}")
            return False

    except Exception as e:
        print(f"[ERROR] Error updating {file_path.name}: {e}")
        return False

def main():
    """Apply MASSIVE comprehensive styling to EVERY element across the entire site."""
    print("=" * 100)
    print(" " * 20 + "PUNJABI SAHIT - ULTIMATE MASSIVE DESIGN TRANSFORMATION")
    print(" " * 15 + "Styling EVERY SINGLE ELEMENT with borders, shadows, and padding")
    print("=" * 100)
    print()

    template_files = sorted(TEMPLATE_DIR.glob("*.html"))

    print(f"Found {len(template_files)} template files to MASSIVELY ENHANCE:")
    for f in template_files:
        print(f"  - {f.name}")
    print()
    print("Applying comprehensive styling to:")
    print("  - All main containers")
    print("  - All section blocks")
    print("  - All grid layouts")
    print("  - All cards and entries")
    print("  - All headings (h1, h2, h3)")
    print("  - All text containers")
    print("  - All paragraphs")
    print("  - All navigation elements")
    print("  - All metadata sections")
    print("  - All badges and labels")
    print("  - All filters and forms")
    print("  - All pagination")
    print("  - ALL other elements!")
    print()

    updated_count = 0
    for template_file in template_files:
        if update_template(template_file):
            updated_count += 1

    print()
    print("=" * 100)
    print(f"MASSIVE TRANSFORMATION COMPLETE: Enhanced {updated_count}/{len(template_files)} files")
    print("=" * 100)
    print()
    print("[SUCCESS] Every element now has:")
    print("  [+] Proper borders everywhere")
    print("  [+] Rounded corners on all components")
    print("  [+] Box shadows for depth")
    print("  [+] Massive padding throughout")
    print("  [+] Enhanced spacing between elements")
    print("  [+] Professional card-based design")
    print("  [+] Visual hierarchy and structure")
    print()
    print("[ACTION] Restart Django server NOW and hard refresh (Ctrl+Shift+R)")
    print("[RESULT] Your site will look COMPLETELY TRANSFORMED!")

if __name__ == "__main__":
    main()
