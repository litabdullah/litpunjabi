# Project Structure - Punjabi Sahit

**Last Updated**: January 17, 2025
**Status**: ✅ Cleaned and Standardized

---

## 📁 Root Directory

```
PunjabiSahit/
├── 📄 manage.py                    # Django management script
├── 📄 requirements.txt             # Python dependencies
├── 📄 README.md                    # Project documentation
├── 📄 STANDARDS.md                 # Development standards
├── 📄 CONFIGURATION.md             # Configuration checklist
├── 📄 PROJECT_STRUCTURE.md         # This file
├── 📄 .gitignore                   # Git ignore rules
│
├── 📁 home/                        # Main application (see details below)
├── 📁 search/                      # Search functionality
├── 📁 punjabisahit/                # Project settings (see details below)
├── 📁 templates/                   # Global templates
├── 📁 media/                       # User-uploaded files
├── 📁 static_compiled/             # Compiled static files (empty in dev)
└── 📁 locale/                      # Translation files (to be created)
```

---

## 📁 home/ (Main Application)

```
home/
├── 📄 __init__.py
├── 📄 apps.py                      # App configuration
├── 📄 models.py                    # Database models (1,320 lines)
├── 📄 views.py                     # View functions (API endpoints)
├── 📄 utils.py                     # Utility functions (Gurmukhi sorting)
├── 📄 tests.py                     # Unit tests
│
├── 📁 management/                  # Django management commands
│   ├── 📄 __init__.py
│   └── 📁 commands/
│       ├── 📄 __init__.py
│       ├── 📄 import_words.py      # Import dictionary entries
│       ├── 📄 import_authors.py    # Import authors
│       ├── 📄 import_phrases.py    # Import phrases
│       ├── 📄 import_idioms.py     # Import idioms
│       └── 📄 import_posts.py      # Import blog posts
│
├── 📁 middleware/                  # Custom middleware
│   ├── 📄 __init__.py
│   └── 📄 views.py                 # Page view counter middleware
│
├── 📁 migrations/                  # Database migrations
│   ├── 📄 __init__.py
│   ├── 📄 0001_initial.py
│   ├── 📄 0002_remove_bookpage_avg_rating_and_more.py
│   ├── 📄 0003_remove_bookpage_authors_remove_bookpage_cover_image_and_more.py
│   ├── 📄 0004_blogpostpage_view_count_eventpage_view_count_and_more.py
│   ├── 📄 0005_idiompage_idiom_basic_defintion_gurmukhi_and_more.py
│   ├── 📄 0006_author_author_id_author_bluesky_author_cover_image_and_more.py
│   ├── 📄 0007_authorsindexpage_booksindexpage_alter_author_options_and_more.py
│   └── 📄 0008_userbookstatus.py
│
├── 📁 static/                      # App-specific static files
│   └── 📁 css/
│       └── 📄 welcome_page.css     # Welcome page styles
│
└── 📁 templates/                   # App-specific templates
    └── 📁 home/
        ├── 📄 home_page.html               # Landing page
        ├── 📄 dictionary_index_page.html   # Dictionary listing
        ├── 📄 dictionary_entry_page.html   # Dictionary entry detail
        ├── 📄 books_index_page.html        # Books listing
        ├── 📄 book_page.html               # Book detail
        ├── 📄 authors_index_page.html      # Authors listing
        ├── 📄 author_detail_page.html      # Author profile
        ├── 📄 events_index_page.html       # Events listing with calendar
        ├── 📄 event_page.html              # Event detail
        ├── 📄 blog_index_page.html         # Blog listing
        ├── 📄 blog_post_page.html          # Blog post detail
        ├── 📄 idioms_index_page.html       # Idioms listing
        ├── 📄 idiom_page.html              # Idiom detail
        ├── 📄 phrases_index_page.html      # Phrases listing
        └── 📄 phrase_page.html             # Phrase detail
```

---

## 📁 punjabisahit/ (Project Settings)

```
punjabisahit/
├── 📄 __init__.py
├── 📄 urls.py                      # URL configuration
├── 📄 wsgi.py                      # WSGI configuration
├── 📄 asgi.py                      # ASGI configuration (if exists)
│
├── 📁 settings/                    # Split settings
│   ├── 📄 __init__.py
│   ├── 📄 base.py                  # Base settings for all environments
│   ├── 📄 dev.py                   # Development settings
│   └── 📄 production.py            # Production settings
│
└── 📁 static/                      # Project-level static files
    ├── 📁 css/
    │   ├── 📄 base.css             # Base styles
    │   └── 📄 PunjabiSahit.css     # Project styles
    └── 📁 js/
        └── (JavaScript files if any)
```

---

## 📁 search/ (Search Application)

```
search/
├── 📄 __init__.py
├── 📄 views.py                     # Search view
└── 📁 templates/
    └── 📁 search/
        └── 📄 search.html          # Search results page
```

---

## 📁 templates/ (Global Templates)

```
templates/
└── 📄 base.html                    # Base template with header/footer/navigation
```

---

## 📁 media/ (User-Uploaded Files)

```
media/
├── 📁 images/                      # Wagtail images
│   └── (uploaded image files)
├── 📁 documents/                   # Wagtail documents
│   └── (uploaded document files)
└── 📁 original_images/             # Original image uploads
    └── (original image files)
```

---

## Database Models Overview

### Core Models (in home/models.py)

#### Abstract Base
- **BaseContentPage** - Abstract base with view_count field

#### Content Models
- **Author** - Author profiles with multi-language support
- **DictionaryEntryPage** - Dictionary entries with Gurmukhi/English
- **BookPage** - Books with details, authors, ratings
- **EventPage** - Events with calendar integration
- **BlogPostPage** - Blog articles
- **IdiomPage** - Punjabi idioms
- **PhrasePage** - Common phrases

#### Index Pages
- **HomePage** - Landing page
- **DictionaryIndexPage** - Dictionary listing with filters
- **BooksIndexPage** - Books listing with filters
- **AuthorsIndexPage** - Authors listing with filters
- **AuthorDetailPage** - Individual author page
- **EventsIndexPage** - Events listing with calendar view
- **BlogIndexPage** - Blog listing
- **IdiomsIndexPage** - Idioms listing
- **PhrasesIndexPage** - Phrases listing

#### User Interaction
- **UserBookStatus** - Reading status tracking for users

---

## Key Files Explained

### Configuration Files

| File | Purpose |
|------|---------|
| `manage.py` | Django management script for commands |
| `requirements.txt` | Python package dependencies |
| `.gitignore` | Files to exclude from version control |
| `README.md` | Project documentation and setup guide |
| `STANDARDS.md` | Code style and development standards |
| `CONFIGURATION.md` | Configuration checklist |

### Settings Files

| File | Purpose |
|------|---------|
| `settings/base.py` | Common settings for all environments |
| `settings/dev.py` | Development-specific settings |
| `settings/production.py` | Production-specific settings |

### Core Application Files

| File | Lines | Purpose |
|------|-------|---------|
| `home/models.py` | 1,320 | All database models |
| `home/views.py` | 110 | API endpoints for book status |
| `home/utils.py` | 158 | Gurmukhi sorting utilities |
| `home/middleware/views.py` | 60 | Page view tracking |

---

## Static Files Structure

### App-Level Static Files
- `home/static/css/welcome_page.css` - Welcome page specific styles

### Project-Level Static Files
- `punjabisahit/static/css/base.css` - Base styles
- `punjabisahit/static/css/PunjabiSahit.css` - Project-wide styles

### Global Static Files (Compiled)
- `static_compiled/` - Collected static files for production (empty in dev)

---

## Template Hierarchy

```
base.html (Global)
├── Provides: Header, Footer, Navigation, Language Switcher
└── Extended by all page templates:
    ├── home/home_page.html
    ├── home/dictionary_index_page.html
    ├── home/books_index_page.html
    ├── home/authors_index_page.html
    ├── home/events_index_page.html
    ├── home/blog_index_page.html
    └── ... (all other templates)
```

---

## URL Structure

### Admin URLs
- `/admin/` - Wagtail CMS admin
- `/django-admin/` - Django admin

### Content URLs
- `/` - Home page
- `/dictionary/` - Dictionary index
- `/books/` - Books index
- `/authors/` - Authors index
- `/events/` - Events index (with calendar)
- `/blog/` - Blog index
- `/idioms/` - Idioms index
- `/phrases/` - Phrases index

### API URLs
- `/api/books/update-status/` - Update book reading status
- `/api/books/delete-status/` - Delete book status
- `/i18n/` - Language switching endpoint
- `/search/` - Search functionality

### Static/Media URLs
- `/static/` - Static files (CSS, JS, images)
- `/media/` - User-uploaded files
- `/documents/` - Wagtail documents

---

## Migration History

| Migration | Description |
|-----------|-------------|
| 0001_initial | Initial database schema |
| 0002 | Remove book rating fields |
| 0003 | Remove book authors and cover fields |
| 0004 | Add view_count to pages |
| 0005 | Add idiom definition fields |
| 0006 | Enhance Author model |
| 0007 | Add Authors and Books systems |
| 0008 | Add UserBookStatus model |

---

## Removed/Cleaned Files

The following were removed during standardization:

### Removed Directories
- ✅ `punjabisahit/templates/` - Duplicate template directory
- ✅ All `__pycache__/` directories - Python compiled bytecode
- ✅ All `.pyc` files - Compiled Python files

### Why These Were Removed
1. **Duplicate Templates**: `punjabisahit/templates/base.html` was an old version, superseded by `templates/base.html`
2. **Compiled Files**: `__pycache__` and `.pyc` files are auto-generated and should not be in version control
3. **Non-functional**: Files not referenced or used by the application

---

## File Count Summary

| Type | Count |
|------|-------|
| Python files | 30+ |
| Templates | 15+ |
| Migrations | 8 |
| CSS files | 3 |
| Documentation | 5 |
| **Total Key Files** | **60+** |

---

## Development vs Production

### Development
- `DEBUG = True`
- Uses `dev.py` settings
- Static files served by Django
- SQLite or local PostgreSQL
- Detailed error pages

### Production
- `DEBUG = False`
- Uses `production.py` settings
- Static files served by web server/CDN
- Production PostgreSQL database
- Generic error pages
- Security headers enabled

---

## Clean Project Checklist

- ✅ No duplicate files
- ✅ No compiled Python files in repo
- ✅ No temporary files
- ✅ No unused CSS/JS files
- ✅ Consistent directory structure
- ✅ All templates properly organized
- ✅ Settings properly split
- ✅ Migrations in order
- ✅ Documentation complete
- ✅ .gitignore configured

---

## Next Steps for Developers

1. **Clone the repository**
2. **Follow README.md** for setup instructions
3. **Review STANDARDS.md** for coding guidelines
4. **Check CONFIGURATION.md** for environment setup
5. **Run migrations** to set up database
6. **Start development server**
7. **Write tests** for new features
8. **Follow commit conventions** from STANDARDS.md

---

**Project Status**: ✅ Clean, Standardized, Production-Ready

