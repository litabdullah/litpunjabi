import json
from django.core.management.base import BaseCommand, CommandError
from home.models import Author

class Command(BaseCommand):
    help = 'Imports authors from JSON file into Wagtail.'

    def add_arguments(self, parser):
        parser.add_argument('json_file_path', type=str, help='Path to authors.json')

    def handle(self, *args, **options):
        json_file_path = options['json_file_path']
        self.stdout.write(self.style.NOTICE(f"Starting author import from {json_file_path}"))

        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                authors_data = data.get('authors', [])
            self.stdout.write(self.style.SUCCESS(f"Loaded {len(authors_data)} authors from JSON."))
        except FileNotFoundError:
            raise CommandError(f"File not found at {json_file_path}")
        except json.JSONDecodeError:
            raise CommandError("Invalid JSON format.")

        created_count = 0
        updated_count = 0

        for author_obj in authors_data:
            author_id = author_obj.get('id')
            if not author_id:
                self.stdout.write(self.style.WARNING("Skipping entry due to missing 'id'."))
                continue

            author, created = Author.objects.update_or_create(
                author_id=author_id,
                defaults={
                    'name': author_obj.get('name') or '',
                    'slug': author_obj.get('slug') or '',
                    'profile_image': author_obj.get('profile_image') or '',
                    'cover_image': author_obj.get('cover_image') or '',
                    'bio': author_obj.get('bio') or '',
                    'website': author_obj.get('website') or '',
                    'location': author_obj.get('location') or '',
                    'facebook': author_obj.get('facebook') or '',
                    'twitter': author_obj.get('twitter') or '',
                    'threads': author_obj.get('threads') or '',
                    'bluesky': author_obj.get('bluesky') or '',
                    'mastodon': author_obj.get('mastodon') or '',
                    'tiktok': author_obj.get('tiktok') or '',
                    'youtube': author_obj.get('youtube') or '',
                    'instagram': author_obj.get('instagram') or '',
                    'linkedin': author_obj.get('linkedin') or '',
                    'meta_title': author_obj.get('meta_title') or '',
                    'meta_description': author_obj.get('meta_description') or '',
                    'original_url': author_obj.get('url') or '',
                }
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Import complete! Created: {created_count}, Updated: {updated_count}"
        ))
