import json
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.dateparse import parse_datetime
from home.models import BlogIndexPage, BlogPostPage, Author

class Command(BaseCommand):
    help = 'Imports blog posts from JSON file into Wagtail.'

    def add_arguments(self, parser):
        parser.add_argument('json_file_path', type=str, help='Path to posts.json')

    @transaction.atomic
    def handle(self, *args, **options):
        json_file_path = options['json_file_path']
        self.stdout.write(self.style.NOTICE(f"Starting post import from {json_file_path}"))

        try:
            parent_page = BlogIndexPage.objects.live().first()
            if not parent_page:
                raise CommandError("CRITICAL: A 'Blog Index Page' must be created and published first.")
            self.stdout.write(self.style.SUCCESS(f"Found parent page: '{parent_page.title}'"))
        except Exception as e:
            raise CommandError(f"Error finding BlogIndexPage: {e}")

        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                posts_data = data.get('posts', [])
            self.stdout.write(self.style.SUCCESS(f"Loaded {len(posts_data)} posts from JSON."))
        except FileNotFoundError:
            raise CommandError(f"File not found at {json_file_path}")
        except json.JSONDecodeError:
            raise CommandError("Invalid JSON format.")

        created_count = 0
        skipped_count = 0

        for post_obj in posts_data:
            post_id = post_obj.get('id')
            if not post_id:
                self.stdout.write(self.style.WARNING("Skipping entry due to missing 'id'."))
                continue

            if BlogPostPage.objects.filter(post_id=post_id).exists():
                skipped_count += 1
                continue

            new_post_page = BlogPostPage(
                title=post_obj.get('title', 'Untitled')[:255],
                post_id=post_id,
                uuid=post_obj.get('uuid'),
                comment_id=post_obj.get('comment_id') or '',
                intro=(post_obj.get('custom_excerpt') or post_obj.get('excerpt') or '')[:500],
                html_content=post_obj.get('html') or '',
                excerpt=post_obj.get('excerpt') or '',
                reading_time=post_obj.get('reading_time') or 0,
                feature_image_url=post_obj.get('feature_image') or '',
                feature_image_alt=post_obj.get('feature_image_alt') or '',
                feature_image_caption=post_obj.get('feature_image_caption') or '',
                featured=post_obj.get('featured', False),
                visibility=post_obj.get('visibility') or 'public',
                published_at=parse_datetime(post_obj.get('published_at')) if post_obj.get('published_at') else None,
                updated_at=parse_datetime(post_obj.get('updated_at')) if post_obj.get('updated_at') else None,
                access=post_obj.get('access', True),
                comments=post_obj.get('comments', True),
                codeinjection_head=post_obj.get('codeinjection_head') or '',
                codeinjection_foot=post_obj.get('codeinjection_foot') or '',
                meta_title=post_obj.get('meta_title') or '',
                meta_description=post_obj.get('meta_description') or '',
                og_image=post_obj.get('og_image') or '',
                og_title=post_obj.get('og_title') or '',
                og_description=post_obj.get('og_description') or '',
                twitter_image=post_obj.get('twitter_image') or '',
                twitter_title=post_obj.get('twitter_title') or '',
                twitter_description=post_obj.get('twitter_description') or '',
                custom_template=post_obj.get('custom_template') or '',
                canonical_url=post_obj.get('canonical_url') or '',
                original_url=post_obj.get('url') or '',
                email_subject=post_obj.get('email_subject') or '',
                frontmatter=post_obj.get('frontmatter') or '',
            )

            parent_page.add_child(instance=new_post_page)
            new_post_page.save_revision().publish()
            created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Import complete! Created: {created_count}, Skipped: {skipped_count}"
        ))
