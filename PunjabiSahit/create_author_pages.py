#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create AuthorDetailPage for each author that doesn't have one."""
import os
import sys
import django

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'punjabisahit.settings.dev')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from home.models import Author, AuthorDetailPage, AuthorsIndexPage
from django.utils.text import slugify

def create_author_detail_pages():
    """Create detail pages for all authors."""
    # Get the authors index page
    authors_index = AuthorsIndexPage.objects.first()
    if not authors_index:
        print("ERROR: AuthorsIndexPage not found!")
        return

    print(f'Authors index page: {authors_index.title} (ID: {authors_index.id})')

    # Get all authors
    authors = Author.objects.all()
    created_count = 0
    skipped_count = 0

    for author in authors:
        # Check if this author already has a detail page
        if author.detail_pages.exists():
            skipped_count += 1
            continue

        # Create a slug from the author name
        name_for_slug = author.name_english or author.name_gurmukhi or author.name
        slug_base = slugify(name_for_slug)

        # Ensure unique slug
        counter = 1
        slug = slug_base
        while AuthorDetailPage.objects.filter(slug=slug).exists():
            slug = f"{slug_base}-{counter}"
            counter += 1

        try:
            # Create the detail page
            detail_page = AuthorDetailPage(
                title=name_for_slug,
                slug=slug,
                author=author,
            )
            authors_index.add_child(instance=detail_page)
            detail_page.save_revision().publish()
            created_count += 1
            print(f'Created: {name_for_slug} -> /home-page/authors/{slug}/')
        except Exception as e:
            print(f'ERROR creating page for {name_for_slug}: {e}')

    print(f'\n=== Summary ===')
    print(f'Detail pages created: {created_count}')
    print(f'Detail pages skipped (already exist): {skipped_count}')
    print(f'Total detail pages now: {AuthorDetailPage.objects.count()}')

if __name__ == '__main__':
    create_author_detail_pages()
