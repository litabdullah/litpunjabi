# Punjabi Sahit - Project Standards & Guidelines

## Table of Contents
1. [Code Style](#code-style)
2. [Python Standards](#python-standards)
3. [Django/Wagtail Standards](#djangowagtail-standards)
4. [Template Standards](#template-standards)
5. [JavaScript Standards](#javascript-standards)
6. [Git Commit Standards](#git-commit-standards)
7. [Documentation Standards](#documentation-standards)

---

## Code Style

### General Principles
- **Readability over cleverness**: Code should be self-documenting
- **DRY (Don't Repeat Yourself)**: Extract common functionality
- **KISS (Keep It Simple, Stupid)**: Prefer simple solutions
- **Consistency**: Follow existing patterns in the codebase

### Line Length
- Maximum 100 characters per line
- Break long lines logically at commas, operators, or method calls

---

## Python Standards

### Style Guide
- Follow **PEP 8** style guide
- Use **4 spaces** for indentation (no tabs)
- Use **snake_case** for variables and functions
- Use **PascalCase** for classes
- Use **UPPER_CASE** for constants

### Imports
Order imports in the following groups, separated by blank lines:

```python
# Standard library imports
import os
import sys
from datetime import datetime

# Third-party imports
from django.db import models
from wagtail.models import Page

# Local application imports
from .models import MyModel
from .utils import my_function
```

### Docstrings
All modules, classes, and functions must have docstrings:

```python
def calculate_progress(current_page, total_pages):
    """
    Calculate reading progress as a percentage.

    Args:
        current_page (int): Current page number
        total_pages (int): Total number of pages

    Returns:
        int: Progress percentage (0-100)

    Raises:
        ValueError: If total_pages is zero or negative
    """
    if total_pages <= 0:
        raise ValueError("Total pages must be positive")
    return min(int((current_page / total_pages) * 100), 100)
```

### Type Hints (Recommended)
```python
from typing import List, Optional

def get_books(author_id: int, limit: Optional[int] = None) -> List[BookPage]:
    """Get books by author with optional limit."""
    books = BookPage.objects.filter(author_id=author_id)
    if limit:
        books = books[:limit]
    return list(books)
```

---

## Django/Wagtail Standards

### Model Standards

#### Field Organization
Organize model fields in this order:
1. Relationships (ForeignKey, ManyToMany)
2. Core fields
3. Metadata fields
4. Timestamps

```python
class BookPage(BaseContentPage):
    """Individual book page with full details."""

    # Relationships
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    # Core fields
    title_gurmukhi = models.CharField(max_length=500)
    title_english = models.CharField(max_length=500, blank=True)
    cover_image = models.ForeignKey('wagtailimages.Image', ...)

    # Metadata
    publication_year = models.PositiveIntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=20, blank=True)

    # Timestamps (if not inherited)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### Model Methods
- Use `__str__()` for string representation
- Use `@property` for computed fields
- Use `get_absolute_url()` for URL generation
- Prefix private methods with underscore

```python
def __str__(self):
    return self.title_english or self.title_gurmukhi

@property
def progress_percentage(self):
    """Calculate reading progress."""
    return self._calculate_progress()

def _calculate_progress(self):
    """Private helper method."""
    if self.pages and self.current_page:
        return min(int((self.current_page / self.pages) * 100), 100)
    return 0
```

### View Standards

#### Function-Based Views
```python
@login_required
@require_POST
def update_status(request):
    """
    Update user's reading status for a book.

    This endpoint expects JSON data and returns JSON response.
    """
    try:
        data = json.loads(request.body)
        # Process data
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
```

#### URL Naming
- Use descriptive names
- Use underscores, not hyphens
- Group related URLs

```python
urlpatterns = [
    # Books API
    path('api/books/status/', update_book_status, name='update_book_status'),
    path('api/books/favorite/', toggle_favorite, name='toggle_book_favorite'),

    # Authors API
    path('api/authors/follow/', follow_author, name='follow_author'),
]
```

---

## Template Standards

### File Organization
```
templates/
├── base.html                 # Base template
├── home/                     # App-specific templates
│   ├── home_page.html
│   ├── book_page.html
│   └── author_detail_page.html
└── components/               # Reusable components
    ├── header.html
    └── footer.html
```

### Template Naming
- Use **snake_case** for template names
- Match model names: `BookPage` → `book_page.html`
- Use suffixes: `_list.html`, `_detail.html`, `_form.html`

### Template Structure
```django
{% extends "base.html" %}
{% load wagtailcore_tags wagtailimages_tags i18n %}

{% block title %}{{ page.title }} | Punjabi Sahit{% endblock %}

{% block extra_css %}
<style>
    /* Page-specific styles */
</style>
{% endblock %}

{% block content %}
<main>
    <!-- Content here -->
</main>
{% endblock %}

{% block extra_js %}
<script>
    // Page-specific JavaScript
</script>
{% endblock %}
```

### Template Best Practices
- Always load required template tags at the top
- Use meaningful variable names
- Comment complex logic
- Keep templates DRY with includes and components
- Use `{% trans %}` for translatable strings

```django
{# Good: Clear, semantic HTML with proper indentation #}
<article class="book-card">
    <h2 class="book-title">{{ book.title }}</h2>
    <p class="book-author">{% trans "By" %} {{ book.author }}</p>
</article>

{# Bad: Unclear structure, no indentation #}
<div class="card"><h2>{{book.title}}</h2><p>{{book.author}}</p></div>
```

---

## JavaScript Standards

### Code Style
- Use **camelCase** for variables and functions
- Use **PascalCase** for classes
- Use **const** and **let**, avoid **var**
- Use template literals for strings

```javascript
// Good
const bookTitle = 'Punjabi Literature';
const updateStatus = (bookId, status) => {
    console.log(`Updating book ${bookId} to ${status}`);
};

// Bad
var book_title = 'Punjabi Literature';
function update_status(book_id, status) {
    console.log('Updating book ' + book_id + ' to ' + status);
}
```

### AJAX Standards
```javascript
// Use fetch API with proper error handling
async function updateBookStatus(bookId, status) {
    try {
        const response = await fetch('/api/books/update-status/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ book_id: bookId, status: status }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error updating book status:', error);
        throw error;
    }
}
```

---

## Git Commit Standards

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, no logic change)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples
```
feat(books): add reading status tracking

Implement user book status model with tracking for:
- Reading status (to read, reading, read, completed)
- Favorites
- Current page and progress
- Ratings and notes

Closes #123

---

fix(dictionary): correct phonetic sorting for Gurmukhi

The previous sorting didn't account for vowel diacritics properly.
Updated the sort key generation to include all Gurmukhi characters.

---

docs(README): update installation instructions

Added steps for setting up PostgreSQL and running migrations.
```

---

## Documentation Standards

### Code Comments
```python
# Good: Explains WHY, not WHAT
# Use F() expression to avoid race conditions during concurrent updates
page_model.objects.filter(pk=page.pk).update(view_count=F('view_count') + 1)

# Bad: States the obvious
# Increment view count by 1
view_count = view_count + 1
```

### README Structure
Every major component should have a README:
```markdown
# Component Name

## Overview
Brief description of what this component does.

## Installation
Steps to install or set up.

## Usage
How to use this component with examples.

## API Reference
If applicable, document the API.

## Configuration
Available configuration options.

## Contributing
Guidelines for contributors.
```

### Inline Documentation
- Document complex algorithms
- Explain business logic
- Note important edge cases
- Link to related issues/tickets

```python
def gurmukhi_sort_key(text):
    """
    Generate a sort key for Gurmukhi text.

    The Gurmukhi alphabet has a specific order that differs from
    Unicode code points. This function maps each character to its
    proper position in the alphabet for correct sorting.

    Reference: Punjabi Language Grammar, Chapter 2
    Issue: #456 - Dictionary sorting incorrect

    Args:
        text (str): Gurmukhi text to sort

    Returns:
        tuple: Sort key tuple
    """
```

---

## File Organization

### Project Structure
```
PunjabiSahit/
├── home/                      # Main Django app
│   ├── management/            # Management commands
│   ├── middleware/            # Custom middleware
│   ├── migrations/            # Database migrations
│   ├── static/                # App-specific static files
│   ├── templates/             # App-specific templates
│   ├── models.py              # Database models
│   ├── views.py               # View functions
│   ├── urls.py                # URL patterns
│   ├── utils.py               # Utility functions
│   └── tests.py               # Unit tests
├── templates/                 # Global templates
├── static/                    # Global static files
├── media/                     # User-uploaded files
├── punjabisahit/              # Project settings
│   └── settings/
│       ├── base.py            # Base settings
│       ├── dev.py             # Development settings
│       └── production.py      # Production settings
├── .gitignore
├── requirements.txt
├── README.md
└── STANDARDS.md               # This file
```

---

## Testing Standards

### Test Organization
```python
from django.test import TestCase
from .models import BookPage, Author

class BookPageTestCase(TestCase):
    """Test cases for BookPage model."""

    def setUp(self):
        """Set up test data."""
        self.author = Author.objects.create(name_english="Test Author")

    def test_progress_calculation(self):
        """Test that progress percentage is calculated correctly."""
        book = BookPage.objects.create(
            title_english="Test Book",
            pages=100,
            author=self.author
        )
        # Test logic here

    def tearDown(self):
        """Clean up after tests."""
        pass
```

### Test Naming
- Use descriptive test names: `test_<what>_<condition>_<expected>`
- Example: `test_book_status_updated_successfully`

---

## Performance Guidelines

### Database Queries
- Use `select_related()` for ForeignKey
- Use `prefetch_related()` for ManyToMany
- Use `only()` to limit fields
- Use `F()` expressions for atomic updates

```python
# Good: Optimized query
books = BookPage.objects.select_related('author').prefetch_related('tags')

# Bad: N+1 query problem
books = BookPage.objects.all()
for book in books:
    print(book.author.name)  # Triggers query for each book
```

### Caching
- Cache expensive computations
- Use Django's cache framework
- Set appropriate cache timeouts

---

## Security Guidelines

### Always
- ✅ Use CSRF tokens for forms
- ✅ Validate and sanitize user input
- ✅ Use `@login_required` for protected views
- ✅ Use parameterized queries (Django ORM does this)
- ✅ Keep SECRET_KEY secure
- ✅ Use HTTPS in production

### Never
- ❌ Store passwords in plain text
- ❌ Trust user input without validation
- ❌ Expose sensitive data in logs
- ❌ Use `eval()` or `exec()` on user input
- ❌ Commit secrets to version control

---

## Accessibility Guidelines

### HTML
- Use semantic HTML elements
- Provide alt text for images
- Use proper heading hierarchy (h1 → h2 → h3)
- Ensure sufficient color contrast

### Forms
- Label all form fields
- Provide helpful error messages
- Support keyboard navigation
- Use appropriate input types

---

## Internationalization (i18n)

### Marking Strings for Translation
```python
# In Python
from django.utils.translation import gettext_lazy as _

class BookPage(Page):
    help_text = _("Enter the book title in Gurmukhi script")

# In templates
{% load i18n %}
<h1>{% trans "Welcome to Punjabi Sahit" %}</h1>
<p>{% blocktrans %}Hello {{ username }}{% endblocktrans %}</p>
```

### Language Files
- Keep translations organized
- Use context when needed
- Provide translator comments for unclear strings

---

## Conclusion

These standards ensure:
- **Consistency** across the codebase
- **Maintainability** for future development
- **Collaboration** among team members
- **Quality** in the final product

All contributors should read and follow these standards. When in doubt, refer to existing code or ask the team.

**Last Updated**: 2025-01-17
**Version**: 1.0.0
