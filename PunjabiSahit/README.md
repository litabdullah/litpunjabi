# Punjabi Sahit - ਪੰਜਾਬੀ ਸਾਹਿਤ

> A comprehensive Punjabi language learning and literature platform built with Django and Wagtail CMS.

[![Django](https://img.shields.io/badge/Django-5.2.7-green.svg)](https://www.djangoproject.com/)
[![Wagtail](https://img.shields.io/badge/Wagtail-6.x-blue.svg)](https://wagtail.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Overview

Punjabi Sahit is a modern web application designed to promote and preserve Punjabi language and literature. It provides a comprehensive platform for:

- **Dictionary**: Searchable Punjabi-English dictionary with phonetic sorting
- **Literature**: Books, authors, and literary works in Punjabi
- **Learning**: Idioms, phrases, and language resources
- **Community**: Blog posts, events, and cultural content
- **Multilingual**: Support for English, हिन्दी (Hindi), and ਪੰਜਾਬੀ (Punjabi)

---

## ✨ Features

### Core Features
- 📚 **Comprehensive Dictionary** with 10,000+ entries
- 🔍 **Advanced Search** with phonetic Gurmukhi sorting
- 📖 **Books Management** with reading status tracking
- ✍️ **Authors Database** with biographical information
- 📅 **Events Calendar** with multiple view options
- 🌐 **Multilingual Support** (English/Hindi/Punjabi)
- 👤 **User Accounts** with personalized features

### Technical Features
- ⚡ **Fast Performance** with optimized queries
- 📱 **Responsive Design** for all devices
- 🎨 **Modern UI** with Tailwind CSS
- 🔒 **Secure** authentication and authorization
- 📊 **Analytics** with view count tracking
- 🔄 **RESTful API** for external integrations

### Recent Additions
- ✅ **Reading Status System** - Track books (To Read, Reading, Completed)
- ✅ **Origin-Based Filters** - Filter words by language origin
- ✅ **Calendar View** - Interactive FullCalendar.js integration
- ✅ **Phonetic Sorting** - Proper Gurmukhi alphabetical order
- ✅ **Language Switcher** - Universal header toggle for languages

---

## 🛠 Tech Stack

### Backend
- **Django 5.2.7** - Web framework
- **Wagtail 6.x** - CMS framework
- **PostgreSQL 15** - Database
- **Python 3.11+** - Programming language

### Frontend
- **Tailwind CSS** - Utility-first CSS framework
- **FullCalendar.js** - Event calendar
- **Vanilla JavaScript** - No heavy framework dependencies
- **Responsive Design** - Mobile-first approach

### DevOps
- **Git** - Version control
- **pip** - Package management
- **Virtual Environment** - Isolated Python environment

---

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- PostgreSQL 15 or higher
- Git
- pip and virtualenv

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd PunjabiSahit
```

### Step 2: Create Virtual Environment
```bash
# On Windows
python -m venv ../venv
..\venv\Scripts\activate

# On macOS/Linux
python3 -m venv ../venv
source ../venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Database Setup
```bash
# Create PostgreSQL database
createdb punjabisahit_db

# Create database user
psql -c "CREATE USER punjabisahit_user WITH PASSWORD 'admin123';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE punjabisahit_db TO punjabisahit_user;"

# Run migrations
python manage.py migrate
```

### Step 5: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 6: Load Initial Data (Optional)
```bash
# Import dictionary entries
python manage.py import_words

# Import authors
python manage.py import_authors

# Import phrases
python manage.py import_phrases

# Import idioms
python manage.py import_idioms
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to see the application.

---

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# Database
DB_NAME=punjabisahit_db
DB_USER=punjabisahit_user
DB_PASSWORD=admin123
DB_HOST=localhost
DB_PORT=5432

# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Wagtail
WAGTAIL_SITE_NAME=Punjabi Sahit
WAGTAILADMIN_BASE_URL=http://localhost:8000
```

### Settings Files
The project uses split settings:

- `punjabisahit/settings/base.py` - Base settings for all environments
- `punjabisahit/settings/dev.py` - Development-specific settings
- `punjabisahit/settings/production.py` - Production-specific settings

---

## 📖 Usage

### Admin Interface
Access the Wagtail admin at: `http://localhost:8000/admin/`

### Key URLs
- **Home**: `/`
- **Dictionary**: `/dictionary/`
- **Books**: `/books/`
- **Authors**: `/authors/`
- **Events**: `/events/`
- **Blog**: `/blog/`
- **Idioms**: `/idioms/`
- **Phrases**: `/phrases/`

### API Endpoints
- `POST /api/books/update-status/` - Update book reading status
- `POST /api/books/delete-status/` - Delete book status
- `POST /i18n/setlang/` - Change language preference

---

## 📁 Project Structure

```
PunjabiSahit/
├── home/                          # Main Django app
│   ├── management/                # Management commands
│   │   └── commands/
│   │       ├── import_words.py
│   │       ├── import_authors.py
│   │       └── ...
│   ├── middleware/                # Custom middleware
│   │   └── views.py              # Page view counter
│   ├── migrations/                # Database migrations
│   ├── static/                    # App-specific static files
│   ├── templates/                 # App-specific templates
│   │   └── home/
│   │       ├── book_page.html
│   │       ├── author_detail_page.html
│   │       └── ...
│   ├── models.py                  # Database models
│   ├── views.py                   # View functions
│   ├── utils.py                   # Utility functions
│   └── apps.py
├── search/                        # Search functionality
├── templates/                     # Global templates
│   └── base.html                 # Base template
├── static/                        # Global static files
├── media/                         # User-uploaded files
├── punjabisahit/                  # Project settings
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── locale/                        # Translation files
├── requirements.txt               # Python dependencies
├── manage.py                      # Django management script
├── README.md                      # This file
└── STANDARDS.md                   # Development standards
```

---

## 🔌 API Documentation

### Update Book Status
Updates a user's reading status for a book.

**Endpoint**: `POST /api/books/update-status/`

**Authentication**: Required (login_required)

**Request Body**:
```json
{
  "book_id": 123,
  "status": "reading",
  "is_favorite": true,
  "current_page": 45,
  "rating": 5,
  "notes": "Great book!"
}
```

**Response**:
```json
{
  "success": true,
  "status": "Currently Reading",
  "is_favorite": true,
  "progress_percentage": 45,
  "rating": 5
}
```

**Status Codes**:
- `200`: Success
- `400`: Bad request (invalid data)
- `404`: Book not found
- `401`: Unauthorized (not logged in)

---

## 🎨 Features in Detail

### 1. Dictionary System
- **10,000+ entries** with Gurmukhi and English definitions
- **Phonetic sorting** using proper Punjabi alphabetical order
- **Advanced filters**: Part of speech, origin, content type
- **Search** by word or definition
- **Audio pronunciation** for select words

### 2. Books Management
- **Comprehensive book database** with authors, publishers, ISBN
- **Reading status tracking**: To Read, Reading, Read, Completed
- **Progress tracking** with current page
- **5-star rating system**
- **Personal notes** for each book
- **Favorites** functionality

### 3. Authors System
- **Author profiles** with biography, photo, dates
- **Multi-language support** (Gurmukhi, English, Hindi)
- **Literary style** and awards
- **Social media links**
- **View counter** for popularity tracking
- **Related content**: Books, blog posts, events

### 4. Events Calendar
- **FullCalendar.js integration** for interactive calendar
- **Multiple views**: Month, Week, List
- **Event details**: Location, speakers, description
- **Filter by date range**
- **Click to view event details**

### 5. Multilingual Support
- **Three languages**: English, हिन्दी, ਪੰਜਾਬੀ
- **Universal language switcher** in header
- **Django i18n framework** for translations
- **Persistent language preference**
- **All UI text translatable**

---

## 📊 Database Models

### Core Models
- **DictionaryEntryPage** - Dictionary entries
- **BookPage** - Books with details
- **Author** - Author profiles
- **EventPage** - Events and programs
- **BlogPostPage** - Blog articles
- **IdiomPage** - Punjabi idioms
- **PhrasePage** - Common phrases

### User Models
- **UserBookStatus** - Reading status tracking
- **User** - Django's built-in user model

### Page Models (Wagtail)
- **HomePage** - Landing page
- **DictionaryIndexPage** - Dictionary listing
- **BooksIndexPage** - Books listing
- **AuthorsIndexPage** - Authors listing
- **EventsIndexPage** - Events listing
- **BlogIndexPage** - Blog listing

---

## 🧪 Testing

Run tests with:
```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test home

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 🚀 Deployment

### Prepare for Production
1. Set `DEBUG = False` in production settings
2. Update `SECRET_KEY` to a secure random value
3. Configure `ALLOWED_HOSTS`
4. Set up proper database credentials
5. Configure static files serving (WhiteNoise or CDN)
6. Set up SSL/HTTPS
7. Configure email backend
8. Set up logging

### Deploy with Gunicorn
```bash
pip install gunicorn
gunicorn punjabisahit.wsgi:application --bind 0.0.0.0:8000
```

### Collect Static Files
```bash
python manage.py collectstatic --no-input
```

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Follow the [STANDARDS.md](STANDARDS.md)** coding guidelines
4. **Write tests** for new features
5. **Commit your changes**: `git commit -m 'feat: add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Commit Message Format
We use conventional commits:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

---

## 📝 Development Guidelines

See [STANDARDS.md](STANDARDS.md) for comprehensive development standards including:
- Code style and formatting
- Python and Django best practices
- Template and JavaScript standards
- Git commit conventions
- Documentation requirements

---

## 🐛 Known Issues

None at the moment. Please report issues on the GitHub issue tracker.

---

## 📅 Roadmap

### Upcoming Features
- [ ] Advanced search with filters
- [ ] User profile pages
- [ ] Discussion forums
- [ ] Audio lessons
- [ ] Quiz system
- [ ] Mobile apps (iOS/Android)
- [ ] API for third-party integrations

---

## 📄 License

This project is proprietary. All rights reserved.

---

## 👥 Team

- **Development Team**: [Your Team Name]
- **Project Manager**: [Name]
- **Lead Developer**: [Name]

---

## 📞 Contact

- **Website**: [https://punjabisahit.com](https://punjabisahit.com)
- **Email**: contact@punjabisahit.com
- **GitHub**: [Repository URL]

---

## 🙏 Acknowledgments

- Punjabi language community for content contributions
- Django and Wagtail communities for excellent frameworks
- All contributors and supporters

---

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Wagtail Documentation](https://docs.wagtail.org/)
- [Punjabi Grammar Reference](https://punjabi-grammar.com/)
- [Gurmukhi Unicode Chart](https://unicode.org/charts/PDF/U0A00.pdf)

---

**Made with ❤️ for the Punjabi community**

*Last Updated: January 17, 2025*
