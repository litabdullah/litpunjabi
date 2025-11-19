import json
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from home.models import PhrasesIndexPage, PhrasePage

class Command(BaseCommand):
    help = 'Imports phrases from a JSON file into Wagtail.'

    def add_arguments(self, parser):
        parser.add_argument('json_file_path', type=str, help='The path to the phrases.json file.')

    @transaction.atomic
    def handle(self, *args, **options):
        json_file_path = options['json_file_path']
        self.stdout.write(self.style.NOTICE(f"Starting phrase import from {json_file_path}"))

        try:
            parent_page = PhrasesIndexPage.objects.live().first()
            if not parent_page:
                raise CommandError("CRITICAL: A 'Phrases Index Page' must be created and published in the Wagtail admin first.")
            self.stdout.write(self.style.SUCCESS(f"Found parent page: '{parent_page.title}'"))
        except Exception as e:
            raise CommandError(f"Error finding PhrasesIndexPage: {e}")

        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                phrases_data = json.load(f)
            self.stdout.write(self.style.SUCCESS(f"Loaded {len(phrases_data)} phrases from JSON."))
        except FileNotFoundError:
            raise CommandError(f"File not found at {json_file_path}")
        except json.JSONDecodeError:
            raise CommandError("Invalid JSON format.")

        created_count = 0
        skipped_count = 0
        
        for phrase_obj in phrases_data:
            gurmukhi_phrase = phrase_obj.get('phrase_gurmukhi')
            if not gurmukhi_phrase:
                self.stdout.write(self.style.WARNING("Skipping entry due to missing 'phrase_gurmukhi'."))
                continue

            if PhrasePage.objects.filter(phrase_gurmukhi=gurmukhi_phrase).exists():
                skipped_count += 1
                continue

            new_phrase_page = PhrasePage(
                title=gurmukhi_phrase[:255],
                # IDs
                phrase_id=phrase_obj.get('phrase_id'),

                # Phrase in different scripts
                phrase_gurmukhi=gurmukhi_phrase,
                phrase_shahmukhi=phrase_obj.get('phrase_shahmukhi', ''),

                # Romanization
                roman_simple=phrase_obj.get('phrase_roman', ''),
                roman_diacritics=phrase_obj.get('phrase_roman_diacritics', ''),

                # Grammar
                grammar=phrase_obj.get('grammar', ''),

                # Definitions - Simple
                meaning_english=phrase_obj.get('definition_english', ''),
                definition_gurmukhi=phrase_obj.get('definition_gurmukhi', ''),

                # Definitions - Enriched/Detailed
                enriched_definition_gurmukhi=phrase_obj.get('g_enriched_definition_gurmukhi', ''),
                enriched_definition_english=phrase_obj.get('g_enriched_definition_english', ''),
                enriched_definition_shahmukhi=phrase_obj.get('g_enriched_definition_shahmukhi', ''),

                # Explanation (legacy field - kept for backward compatibility)
                explanation=phrase_obj.get('g_enriched_definition_gurmukhi', ''),

                # Examples
                example_sentences_gurmukhi=phrase_obj.get('g_example_sentence_gurmukhi', ''),
                example_usage=phrase_obj.get('g_example_sentence_gurmukhi', ''),

                # Synonyms
                synonyms_gurmukhi=phrase_obj.get('synonyms_gurmukhi', ''),
                synonyms=phrase_obj.get('synonyms_gurmukhi', ''),

                # Source
                source=phrase_obj.get('source', ''),
                source_reference=phrase_obj.get('source', ''),

                # Note: sound field requires Document model handling, will be added in separate step
            )

            parent_page.add_child(instance=new_phrase_page)
            new_phrase_page.save_revision().publish()
            created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Import complete! Created: {created_count} new phrases. Skipped: {skipped_count} (already existed)."
        ))