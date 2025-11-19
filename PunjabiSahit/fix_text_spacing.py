#!/usr/bin/env python3
"""
Add comprehensive padding, margins, and spacing to ALL text elements across all templates.
This fixes the cramped appearance by adding breathing room to paragraphs, headings, lists, etc.
"""

import os
import re
from pathlib import Path

TEMPLATE_DIR = Path(r"C:\src\PunjabiSahit\home\templates\home")

# Comprehensive spacing fixes for text content
REPLACEMENTS = [
    # Rich text content - add padding and margins
    (r'(\{\{\s*page\.body\|richtext\s*\}\})',
     r'<div style="padding: var(--ft-space-6); line-height: 1.8;">\1</div>'),

    (r'(\{\{\s*page\.explanation\|richtext\s*\}\})',
     r'<div style="padding: var(--ft-space-4); line-height: 1.8;">\1</div>'),

    (r'(\{\{\s*page\.example_usage\|richtext\s*\}\})',
     r'<div style="padding: var(--ft-space-4); line-height: 1.8;">\1</div>'),

    (r'(\{\{\s*page\.enriched_definition_gurmukhi\|richtext\s*\}\})',
     r'<div style="padding: var(--ft-space-4);">\1</div>'),

    (r'(\{\{\s*page\.enriched_definition_english\|richtext\s*\}\})',
     r'<div style="padding: var(--ft-space-4);">\1</div>'),

    (r'(\{\{\s*page\.example_sentences_gurmukhi\|richtext\s*\}\})',
     r'<div style="padding: var(--ft-space-4);">\1</div>'),

    (r'(\{\{\s*page\.biography_english\|richtext)',
     r'<div style="padding: var(--ft-space-4); line-height: 1.8;">\1</div>'),

    (r'(\{\{\s*page\.biography_gurmukhi\|richtext\s*\}\})',
     r'<div style="padding: var(--ft-space-4); line-height: 2;">\1</div>'),

    (r'(\{\{\s*page\.awards\|richtext\s*\}\})',
     r'<div style="padding: var(--ft-space-4); line-height: 1.8;">\1</div>'),

    # Section content divs - ensure they have padding
    (r'<div style="font-size: 1\.0625rem; line-height: 1\.7; color: var\(--ft-color-slate\);">',
     r'<div style="font-size: 1.0625rem; line-height: 1.8; color: var(--ft-color-slate); padding: var(--ft-space-4); margin-bottom: var(--ft-space-4);">'),

    (r'<div style="font-family: var\(--ft-font-gurmukhi\); font-size: 1\.25rem; line-height: 1\.8; color: var\(--ft-color-slate\);">',
     r'<div style="font-family: var(--ft-font-gurmukhi); font-size: 1.25rem; line-height: 2; color: var(--ft-color-slate); padding: var(--ft-space-4); margin-bottom: var(--ft-space-4);">'),

    (r'<div style="font-family: var\(--ft-font-gurmukhi\); font-size: 1\.125rem; line-height: 1\.7;',
     r'<div style="font-family: var(--ft-font-gurmukhi); font-size: 1.125rem; line-height: 2; padding: var(--ft-space-4); margin-bottom: var(--ft-space-4);'),

    # Paragraphs - add bottom margins
    (r'<p style="font-size: 1\.25rem; color: var\(--ft-text-tertiary\);',
     r'<p style="font-size: 1.25rem; color: var(--ft-text-tertiary); line-height: 1.8; margin-bottom: var(--ft-space-6);'),

    (r'<p style="font-size: 1\.125rem; color: var\(--ft-text-secondary\);',
     r'<p style="font-size: 1.125rem; color: var(--ft-text-secondary); line-height: 1.7; margin-bottom: var(--ft-space-4);'),

    (r'<p style="font-size: 0\.875rem; color: var\(--ft-text-tertiary\);',
     r'<p style="font-size: 0.875rem; color: var(--ft-text-tertiary); line-height: 1.6; margin-bottom: var(--ft-space-3);'),

    # Headings - add more bottom margin
    (r'<h1 style="font-family: var\(--ft-font-headline\); font-size: 3rem; font-weight: 700; color: var\(--ft-color-slate\); line-height: 1\.1; margin-bottom: var\(--ft-space-lg\);',
     r'<h1 style="font-family: var(--ft-font-headline); font-size: 3rem; font-weight: 700; color: var(--ft-color-slate); line-height: 1.2; margin-bottom: var(--ft-space-8); padding-bottom: var(--ft-space-4);'),

    (r'<h2 style="font-family: var\(--ft-font-headline\); font-size: 1\.5rem; font-weight: 700; color: var\(--ft-color-slate\); margin-bottom: var\(--ft-space-xl\);',
     r'<h2 style="font-family: var(--ft-font-headline); font-size: 1.5rem; font-weight: 700; color: var(--ft-color-slate); margin-bottom: var(--ft-space-8); padding-bottom: var(--ft-space-3);'),

    (r'<h3 style="font-weight: 600; color: var\(--ft-color-slate\); margin-bottom: 8px;',
     r'<h3 style="font-weight: 600; color: var(--ft-color-slate); margin-bottom: var(--ft-space-4); padding-bottom: var(--ft-space-2);'),

    (r'<h3 style="font-weight: 600; color: var\(--ft-color-slate\); margin-bottom: 12px;',
     r'<h3 style="font-weight: 600; color: var(--ft-color-slate); margin-bottom: var(--ft-space-4); padding-bottom: var(--ft-space-2);'),

    # Info boxes - add internal padding
    (r'<div style="background-color: #e0f2e9; border-left: 4px solid #228B22; padding: var\(--ft-space-4\);',
     r'<div style="background-color: #e0f2e9; border-left: 4px solid #228B22; padding: var(--ft-space-6); margin: var(--ft-space-4) 0;'),

    (r'<div style="background-color: #e0f2e9; border-left: 4px solid #228B22; padding: var\(--ft-space-lg\);',
     r'<div style="background-color: #e0f2e9; border-left: 4px solid #228B22; padding: var(--ft-space-6); margin: var(--ft-space-4) 0;'),

    (r'<div style="background-color: #ffe0e0; border-left: 4px solid var\(--ft-color-error\); padding: var\(--ft-space-lg\);',
     r'<div style="background-color: #ffe0e0; border-left: 4px solid var(--ft-color-error); padding: var(--ft-space-6); margin: var(--ft-space-4) 0;'),

    (r'<div style="background-color: var\(--ft-color-ft-pink\); border-left: 4px solid var\(--ft-color-oxford\); padding: var\(--ft-space-lg\);',
     r'<div style="background-color: var(--ft-color-ft-pink); border-left: 4px solid var(--ft-color-oxford); padding: var(--ft-space-6); margin: var(--ft-space-4) 0;'),

    (r'<div style="background-color: var\(--ft-color-ft-pink\); border-left: 4px solid var\(--ft-color-oxford\); padding: var\(--ft-space-4\);',
     r'<div style="background-color: var(--ft-color-ft-pink); border-left: 4px solid var(--ft-color-oxford); padding: var(--ft-space-6); margin: var(--ft-space-4) 0;'),

    (r'<div style="background-color: #e3f2fd; border-left: 4px solid var\(--ft-color-oxford\); padding: var\(--ft-space-4\);',
     r'<div style="background-color: #e3f2fd; border-left: 4px solid var(--ft-color-oxford); padding: var(--ft-space-6); margin: var(--ft-space-4) 0;'),

    # Example/content boxes with border-left
    (r'<div style="font-family: var\(--ft-font-gurmukhi\); font-size: 1\.125rem; line-height: 1\.7; color: var\(--ft-color-slate\); background-color: var\(--ft-bg-card\); padding: var\(--ft-space-4\); border-left: 4px solid var\(--ft-color-teal\);',
     r'<div style="font-family: var(--ft-font-gurmukhi); font-size: 1.125rem; line-height: 2; color: var(--ft-color-slate); background-color: var(--ft-bg-card); padding: var(--ft-space-6); margin: var(--ft-space-4) 0; border-left: 4px solid var(--ft-color-teal);'),

    (r'<div style="font-family: var\(--ft-font-gurmukhi\); font-size: 1\.125rem; line-height: 1\.7; color: rgba\(38, 42, 51, 0\.9\); background-color: var\(--ft-bg-card\); padding: var\(--ft-space-4\); border-left: 4px solid var\(--ft-color-teal\);',
     r'<div style="font-family: var(--ft-font-gurmukhi); font-size: 1.125rem; line-height: 2; color: rgba(38, 42, 51, 0.9); background-color: var(--ft-bg-card); padding: var(--ft-space-6); margin: var(--ft-space-4) 0; border-left: 4px solid var(--ft-color-teal);'),

    # Grid items - add padding
    (r'<div style="padding: 12px; background-color: var\(--ft-bg-card\); border-left: 3px solid var\(--ft-color-teal\);',
     r'<div style="padding: var(--ft-space-6); background-color: var(--ft-bg-card); border-left: 3px solid var(--ft-color-teal); margin-bottom: var(--ft-space-3);'),

    # Lists and text containers
    (r'<div style="font-size: 0\.75rem; color: var\(--ft-text-tertiary\); font-weight: 600; margin-bottom: 4px;',
     r'<div style="font-size: 0.75rem; color: var(--ft-text-tertiary); font-weight: 600; margin-bottom: var(--ft-space-2); padding-top: var(--ft-space-1);'),

    (r'<div style="font-size: 1\.25rem; font-weight: 600; color: var\(--ft-color-slate\);',
     r'<div style="font-size: 1.25rem; font-weight: 600; color: var(--ft-color-slate); padding: var(--ft-space-2) 0;'),

    # Add spacing to standalone text divs
    (r'<div style="font-size: 1\.125rem; font-weight: 700; color: var\(--ft-color-slate\); margin-bottom: 4px;',
     r'<div style="font-size: 1.125rem; font-weight: 700; color: var(--ft-color-slate); margin-bottom: var(--ft-space-3); padding: var(--ft-space-2) 0;'),

    (r'<div style="font-size: 0\.9375rem; color: var\(--ft-text-tertiary\);',
     r'<div style="font-size: 0.9375rem; color: var(--ft-text-tertiary); padding: var(--ft-space-1) 0; margin-top: var(--ft-space-1);'),
]

def update_template(file_path):
    """Update a single template file with comprehensive spacing improvements."""
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
    """Update all template files with comprehensive text spacing."""
    print("=" * 60)
    print("PUNJABI SAHIT - COMPREHENSIVE TEXT SPACING FIX")
    print("Adding padding, margins, and breathing room to all content")
    print("=" * 60)
    print()

    template_files = sorted(TEMPLATE_DIR.glob("*.html"))

    print(f"Found {len(template_files)} template files to update:")
    print()

    updated_count = 0
    for template_file in template_files:
        if update_template(template_file):
            updated_count += 1

    print()
    print("=" * 60)
    print(f"COMPLETE: Added spacing to {updated_count}/{len(template_files)} files")
    print("=" * 60)
    print()
    print("[OK] All text content now has proper padding and margins!")
    print("[OK] Restart Django server and hard refresh (Ctrl+Shift+R)")

if __name__ == "__main__":
    main()
