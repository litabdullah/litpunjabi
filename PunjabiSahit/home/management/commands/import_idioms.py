import json
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from home.models import IdiomsIndexPage, IdiomPage

class Command(BaseCommand):
    help = 'Imports idioms from a JSON file into Wagtail.'

    def add_arguments(self, parser):
        parser.add_argument('json_file_path', type=str, help='The path to the idioms.json file.')

    @transaction.atomic
    def handle(self, *args, **options):
        json_file_path = options['json_file_path']
        self.stdout.write(self.style.NOTICE(f"Starting idiom import from {json_file_path}"))

        try:
            parent_page = IdiomsIndexPage.objects.live().first()
            if not parent_page:
                raise CommandError("CRITICAL: An 'Idioms Index Page' must be created and published in the Wagtail admin first.")
            self.stdout.write(self.style.SUCCESS(f"Found parent page: '{parent_page.title}'"))
        except Exception as e:
            raise CommandError(f"Error finding IdiomsIndexPage: {e}")

        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                idioms_data = json.load(f)
            self.stdout.write(self.style.SUCCESS(f"Loaded {len(idioms_data)} idioms from JSON."))
        except FileNotFoundError:
            raise CommandError(f"File not found at {json_file_path}")
        except json.JSONDecodeError:
            raise CommandError("Invalid JSON format.")

        created_count = 0
        skipped_count = 0
        
        for idiom_obj in idioms_data:
            idiom_id = idiom_obj.get('idiom_id')
            if not idiom_id:
                self.stdout.write(self.style.WARNING("Skipping entry due to missing 'idiom_id'."))
                continue

            if IdiomPage.objects.filter(idiom_id=idiom_id).exists():
                skipped_count += 1
                continue

            new_idiom_page = IdiomPage(
                title=idiom_obj.get('idiom_gurmukhi', f"Idiom {idiom_id}")[:255],
                idiom_id=idiom_id,
                idiom_gurmukhi=idiom_obj.get('idiom_gurmukhi', ''),
                idiom_basic_defintion_gurmukhi=idiom_obj.get('idiom_basic_defintion_gurmukhi', ''),
                idiom_shahmukhi=idiom_obj.get('idiom_shahmukhi', ''),
                transliteration_roman_simple=idiom_obj.get('transliteration_roman_simple', ''),
                transliteration_roman=idiom_obj.get('transliteration_roman', ''),
                definition_gurmukhi=idiom_obj.get('definition_gurmukhi', ''),
                definition_shahmukhi=idiom_obj.get('definition_shahmukhi', ''),
                definition_english=idiom_obj.get('definition_english', ''),
                western_phrase=idiom_obj.get('western_phrase', []),
            )

            parent_page.add_child(instance=new_idiom_page)
            new_idiom_page.save_revision().publish()
            created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Import complete! Created: {created_count} new idioms. Skipped: {skipped_count} (already existed)."
        ))