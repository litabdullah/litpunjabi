import json
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

# Make sure your models are correctly imported from the 'home' app
try:
    from home.models import DictionaryIndexPage, DictionaryEntryPage
except ImportError:
    raise ImportError(
        "Could not import models from 'home.models'. "
        "Ensure your 'home' app and models are correctly defined."
    )

class Command(BaseCommand):
    """
    Imports dictionary words from a specified JSON file into Wagtail.
    
    Usage: python manage.py import_words <path_to_words.json>
    """
    help = 'Imports dictionary words from a JSON file into Wagtail.'

    def add_arguments(self, parser):
        parser.add_argument('json_file_path', type=str, help='The full path to the words.json file.')

    def handle(self, *args, **options):
        json_file_path = options['json_file_path']
        self.stdout.write(self.style.NOTICE(f"Attempting to import words from: {json_file_path}"))

        # 1. Find the parent page for dictionary entries
        try:
            parent_page = DictionaryIndexPage.objects.live().first()
            if not parent_page:
                raise CommandError(
                    "CRITICAL: A 'Dictionary Index Page' must be created and published in the Wagtail admin before running this command."
                )
            self.stdout.write(self.style.SUCCESS(f"Found parent page: '{parent_page.title}'"))
        except Exception as e:
            raise CommandError(f"An error occurred trying to find the DictionaryIndexPage: {e}")

        # 2. Load the JSON data
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                words_data = json.load(f)
            self.stdout.write(self.style.SUCCESS(f"Successfully loaded {len(words_data)} words from JSON file."))
        except FileNotFoundError:
            raise CommandError(f"Error: The file at path '{json_file_path}' was not found.")
        except json.JSONDecodeError:
            raise CommandError("Error: The JSON file is malformed. Could not decode.")
        except Exception as e:
            raise CommandError(f"An unexpected error occurred while reading the file: {e}")

        # 3. Process and import the words
        created_count = 0
        skipped_count = 0
        
        try:
            with transaction.atomic(): # Use a transaction for speed and safety
                for i, word_obj in enumerate(words_data):
                    headword = word_obj.get('headword_gurmukhi')
                    if not headword:
                        self.stdout.write(self.style.WARNING(f"Skipping entry {i+1} due to missing 'headword_gurmukhi'."))
                        continue

                    # Prevent duplicates
                    if DictionaryEntryPage.objects.filter(headword_gurmukhi=headword, path__startswith=parent_page.path).exists():
                        skipped_count += 1
                        continue
                    
                    # Create the new page object
                    new_word_page = DictionaryEntryPage(
                        title=headword,
                        lemma_gurmukhi=word_obj.get('lemma_gurmukhi', ''),
                        headword_gurmukhi=headword,
                        headword_shahmukhi=word_obj.get('headword_shahmukhi', ''),
                        headword_roman_simple=word_obj.get('headword_roman_simple', ''),
                        headword_roman_diacritics=word_obj.get('headword_roman_diacritics', ''),
                        headword_roman_ipa=word_obj.get('headword_roman_ipa', ''),
                        parts_of_speech=word_obj.get('parts_of_speech', ''),
                        enriched_definition_gurmukhi=word_obj.get('enriched_definition_gurmukhi', ''),
                        enriched_definition_english=word_obj.get('enriched_definition_english', ''),
                        simple_definition_shahmukhi=word_obj.get('simple_definition_shahmukhi', ''),
                        simple_definition_hindi=word_obj.get('simple_definition_hindi', ''),
                        simple_definition_urdu=word_obj.get('simple_definition_urdu', ''),
                        example_sentences_gurmukhi=word_obj.get('example_sentences_gurmukhi', ''),
                        synonyms_gurmukhi=word_obj.get('synonyms_gurmukhi', ''),
                        antonyms_gurmukhi=word_obj.get('antonyms_gurmukhi', ''),
                        etymology=word_obj.get('etymology', ''),
                        loaned_from=word_obj.get('loaned_from', ''),
                    )

                    parent_page.add_child(instance=new_word_page)
                    new_word_page.save_revision().publish()
                    created_count += 1
        
        except Exception as e:
            raise CommandError(f"A critical error occurred during the import transaction. No data was saved. Error: {e}")

        self.stdout.write(self.style.SUCCESS(
            f"\nImport complete! Created: {created_count} new words. Skipped: {skipped_count} (already existed)."
        ))