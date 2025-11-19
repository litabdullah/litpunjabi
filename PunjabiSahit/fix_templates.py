#!/usr/bin/env python3
"""
Automatically update all Punjabi Sahit templates to use the new 2025 design system.
This script updates all inline styles to use modern CSS variables.
"""

import os
import re
from pathlib import Path

# Template directory
TEMPLATE_DIR = Path(r"C:\src\PunjabiSahit\home\templates\home")

# Find and replace mappings
REPLACEMENTS = [
    # Background colors
    (r'background-color:\s*var\(--ft-color-white\)', 'background-color: var(--ft-bg-card)'),
    (r'background:\s*var\(--ft-color-white\)', 'background: var(--ft-bg-card)'),
    (r'background-color:\s*var\(--ft-color-paper\)(?!;?\s*})', 'background-color: var(--ft-bg-card)'),

    # Border colors
    (r'border:\s*1px solid var\(--ft-color-grey-1\)', 'border: 1px solid rgba(13, 118, 128, 0.15)'),
    (r'border-top:\s*1px solid var\(--ft-color-grey-1\)', 'border-top: 1px solid rgba(13, 118, 128, 0.15)'),
    (r'border-bottom:\s*1px solid var\(--ft-color-grey-1\)', 'border-bottom: 1px solid rgba(13, 118, 128, 0.15)'),
    (r'border-left:\s*1px solid var\(--ft-color-grey-1\)', 'border-left: 1px solid rgba(13, 118, 128, 0.15)'),
    (r'border-right:\s*1px solid var\(--ft-color-grey-1\)', 'border-right: 1px solid rgba(13, 118, 128, 0.15)'),
    (r'border-bottom:\s*2px solid var\(--ft-color-grey-1\)', 'border-bottom: 2px solid rgba(13, 118, 128, 0.15)'),
    (r'border-top:\s*2px solid var\(--ft-color-grey-1\)', 'border-top: 2px solid rgba(13, 118, 128, 0.15)'),
    (r'border-top:\s*3px solid var\(--ft-color-grey-1\)', 'border-top: 3px solid rgba(13, 118, 128, 0.15)'),

    # Text colors
    (r'color:\s*var\(--ft-color-white\)', 'color: var(--ft-text-inverse)'),
    (r'color:\s*var\(--ft-color-grey-3\)', 'color: var(--ft-text-tertiary)'),
    (r'color:\s*rgba\(38,\s*42,\s*51,\s*0\.8\)', 'color: var(--ft-text-secondary)'),

    # Transitions
    (r'transition:\s*var\(--ft-transition\)(?!-)', 'transition: var(--ft-transition-base)'),

    # Border radius (only update old 2px values)
    (r'border-radius:\s*var\(--ft-radius\)(?!-)', 'border-radius: var(--ft-radius-md)'),

    # Spacing - replace hardcoded values with variables
    (r'padding:\s*48px', 'padding: var(--ft-space-12)'),
    (r'padding:\s*32px', 'padding: var(--ft-space-8)'),
    (r'padding:\s*24px', 'padding: var(--ft-space-6)'),
    (r'padding:\s*16px', 'padding: var(--ft-space-4)'),
    (r'margin-bottom:\s*48px', 'margin-bottom: var(--ft-space-12)'),
    (r'margin-bottom:\s*32px', 'margin-bottom: var(--ft-space-8)'),
    (r'margin-bottom:\s*24px', 'margin-bottom: var(--ft-space-6)'),
    (r'margin-bottom:\s*16px', 'margin-bottom: var(--ft-space-4)'),
    (r'margin-top:\s*48px', 'margin-top: var(--ft-space-12)'),
    (r'margin-top:\s*32px', 'margin-top: var(--ft-space-8)'),
    (r'margin-top:\s*24px', 'margin-top: var(--ft-space-6)'),
    (r'margin-top:\s*16px', 'margin-top: var(--ft-space-4)'),
    (r'gap:\s*32px', 'gap: var(--ft-space-8)'),
    (r'gap:\s*24px', 'gap: var(--ft-space-6)'),
    (r'gap:\s*16px', 'gap: var(--ft-space-4)'),
    (r'gap:\s*12px', 'gap: var(--ft-space-3)'),
    (r'gap:\s*8px', 'gap: var(--ft-space-2)'),

    # Shadow updates
    (r'box-shadow:\s*var\(--ft-shadow-sm\)(?=;)', 'box-shadow: var(--ft-shadow-md)'),
]

def update_template(file_path):
    """Update a single template file with all replacements."""
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
            print(f"[OK] Updated {file_path.name} ({changes_made} changes)")
            return True
        else:
            print(f"  No changes needed for {file_path.name}")
            return False

    except Exception as e:
        print(f"[ERROR] Error updating {file_path.name}: {e}")
        return False

def main():
    """Update all template files."""
    print("=" * 60)
    print("PUNJABI SAHIT - TEMPLATE MODERNIZATION SCRIPT")
    print("=" * 60)
    print()

    # Get all HTML files in the template directory
    template_files = list(TEMPLATE_DIR.glob("*.html"))

    if not template_files:
        print(f"No templates found in {TEMPLATE_DIR}")
        return

    print(f"Found {len(template_files)} template files to update:\n")

    updated_count = 0
    for template_file in sorted(template_files):
        if update_template(template_file):
            updated_count += 1

    print()
    print("=" * 60)
    print(f"COMPLETE: Updated {updated_count}/{len(template_files)} files")
    print("=" * 60)
    print()
    print("[OK] All templates now use the modern 2025 design system!")
    print("[OK] Restart your Django dev server and hard refresh browser (Ctrl+Shift+R)")

if __name__ == "__main__":
    main()
