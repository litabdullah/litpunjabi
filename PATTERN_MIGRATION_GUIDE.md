# Pattern Migration Guide
**Punjabi Sahit - FT Origami Design System**

## Overview

Successfully migrated 4 key UI patterns from `base_preview.css` to `ft-origami.css` with proper `ft-` prefix naming. This guide shows you how to use these patterns instead of inline styles.

---

## ✅ Migrated Patterns

### 1. **Hero Layout Pattern**
Two-column responsive hero section for landing pages

**Classes Added:**
- `.ft-hero` - Main hero grid container
- `.ft-hero-title` - Large headline text
- `.ft-hero-subtitle` - Supporting description
- `.ft-hero-actions` - Button group container
- `.ft-hero-meta` - Statistics display
- `.ft-stat-number` - Stat value (e.g., "60,000+")
- `.ft-stat-label` - Stat description
- `.ft-hero-panel` - Featured content card
- `.ft-pill` - Badge/tag component

**Example Usage:**
```html
<section class="ft-hero">
    <div class="ft-hero-text">
        <h1 class="ft-hero-title">Explore Punjabi Literature</h1>
        <p class="ft-hero-subtitle">
            Discover words, idioms, books, and cultural heritage.
        </p>
        <div class="ft-hero-actions">
            <a href="#" class="o-buttons o-buttons__primary">Browse Dictionary</a>
            <a href="#" class="o-buttons o-buttons__secondary">View Idioms</a>
        </div>
        <div class="ft-hero-meta">
            <div>
                <span class="ft-stat-number">60,000+</span>
                <span class="ft-stat-label">Word Entries</span>
            </div>
            <div>
                <span class="ft-stat-number">1,500+</span>
                <span class="ft-stat-label">Idioms</span>
            </div>
        </div>
    </div>

    <div class="ft-hero-panel">
        <span class="ft-pill">Featured</span>
        <!-- Featured content here -->
    </div>
</section>
```

---

### 2. **Two-Column Detail Layout**
Main content + sidebar for entry/detail pages (dictionary, phrases, books)

**Classes Added:**
- `.ft-two-column` - Responsive 2-column grid
- `.ft-column` - Column container
- `.ft-column--side` - Sidebar (sticky on desktop)
- `.ft-entry-header` - Entry page header layout
- `.ft-entry-main` - Primary headword (Gurmukhi)
- `.ft-entry-sub` - Secondary script
- `.ft-entry-roman` - Romanization
- `.ft-entry-body` - Main content area
- `.ft-tabs` - Tab navigation container
- `.ft-tab` - Individual tab button
- `.ft-tab--active` - Active tab state
- `.ft-badge` - Category/type badge
- `.ft-meta-list` - Metadata list with proper spacing

**Example Usage:**
```html
<div class="ft-two-column">
    <!-- Main Content Column -->
    <div class="ft-column">
        <div class="ft-entry-header">
            <div>
                <div class="ft-entry-main gurmukhi">ਸਿੱਖਿਆ</div>
                <div class="ft-entry-sub shahmukhi">سکھیا</div>
                <div class="ft-entry-roman">Sikhia — education</div>
            </div>
            <span class="ft-badge">Noun</span>
        </div>

        <div class="ft-tabs">
            <button class="ft-tab ft-tab--active">Definition</button>
            <button class="ft-tab">Examples</button>
            <button class="ft-tab">Related</button>
        </div>

        <div class="ft-entry-body ft-rich-text">
            <p>Formal or informal process of acquiring knowledge.</p>
            <ul>
                <li>Example sentence 1</li>
                <li>Example sentence 2</li>
            </ul>
        </div>
    </div>

    <!-- Sidebar Column -->
    <aside class="ft-column ft-column--side">
        <div class="ft-card">
            <h3>Metadata</h3>
            <dl class="ft-meta-list">
                <div>
                    <dt>Category</dt>
                    <dd>Education</dd>
                </div>
                <div>
                    <dt>Origin</dt>
                    <dd>Sanskrit-derived</dd>
                </div>
                <div>
                    <dt>Added</dt>
                    <dd>2024-10-01</dd>
                </div>
            </dl>
        </div>

        <div class="ft-card">
            <h3>Related</h3>
            <ul class="ft-list">
                <li><a href="#">Related word 1</a></li>
                <li><a href="#">Related word 2</a></li>
            </ul>
        </div>
    </aside>
</div>
```

---

### 3. **Table + Toolbar Pattern**
Filterable, sortable data tables with search/filter toolbar

**Classes Added:**
- `.ft-table-toolbar` - Filter/search bar above table
- `.ft-table-actions` - Action button group
- `.ft-table-wrapper` - Table container with styling
- `.ft-table` - Data table
- `.ft-input` - Text input (rounded, proper styling)
- `.ft-select` - Dropdown select

**Example Usage:**
```html
<!-- Toolbar with search and filters -->
<div class="ft-table-toolbar">
    <input type="text" class="ft-input" placeholder="Search phrases...">
    <div class="ft-table-actions">
        <select class="ft-select">
            <option>Sort by: Latest</option>
            <option>Sort by: A–Z</option>
            <option>Sort by: Popular</option>
        </select>
        <button class="o-buttons o-buttons__secondary">Filters</button>
    </div>
</div>

<!-- Table -->
<div class="ft-table-wrapper">
    <table class="ft-table">
        <thead>
            <tr>
                <th>Phrase</th>
                <th>Translation</th>
                <th>Category</th>
                <th>Views</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ</td>
                <td>The Khalsa belongs to God</td>
                <td>Formal</td>
                <td>1,234</td>
            </tr>
            <!-- More rows -->
        </tbody>
    </table>
</div>
```

---

### 4. **Footer Grid Enhancement**
Responsive 4-column footer layout

**Classes Added:**
- `.ft-footer-grid` - Responsive footer grid (1→2→4 columns)
- `.ft-footer-column` - Individual column
- `.ft-footer-title` - Column heading
- `.ft-footer-text` - Description text
- `.ft-footer-bottom` - Copyright/legal section

**Example Usage:**
```html
<footer class="ft-footer">
    <div class="ft-container">
        <div class="ft-footer-grid">
            <div class="ft-footer-column">
                <div class="ft-footer-title">Punjabi Sahit</div>
                <div class="ft-footer-text">
                    A digital platform for Punjabi language preservation.
                </div>
            </div>

            <div class="ft-footer-column">
                <div class="ft-footer__heading">Sections</div>
                <a href="#" class="ft-footer__link">Dictionary</a>
                <a href="#" class="ft-footer__link">Idioms</a>
                <a href="#" class="ft-footer__link">Books</a>
            </div>

            <div class="ft-footer-column">
                <div class="ft-footer__heading">Community</div>
                <a href="#" class="ft-footer__link">Contributors</a>
                <a href="#" class="ft-footer__link">Submit a word</a>
            </div>

            <div class="ft-footer-column">
                <div class="ft-footer__heading">Legal</div>
                <a href="#" class="ft-footer__link">Terms</a>
                <a href="#" class="ft-footer__link">Privacy</a>
            </div>
        </div>

        <div class="ft-footer-bottom">
            <span>© 2025 Punjabi Sahit. All rights reserved.</span>
        </div>
    </div>
</footer>
```

---

## 🔄 Migration Strategy

### **BEFORE (Inline Styles - Don't Do This):**
```html
<section style="border: 3px solid var(--ft-color-slate); border-radius: var(--ft-radius-xl); box-shadow: var(--ft-shadow-lg); background-color: var(--ft-bg-card); padding: var(--ft-space-6) var(--ft-space-4); margin-bottom: var(--ft-space-12);">
    <h1 style="font-family: var(--ft-font-headline); font-size: 2rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: var(--ft-color-slate); padding: var(--ft-space-6); border-bottom: 3px solid rgba(13, 118, 128, 0.2); margin-bottom: var(--ft-space-6);">
        {{ page.title }}
    </h1>
</section>
```

### **AFTER (CSS Classes - Do This):**
```html
<section class="ft-card ft-card--prominent ft-space-3xl">
    <h1 class="ft-section-heading">{{ page.title }}</h1>
</section>
```

---

## 📋 Complete Class Reference

### Layout & Structure
- `.ft-container` - Max-width container with padding
- `.ft-grid`, `.ft-grid--2`, `.ft-grid--3`, `.ft-grid--4` - Responsive grids
- `.ft-hero` - Hero section layout
- `.ft-two-column` - 2-column detail layout

### Cards & Containers
- `.ft-card` - Basic card
- `.ft-card--elevated` - Card with larger shadow
- `.ft-card--prominent` - Card with gradient background
- `.ft-headword-card` - Dictionary entry card
- `.ft-section-card` - Section container
- `.ft-hero-panel` - Featured content panel

### Typography & Content
- `.ft-section-heading` - Section title
- `.ft-entry-main`, `.ft-entry-sub`, `.ft-entry-roman` - Entry headers
- `.ft-rich-text` - Rich text content formatting
- `.gurmukhi` - Gurmukhi script font

### Interactive Elements
- `.o-buttons`, `.o-buttons__primary`, `.o-buttons__secondary` - Buttons
- `.ft-tabs`, `.ft-tab`, `.ft-tab--active` - Tab navigation
- `.ft-input` - Text input
- `.ft-select` - Dropdown select

### Tables
- `.ft-table-toolbar` - Table toolbar
- `.ft-table-wrapper` - Table container
- `.ft-table` - Data table

### Metadata & Tags
- `.ft-badge` - Category badge
- `.ft-pill` - Small badge/tag
- `.ft-meta-list` - Metadata definition list

### Lists
- `.ft-list` - Clean link list
- `.ft-hero-meta` - Statistics display

### Spacing Utilities
- `.ft-space-sm` through `.ft-space-6xl` - Bottom margin utilities
- `.ft-py-sm`, `.ft-py-md`, `.ft-py-lg` - Vertical padding
- `.ft-mt-*`, `.ft-mb-*` - Margin utilities

---

## 🎯 Next Steps

1. **Review your index pages** (dictionary_index_page.html, phrases_index_page.html, etc.)
2. **Replace inline styles** with the appropriate CSS classes
3. **Remove custom `<style>` blocks** in templates where patterns now exist in ft-origami.css
4. **Use `.ft-card` instead** of custom styled divs
5. **Apply `.ft-two-column`** layout to detail pages
6. **Use `.ft-table-toolbar` and `.ft-table`** for index pages with filtering

## Benefits

✅ **Consistency** - Same design everywhere
✅ **Maintainability** - Update once in CSS, applies everywhere
✅ **Performance** - Less inline CSS = smaller HTML
✅ **Responsive** - All patterns have mobile breakpoints built-in
✅ **Accessible** - Proper semantic HTML with ARIA support

---

**File Locations:**
- Main CSS: `C:\src\PunjabiSahit\static\css\ft-origami.css`
- Pattern Examples: `C:\src\base_preview.html`
- Templates: `C:\src\PunjabiSahit\home\templates\home\*`
