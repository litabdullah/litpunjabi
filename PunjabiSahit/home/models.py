# home/models.py

from django.db import models
from django.db.models import Avg, F
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

from .utils import gurmukhi_sort_key, sort_gurmukhi_items

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

import wagtail.blocks as blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock


# ===================================================================
# Abstract Base Page for Shared Fields
# ===================================================================

class BaseContentPage(Page):
    """
    An abstract base model that all content-specific pages will inherit from.
    It includes a view counter for tracking trending content.
    """
    view_count = models.PositiveIntegerField(
        default=0,
        editable=False,
        help_text="This is automatically updated when a page is viewed."
    )

    class Meta:
        abstract = True # This tells Django not to create a database table for this model


# ===================================================================
# Reusable StreamField Blocks & Snippets (Unchanged)
# ===================================================================
class RichTextBlock(blocks.StructBlock):
    content = blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr'])
    class Meta: template = "blocks/rich_text_block.html"; icon = "pilcrow"; label = "Rich Text"
class CodeBlock(blocks.StructBlock):
    language = blocks.ChoiceBlock(choices=[('python', 'Python'), ('javascript', 'JavaScript'), ('html', 'HTML'), ('css', 'CSS'), ('bash', 'Bash/Shell')], blank=True, required=False, label="Language")
    code = blocks.TextBlock(label="Code")
    class Meta: icon = "code"; label = "Code Snippet"
class QuoteBlock(blocks.StructBlock):
    quote = blocks.TextBlock(rows=3, required=True); attribution = blocks.CharBlock(required=False, max_length=100)
    class Meta: icon = "openquote"; label = "Quote"

@register_snippet
class Author(models.Model):
    """
    Author model for writers, poets, scholars, etc.
    Registered as a snippet so it can be referenced across different content types.
    """
    # Legacy Core Fields (for backward compatibility)
    author_id = models.CharField(max_length=100, unique=True, help_text="Original ID from JSON", default='temp_id')
    name = models.CharField(max_length=255, help_text="Legacy name field - use name_english for new entries")
    slug = models.SlugField(max_length=255, unique=True, default='temp-slug', help_text="URL-friendly version of name")

    # Names in multiple scripts
    name_gurmukhi = models.CharField(max_length=255, blank=True, help_text="Author name in Gurmukhi")
    name_english = models.CharField(max_length=255, blank=True, help_text="Author name in English")
    name_hindi = models.CharField(max_length=255, blank=True, help_text="Author name in Hindi")
    name_shahmukhi = models.CharField(max_length=255, blank=True, help_text="Author name in Shahmukhi")

    # Images
    profile_image = models.URLField(max_length=500, blank=True, help_text="URL to profile image (legacy)")
    cover_image = models.URLField(max_length=500, blank=True, help_text="URL to cover image (legacy)")
    author_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text="Local uploaded image (legacy)")
    profile_photo = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text="Profile photo (use this for new entries)")

    # Life dates
    birth_date = models.DateField(null=True, blank=True, help_text="Date of birth")
    death_date = models.DateField(null=True, blank=True, help_text="Date of death (leave blank if living)")
    birthplace = models.CharField(max_length=255, blank=True, help_text="Place of birth")

    # Biography & Location
    bio = models.TextField(blank=True, help_text="Legacy bio field - use biography_english for new entries")
    location = models.CharField(max_length=255, blank=True, help_text="Current location")

    # Biography in multiple languages
    biography_gurmukhi = RichTextField(blank=True, help_text="Biography in Gurmukhi")
    biography_english = RichTextField(blank=True, help_text="Biography in English")
    biography_hindi = RichTextField(blank=True, help_text="Biography in Hindi")

    # Literary information
    literary_style = models.CharField(max_length=500, blank=True, help_text="Writing style or genres (comma-separated)")
    awards = RichTextField(blank=True, help_text="Awards and achievements")

    # Social Media Links
    website = models.URLField(max_length=500, blank=True, help_text="Personal website")
    wikipedia_link = models.URLField(blank=True, help_text="Wikipedia page")
    facebook = models.CharField(max_length=255, blank=True)
    twitter = models.CharField(max_length=255, blank=True)
    threads = models.CharField(max_length=255, blank=True)
    bluesky = models.CharField(max_length=255, blank=True)
    mastodon = models.CharField(max_length=255, blank=True)
    tiktok = models.CharField(max_length=255, blank=True)
    youtube = models.CharField(max_length=255, blank=True)
    instagram = models.CharField(max_length=255, blank=True)
    linkedin = models.CharField(max_length=255, blank=True)

    # Metadata
    is_featured = models.BooleanField(default=False, help_text="Feature this author on homepage")
    view_count = models.PositiveIntegerField(default=0, editable=False)

    # SEO Fields
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)

    # Original URL
    original_url = models.URLField(max_length=500, blank=True, help_text="Original URL from punjabisahit.com")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('author_id'),
            FieldPanel('name'),
            FieldPanel('slug'),
        ], heading="Legacy Basic Info (for backward compatibility)"),
        MultiFieldPanel([
            FieldPanel('name_gurmukhi'),
            FieldPanel('name_english'),
            FieldPanel('name_hindi'),
            FieldPanel('name_shahmukhi'),
        ], heading="Names (Multiple Scripts)"),
        MultiFieldPanel([
            FieldPanel('profile_photo'),
            FieldPanel('profile_image'),
            FieldPanel('cover_image'),
            FieldPanel('author_image'),
        ], heading="Images"),
        MultiFieldPanel([
            FieldPanel('birth_date'),
            FieldPanel('death_date'),
            FieldPanel('birthplace'),
            FieldPanel('location'),
        ], heading="Life Information"),
        MultiFieldPanel([
            FieldPanel('bio'),
            FieldPanel('biography_gurmukhi'),
            FieldPanel('biography_english'),
            FieldPanel('biography_hindi'),
        ], heading="Biography"),
        MultiFieldPanel([
            FieldPanel('literary_style'),
            FieldPanel('awards'),
        ], heading="Literary Information"),
        MultiFieldPanel([
            FieldPanel('website'),
            FieldPanel('wikipedia_link'),
            FieldPanel('facebook'),
            FieldPanel('twitter'),
            FieldPanel('instagram'),
            FieldPanel('threads'),
            FieldPanel('bluesky'),
            FieldPanel('mastodon'),
            FieldPanel('tiktok'),
            FieldPanel('youtube'),
            FieldPanel('linkedin'),
        ], heading="External Links & Social Media"),
        MultiFieldPanel([
            FieldPanel('meta_title'),
            FieldPanel('meta_description'),
            FieldPanel('original_url'),
        ], heading="SEO & Metadata"),
        FieldPanel('is_featured'),
    ]

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ['name']

    def __str__(self):
        return self.name_english or self.name or self.name_gurmukhi or "Unnamed Author"

    def get_books(self):
        """Get all books by this author"""
        from home.models import BookPage
        return BookPage.objects.live().filter(author=self).order_by('-publication_year')

    def get_blog_posts(self):
        """Get all blog posts by this author"""
        from home.models import BlogPostPage
        return BlogPostPage.objects.live().filter(author=self).order_by('-first_published_at')

    def get_events(self):
        """Get all events featuring this author"""
        from home.models import EventPage
        return EventPage.objects.live().filter(speakers=self).order_by('-start_datetime')

# ===================================================================
# App Index Pages (Unchanged)
# ===================================================================
class DictionaryIndexPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [FieldPanel('intro')]
    subpage_types = ['home.DictionaryEntryPage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Start with all entries
        all_entries = DictionaryEntryPage.objects.live().public().child_of(self)

        # === FILTERS ===
        # Letter filter
        letter = request.GET.get('letter')
        if letter:
            all_entries = all_entries.filter(headword_gurmukhi__startswith=letter)

        # Search query
        search_query = request.GET.get('q')
        if search_query:
            all_entries = all_entries.search(search_query)

        # Part of speech filter
        pos = request.GET.get('pos')
        if pos:
            all_entries = all_entries.filter(parts_of_speech__icontains=pos)

        # Origin filter
        origin = request.GET.get('origin')
        if origin:
            all_entries = all_entries.filter(origin=origin)

        # Has content filters
        if request.GET.get('has_synonyms') == 'true':
            all_entries = all_entries.exclude(synonyms_gurmukhi='')
        if request.GET.get('has_antonyms') == 'true':
            all_entries = all_entries.exclude(antonyms_gurmukhi='')
        if request.GET.get('has_examples') == 'true':
            all_entries = all_entries.exclude(example_sentences_gurmukhi='')
        if request.GET.get('has_audio') == 'true':
            all_entries = all_entries.exclude(sound__isnull=True)

        # === SORTING ===
        sort_by = request.GET.get('sort', 'alpha_asc')
        if sort_by == 'alpha_asc':
            # Use phonetic Gurmukhi sorting
            all_entries_list = list(all_entries)
            all_entries = sort_gurmukhi_items(all_entries_list, key_func=lambda x: x.headword_gurmukhi)
        elif sort_by == 'alpha_desc':
            # Use phonetic Gurmukhi sorting (reversed)
            all_entries_list = list(all_entries)
            sorted_entries = sort_gurmukhi_items(all_entries_list, key_func=lambda x: x.headword_gurmukhi)
            all_entries = list(reversed(sorted_entries))
        elif sort_by == 'popular':
            all_entries = all_entries.order_by('-view_count')
        elif sort_by == 'recent':
            all_entries = all_entries.order_by('-first_published_at')

        # === PAGINATION ===
        paginator = Paginator(all_entries, 20)
        page = request.GET.get('page')
        try:
            dictionary_entries = paginator.page(page)
        except PageNotAnInteger:
            dictionary_entries = paginator.page(1)
        except EmptyPage:
            dictionary_entries = paginator.page(paginator.num_pages)

        context['dictionary_entries'] = dictionary_entries
        context['current_letter'] = letter
        context['current_sort'] = sort_by
        context['search_query'] = search_query

        return context
class IdiomsIndexPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [FieldPanel('intro')]
    subpage_types = ['home.IdiomPage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Start with all idioms
        all_idioms = IdiomPage.objects.live().public().child_of(self)

        # === FILTERS ===
        # Search query
        search_query = request.GET.get('q')
        if search_query:
            all_idioms = all_idioms.search(search_query)

        # === SORTING ===
        sort_by = request.GET.get('sort', 'alpha_asc')
        if sort_by == 'alpha_asc':
            all_idioms = all_idioms.order_by('idiom_gurmukhi')
        elif sort_by == 'alpha_desc':
            all_idioms = all_idioms.order_by('-idiom_gurmukhi')
        elif sort_by == 'popular':
            all_idioms = all_idioms.order_by('-view_count')
        elif sort_by == 'recent':
            all_idioms = all_idioms.order_by('-first_published_at')
        else:
            all_idioms = all_idioms.order_by('title')

        # === PAGINATION ===
        paginator = Paginator(all_idioms, 20)
        page = request.GET.get('page')
        try:
            idioms = paginator.page(page)
        except PageNotAnInteger:
            idioms = paginator.page(1)
        except EmptyPage:
            idioms = paginator.page(paginator.num_pages)

        context['idioms'] = idioms
        context['current_sort'] = sort_by
        context['search_query'] = search_query

        return context
class PhrasesIndexPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [FieldPanel('intro')]
    subpage_types = ['home.PhrasePage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Start with all phrases
        all_phrases = PhrasePage.objects.live().public().child_of(self)

        # === FILTERS ===
        # Search query
        search_query = request.GET.get('q')
        if search_query:
            all_phrases = all_phrases.search(search_query)

        # Category filter
        category = request.GET.get('category')
        if category:
            all_phrases = all_phrases.filter(category__icontains=category)

        # === SORTING ===
        sort_by = request.GET.get('sort', 'alpha_asc')
        if sort_by == 'alpha_asc':
            all_phrases = all_phrases.order_by('phrase_gurmukhi')
        elif sort_by == 'alpha_desc':
            all_phrases = all_phrases.order_by('-phrase_gurmukhi')
        elif sort_by == 'popular':
            all_phrases = all_phrases.order_by('-view_count')
        elif sort_by == 'recent':
            all_phrases = all_phrases.order_by('-first_published_at')
        else:
            all_phrases = all_phrases.order_by('title')

        # === PAGINATION ===
        paginator = Paginator(all_phrases, 20)
        page = request.GET.get('page')
        try:
            phrases = paginator.page(page)
        except PageNotAnInteger:
            phrases = paginator.page(1)
        except EmptyPage:
            phrases = paginator.page(paginator.num_pages)

        context['phrases'] = phrases
        context['current_sort'] = sort_by
        context['search_query'] = search_query
        context['current_category'] = category

        return context
class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [FieldPanel('intro')]
    subpage_types = ['home.BlogPostPage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Start with all blog posts
        all_posts = BlogPostPage.objects.live().public()

        # === FILTERS ===
        # Search query
        search_query = request.GET.get('q')
        if search_query:
            all_posts = all_posts.search(search_query)

        # Tag filter
        tag = request.GET.get('tag')
        if tag:
            all_posts = all_posts.filter(tags__name=tag)

        # === SORTING ===
        sort_by = request.GET.get('sort', 'recent')
        if sort_by == 'recent':
            all_posts = all_posts.order_by('-first_published_at')
        elif sort_by == 'popular':
            all_posts = all_posts.order_by('-view_count')
        elif sort_by == 'title':
            all_posts = all_posts.order_by('title')

        # === PAGINATION ===
        paginator = Paginator(all_posts, 12)
        page = request.GET.get('page')
        try:
            blog_posts = paginator.page(page)
        except PageNotAnInteger:
            blog_posts = paginator.page(1)
        except EmptyPage:
            blog_posts = paginator.page(paginator.num_pages)

        # Get all tags for filter dropdown
        from home.models import BlogPostPageTag
        all_tags = BlogPostPageTag.objects.all().values_list('tag__name', flat=True).distinct()

        context['blog_posts'] = blog_posts
        context['current_sort'] = sort_by
        context['search_query'] = search_query
        context['current_tag'] = tag
        context['all_tags'] = all_tags

        return context
class EventsIndexPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [FieldPanel('intro')]
    subpage_types = ['home.EventPage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        now = timezone.now()

        # Start with all events
        all_events = EventPage.objects.live().public().child_of(self)

        # === FILTERS ===
        # Search query
        search_query = request.GET.get('q')
        if search_query:
            all_events = all_events.search(search_query)

        # Time filter (upcoming/past/all)
        time_filter = request.GET.get('time', 'upcoming')
        if time_filter == 'upcoming':
            all_events = all_events.filter(start_datetime__gte=now)
            sort_order = 'start_datetime'  # Soonest first
        elif time_filter == 'past':
            all_events = all_events.filter(start_datetime__lt=now)
            sort_order = '-start_datetime'  # Most recent first
        else:  # all
            sort_order = '-start_datetime'

        # Location filter
        location = request.GET.get('location')
        if location:
            all_events = all_events.filter(location__icontains=location)

        # === SORTING ===
        all_events = all_events.order_by(sort_order)

        # === PAGINATION ===
        paginator = Paginator(all_events, 15)
        page = request.GET.get('page')
        try:
            events = paginator.page(page)
        except PageNotAnInteger:
            events = paginator.page(1)
        except EmptyPage:
            events = paginator.page(paginator.num_pages)

        context['events'] = events
        context['current_time_filter'] = time_filter
        context['search_query'] = search_query
        context['current_location'] = location

        # Pass all events for calendar view (without pagination)
        context['all_events'] = EventPage.objects.live().public().child_of(self).order_by('start_datetime')

        return context

# ===================================================================
# Home App
# ===================================================================
class HomePage(Page):
    featured_item = models.ForeignKey('wagtailcore.Page', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text="Optional: Manually select a page to feature. If empty, a random Phrase of the Day will be chosen.")
    content_panels = Page.content_panels + [FieldPanel('featured_item')]
    subpage_types = ['home.DictionaryIndexPage', 'home.IdiomsIndexPage', 'home.PhrasesIndexPage', 'home.BlogIndexPage', 'home.EventsIndexPage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Featured Page (Phrase of the Day)
        if self.featured_item and self.featured_item.live:
            featured_page = self.featured_item.specific
        else:
            featured_page = PhrasePage.objects.live().public().order_by('?').first()
        context['featured_page'] = featured_page

        # Trending Content
        context['trending_words'] = DictionaryEntryPage.objects.live().public().order_by('-view_count')[:3]
        context['trending_idioms'] = IdiomPage.objects.live().public().order_by('-view_count')[:3]
        context['trending_phrases'] = PhrasePage.objects.live().public().order_by('-view_count')[:3]

        # Stats for Counter Animation
        context['stats'] = {
            'words': DictionaryEntryPage.objects.live().public().count(),
            'idioms': IdiomPage.objects.live().public().count(),
            'phrases': PhrasePage.objects.live().public().count(),
            'blog_posts': BlogPostPage.objects.live().public().count(),
        }

        # Latest Blog Posts
        context['latest_blog_posts'] = BlogPostPage.objects.live().public().order_by('-first_published_at')[:3]

        return context

# ===================================================================
# Dictionary App - NOW INHERITS FROM BaseContentPage
# ===================================================================
class DictionaryEntryPage(BaseContentPage):
    lemma_gurmukhi = models.CharField(max_length=255, help_text="The base form of the word in Gurmukhi."); headword_gurmukhi = models.CharField(max_length=255); headword_shahmukhi = models.CharField(max_length=255); headword_roman_simple = models.CharField(max_length=255); headword_roman_diacritics = models.CharField(max_length=255, blank=True); headword_roman_ipa = models.CharField(max_length=255, blank=True, verbose_name="Roman (IPA)")
    parts_of_speech = models.CharField(max_length=100); sound = models.ForeignKey('wagtaildocs.Document', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    enriched_definition_gurmukhi = RichTextField(); enriched_definition_english = RichTextField(); simple_definition_shahmukhi = models.TextField(); simple_definition_hindi = models.TextField(blank=True); simple_definition_urdu = models.TextField(blank=True)
    example_sentences_gurmukhi = RichTextField(blank=True); synonyms_gurmukhi = models.CharField(max_length=500, blank=True); antonyms_gurmukhi = models.CharField(max_length=500, blank=True)
    etymology = models.CharField(max_length=500, blank=True); loaned_from = models.CharField(max_length=100, blank=True)
    origin = models.CharField(max_length=100, blank=True, choices=[
        ('punjabi', 'Punjabi'),
        ('arabic', 'Arabic'),
        ('persian', 'Persian'),
        ('sanskrit', 'Sanskrit'),
        ('urdu', 'Urdu'),
        ('hindi', 'Hindi'),
        ('english', 'English'),
        ('other', 'Other'),
    ], help_text="Language origin of the word")
    tags = ClusterTaggableManager(through='home.DictionaryEntryTag', blank=True) # view_count is now inherited
    search_fields = Page.search_fields + [index.SearchField('headword_gurmukhi', partial_match=True, boost=5), index.SearchField('headword_shahmukhi', partial_match=True, boost=5), index.SearchField('headword_roman_simple', partial_match=True, boost=4), index.SearchField('enriched_definition_english', boost=2), index.SearchField('enriched_definition_gurmukhi'), index.SearchField('synonyms_gurmukhi')]
    content_panels = Page.content_panels + [MultiFieldPanel([FieldPanel('lemma_gurmukhi'), FieldPanel('headword_gurmukhi'), FieldPanel('headword_shahmukhi')], heading="Headwords"), MultiFieldPanel([FieldPanel('headword_roman_simple'), FieldPanel('headword_roman_diacritics'), FieldPanel('headword_roman_ipa')], heading="Roman Transliteration"), MultiFieldPanel([FieldPanel('parts_of_speech'), FieldPanel('sound'), FieldPanel('tags')], heading="Core Details"), MultiFieldPanel([FieldPanel('enriched_definition_gurmukhi'), FieldPanel('enriched_definition_english'), FieldPanel('simple_definition_shahmukhi'), FieldPanel('simple_definition_hindi'), FieldPanel('simple_definition_urdu')], heading="Definitions"), MultiFieldPanel([FieldPanel('example_sentences_gurmukhi'), FieldPanel('synonyms_gurmukhi'), FieldPanel('antonyms_gurmukhi')], heading="Usage"), MultiFieldPanel([FieldPanel('etymology'), FieldPanel('loaned_from'), FieldPanel('origin')], heading="Origin")]
    parent_page_types = ['home.DictionaryIndexPage']; subpage_types = []

    def get_similar_words(self, max_words=6):
        """
        Returns similar dictionary entries based on shared tags, part of speech, or etymology.
        """
        from django.db.models import Count, Q

        # Get entries that share tags
        entry_tags = self.tags.all()
        similar_words = None

        if entry_tags:
            tag_ids = [tag.id for tag in entry_tags]
            similar_words = (
                DictionaryEntryPage.objects
                .live()
                .public()
                .exclude(pk=self.pk)
                .filter(tags__in=tag_ids)
                .annotate(same_tags=Count('pk'))
                .order_by('-same_tags', '-view_count')
                .distinct()[:max_words]
            )

        # If no tag matches, find by part of speech
        if not similar_words or similar_words.count() < max_words:
            remaining = max_words - (similar_words.count() if similar_words else 0)
            pos_similar = (
                DictionaryEntryPage.objects
                .live()
                .public()
                .exclude(pk=self.pk)
                .filter(parts_of_speech=self.parts_of_speech)
                .order_by('-view_count')[:remaining]
            )

            if similar_words:
                # Combine querysets
                similar_words = list(similar_words) + list(pos_similar)
            else:
                similar_words = pos_similar

        return similar_words[:max_words] if similar_words else []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['similar_words'] = self.get_similar_words()
        return context

class DictionaryEntryTag(TaggedItemBase):
    content_object = ParentalKey('home.DictionaryEntryPage', on_delete=models.CASCADE, related_name='tagged_items')
    # ===================================================================
# Idioms App - NOW INHERITS FROM BaseContentPage
# ===================================================================

class IdiomPage(BaseContentPage):
    idiom_id = models.PositiveIntegerField(unique=True, help_text="The original ID from the JSON file.")
    idiom_gurmukhi = models.CharField(max_length=500)
    idiom_basic_defintion_gurmukhi = models.TextField(blank=True, help_text="Basic definition in Gurmukhi (note: typo from source JSON)")
    idiom_shahmukhi = models.CharField(max_length=500)
    transliteration_roman_simple = models.CharField(max_length=500)
    transliteration_roman = models.CharField(max_length=500, blank=True, verbose_name="Roman with diacritics")
    definition_gurmukhi = models.TextField()
    definition_shahmukhi = models.TextField()
    definition_english = models.TextField()
    western_phrase = models.JSONField(help_text="A list of equivalent or similar Western phrases.")
    # view_count is now inherited
    search_fields = Page.search_fields + [index.SearchField('idiom_gurmukhi', partial_match=True, boost=5), index.SearchField('idiom_shahmukhi', partial_match=True, boost=5), index.SearchField('transliteration_roman_simple', boost=4), index.SearchField('definition_english', boost=2), index.SearchField('idiom_basic_defintion_gurmukhi')]
    content_panels = Page.content_panels + [FieldPanel('idiom_id'), MultiFieldPanel([FieldPanel('idiom_gurmukhi'), FieldPanel('idiom_basic_defintion_gurmukhi'), FieldPanel('idiom_shahmukhi'), FieldPanel('transliteration_roman_simple'), FieldPanel('transliteration_roman')], heading="Idiom Text"), MultiFieldPanel([FieldPanel('definition_gurmukhi'), FieldPanel('definition_shahmukhi'), FieldPanel('definition_english')], heading="Definitions"), FieldPanel('western_phrase')]
    parent_page_types = ['home.IdiomsIndexPage']
    subpage_types = []


# ===================================================================
# Phrases App - NOW INHERITS FROM BaseContentPage
# ===================================================================

class PhrasePage(BaseContentPage):
    # IDs from JSON
    phrase_id = models.PositiveIntegerField(unique=True, null=True, blank=True, help_text="The original ID from the JSON file.")

    # Phrase in different scripts
    phrase_gurmukhi = models.CharField(max_length=500)
    phrase_shahmukhi = models.CharField(max_length=500)

    # Romanization
    roman_simple = models.CharField(max_length=500, verbose_name="Roman (simple)")
    roman_diacritics = models.CharField(max_length=500, blank=True, verbose_name="Roman (with diacritics)")

    # Grammar
    grammar = models.CharField(max_length=100, blank=True, help_text="Type: phrase, idiom, etc.")

    # Definitions - Simple
    meaning_english = models.CharField(max_length=500, verbose_name="Simple English meaning")
    definition_gurmukhi = models.TextField(blank=True, help_text="Simple definition in Gurmukhi")

    # Definitions - Enriched/Detailed
    enriched_definition_gurmukhi = RichTextField(blank=True, help_text="Detailed explanation in Gurmukhi")
    enriched_definition_english = RichTextField(blank=True, help_text="Detailed explanation in English")
    enriched_definition_shahmukhi = models.TextField(blank=True, help_text="Detailed explanation in Shahmukhi")

    # Explanation (keeping for backward compatibility)
    explanation = RichTextField(blank=True, help_text="General explanation (legacy field)")

    # Examples
    example_sentences_gurmukhi = RichTextField(blank=True, help_text="Example sentences in Gurmukhi")
    example_usage = RichTextField(blank=True, help_text="Example usage (legacy field)")

    # Synonyms & Antonyms
    synonyms_gurmukhi = models.CharField(max_length=500, blank=True, verbose_name="Synonyms (Gurmukhi)")
    synonyms = models.CharField(max_length=500, blank=True, help_text="Synonyms (legacy field)")
    antonyms = models.CharField(max_length=500, blank=True)

    # Source & References
    source = models.CharField(max_length=255, blank=True, help_text="Source attribution")
    source_reference = models.CharField(max_length=255, blank=True, help_text="Source reference (legacy field)")

    # Audio
    sound = models.ForeignKey('wagtaildocs.Document', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text="Audio pronunciation file")

    # Related entries
    related_entries = ParentalManyToManyField('home.DictionaryEntryPage', blank=True)

    # view_count is now inherited
    search_fields = Page.search_fields + [
        index.SearchField('phrase_gurmukhi', partial_match=True, boost=5),
        index.SearchField('phrase_shahmukhi', partial_match=True, boost=5),
        index.SearchField('roman_simple', boost=4),
        index.SearchField('meaning_english', boost=3),
        index.SearchField('enriched_definition_english', boost=2),
        index.SearchField('definition_gurmukhi'),
        index.SearchField('synonyms_gurmukhi')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('phrase_id'),
        MultiFieldPanel([
            FieldPanel('phrase_gurmukhi'),
            FieldPanel('phrase_shahmukhi'),
            FieldPanel('roman_simple'),
            FieldPanel('roman_diacritics'),
            FieldPanel('grammar')
        ], heading="Phrase Text"),
        MultiFieldPanel([
            FieldPanel('meaning_english'),
            FieldPanel('definition_gurmukhi'),
            FieldPanel('enriched_definition_gurmukhi'),
            FieldPanel('enriched_definition_english'),
            FieldPanel('enriched_definition_shahmukhi'),
            FieldPanel('explanation')
        ], heading="Definitions & Explanations"),
        MultiFieldPanel([
            FieldPanel('example_sentences_gurmukhi'),
            FieldPanel('example_usage'),
            FieldPanel('synonyms_gurmukhi'),
            FieldPanel('synonyms'),
            FieldPanel('antonyms')
        ], heading="Usage & Related Words"),
        MultiFieldPanel([
            FieldPanel('source'),
            FieldPanel('source_reference'),
            FieldPanel('sound')
        ], heading="Source & Media"),
        FieldPanel('related_entries')
    ]
    parent_page_types = ['home.PhrasesIndexPage']
    subpage_types = []


# ===================================================================
# Blog App - NOW INHERITS FROM BaseContentPage
# ===================================================================

class BlogPostPageTag(TaggedItemBase):
    content_object = ParentalKey('home.BlogPostPage', on_delete=models.CASCADE, related_name='tagged_items')

class BlogPostPage(BaseContentPage):
    # IDs from JSON
    post_id = models.CharField(max_length=100, unique=True, blank=True, null=True, help_text="Original ID from JSON")
    uuid = models.UUIDField(blank=True, null=True, help_text="UUID from original post")
    comment_id = models.CharField(max_length=100, blank=True)

    # Content
    intro = models.CharField(max_length=500, blank=True, help_text="Custom excerpt / intro")
    body = StreamField([
        ('paragraph', RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('video', EmbedBlock()),
        ('code', CodeBlock()),
        ('quote', QuoteBlock()),
    ], use_json_field=True, blank=True)
    html_content = models.TextField(blank=True, help_text="Raw HTML content from JSON")
    excerpt = models.TextField(blank=True, help_text="Auto-generated excerpt")
    reading_time = models.IntegerField(default=0, help_text="Reading time in minutes")

    # Images
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    feature_image_url = models.URLField(max_length=500, blank=True, help_text="URL to feature image")
    feature_image_alt = models.CharField(max_length=255, blank=True)
    feature_image_caption = models.TextField(blank=True)

    # Authors & Tags
    author = models.ForeignKey('home.Author', null=True, blank=True, on_delete=models.SET_NULL, related_name='blog_posts', help_text="Primary author of this post")
    tags = ClusterTaggableManager(through=BlogPostPageTag, blank=True)

    # Publishing metadata
    featured = models.BooleanField(default=False)
    visibility = models.CharField(max_length=20, default='public', choices=[
        ('public', 'Public'),
        ('private', 'Private'),
        ('members', 'Members Only'),
    ])
    published_at = models.DateTimeField(blank=True, null=True, help_text="Original publish date")
    updated_at = models.DateTimeField(blank=True, null=True, help_text="Last updated date")

    # Options
    access = models.BooleanField(default=True)
    comments = models.BooleanField(default=True)

    # Code injection
    codeinjection_head = models.TextField(blank=True, help_text="Code to inject in <head>")
    codeinjection_foot = models.TextField(blank=True, help_text="Code to inject before </body>")

    # SEO - Meta tags
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)

    # SEO - OpenGraph
    og_image = models.URLField(max_length=500, blank=True)
    og_title = models.CharField(max_length=255, blank=True)
    og_description = models.TextField(blank=True)

    # SEO - Twitter
    twitter_image = models.URLField(max_length=500, blank=True)
    twitter_title = models.CharField(max_length=255, blank=True)
    twitter_description = models.TextField(blank=True)

    # Other metadata
    custom_template = models.CharField(max_length=255, blank=True)
    canonical_url = models.URLField(max_length=500, blank=True)
    original_url = models.URLField(max_length=500, blank=True, help_text="Original URL from punjabisahit.com")
    email_subject = models.CharField(max_length=255, blank=True)
    frontmatter = models.TextField(blank=True)

    # view_count is now inherited
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
        index.SearchField('html_content'),
        index.SearchField('excerpt'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('post_id'),
            FieldPanel('uuid'),
            FieldPanel('comment_id'),
        ], heading="IDs"),
        MultiFieldPanel([
            FieldPanel('intro'),
            FieldPanel('body'),
            FieldPanel('html_content'),
            FieldPanel('excerpt'),
            FieldPanel('reading_time'),
        ], heading="Content"),
        MultiFieldPanel([
            FieldPanel('featured_image'),
            FieldPanel('feature_image_url'),
            FieldPanel('feature_image_alt'),
            FieldPanel('feature_image_caption'),
        ], heading="Featured Image"),
        MultiFieldPanel([
            FieldPanel('author'),
            FieldPanel('tags'),
            FieldPanel('featured'),
            FieldPanel('visibility'),
            FieldPanel('published_at'),
            FieldPanel('updated_at'),
        ], heading="Metadata"),
        MultiFieldPanel([
            FieldPanel('access'),
            FieldPanel('comments'),
            FieldPanel('custom_template'),
            FieldPanel('canonical_url'),
            FieldPanel('original_url'),
        ], heading="Options"),
        MultiFieldPanel([
            FieldPanel('codeinjection_head'),
            FieldPanel('codeinjection_foot'),
        ], heading="Code Injection"),
        MultiFieldPanel([
            FieldPanel('meta_title'),
            FieldPanel('meta_description'),
            FieldPanel('og_image'),
            FieldPanel('og_title'),
            FieldPanel('og_description'),
            FieldPanel('twitter_image'),
            FieldPanel('twitter_title'),
            FieldPanel('twitter_description'),
            FieldPanel('email_subject'),
            FieldPanel('frontmatter'),
        ], heading="SEO & Advanced"),
    ]

    parent_page_types = ['home.BlogIndexPage']
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['next_post'] = self.next_post
        context['prev_post'] = self.prev_post
        context['similar_posts'] = self.get_similar_posts()
        return context

    @property
    def next_post(self):
        return self.get_next_siblings().live().public().first()

    @property
    def prev_post(self):
        return self.get_prev_siblings().live().public().first()

    def get_similar_posts(self, max_posts=3):
        """
        Returns similar blog posts based on shared tags.
        Uses tag matching to find related content.
        """
        # Get all tags for this post
        post_tags = self.tags.all()

        if not post_tags:
            # If no tags, return recent posts excluding this one
            return BlogPostPage.objects.live().public().exclude(pk=self.pk).order_by('-first_published_at')[:max_posts]

        # Find posts that share at least one tag with this post
        # Annotate with the count of matching tags and order by it
        from django.db.models import Count, Q

        tag_ids = [tag.id for tag in post_tags]
        similar_posts = (
            BlogPostPage.objects
            .live()
            .public()
            .exclude(pk=self.pk)  # Exclude current post
            .filter(tags__in=tag_ids)  # Filter by shared tags
            .annotate(same_tags=Count('pk'))  # Count occurrences
            .order_by('-same_tags', '-first_published_at')  # Order by tag matches, then recency
            .distinct()[:max_posts]
        )

        return similar_posts


# ===================================================================
# Events App - NOW INHERITS FROM BaseContentPage
# ===================================================================

class EventPageTag(TaggedItemBase):
    content_object = ParentalKey('home.EventPage', on_delete=models.CASCADE, related_name='tagged_items')

class EventPage(BaseContentPage):
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, help_text="Short description for list views")
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    organizer = models.CharField(max_length=255, blank=True)
    speakers = ParentalManyToManyField('home.Author', blank=True, related_name='speaking_events', help_text="Authors/speakers for this event")
    body = RichTextField()
    external_link = models.URLField(blank=True)
    tags = ClusterTaggableManager(through=EventPageTag, blank=True)
    # view_count is now inherited
    search_fields = Page.search_fields + [
        index.SearchField('location'),
        index.SearchField('body'),
    ]
    
    content_panels = Page.content_panels + [
        FieldPanel('start_datetime'),
        FieldPanel('end_datetime'),
        FieldPanel('location'),
        FieldPanel('description'),
        FieldPanel('price'),
        FieldPanel('organizer'),
        FieldPanel('speakers'),
        FieldPanel('body'),
        FieldPanel('external_link'),
        FieldPanel('tags'),
    ]

    parent_page_types = ['home.EventsIndexPage']
    subpage_types = []


# ===================================================================
# Authors App - Index and Detail Pages
# ===================================================================

class AuthorsIndexPage(Page):
    """Index page for all authors"""
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    subpage_types = ['home.AuthorDetailPage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Get all authors from the snippet
        all_authors = Author.objects.prefetch_related('detail_pages').all()

        # Search filter
        search_query = request.GET.get('q')
        if search_query:
            all_authors = all_authors.filter(
                models.Q(name_gurmukhi__icontains=search_query) |
                models.Q(name_english__icontains=search_query) |
                models.Q(name_hindi__icontains=search_query)
            )

        # Genre/style filter
        style = request.GET.get('style')
        if style:
            all_authors = all_authors.filter(literary_style__icontains=style)

        # Sort
        sort_by = request.GET.get('sort', 'name')
        if sort_by == 'name':
            all_authors = all_authors.order_by('name_gurmukhi')
        elif sort_by == 'birth_year':
            all_authors = all_authors.order_by('birth_date')
        elif sort_by == 'popular':
            all_authors = all_authors.order_by('-view_count')

        # Pagination
        paginator = Paginator(all_authors, 24)
        page = request.GET.get('page')
        try:
            authors = paginator.page(page)
        except PageNotAnInteger:
            authors = paginator.page(1)
        except EmptyPage:
            authors = paginator.page(paginator.num_pages)

        context['authors'] = authors
        context['search_query'] = search_query
        context['current_sort'] = sort_by

        return context


class AuthorDetailPage(Page):
    """Detail page for a single author"""
    author = models.ForeignKey(
        Author,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='detail_pages'
    )

    content_panels = Page.content_panels + [
        FieldPanel('author'),
    ]

    parent_page_types = ['home.AuthorsIndexPage']
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        if self.author:
            # Get author's content
            context['books'] = self.author.get_books()
            context['blog_posts'] = self.author.get_blog_posts()[:10]
            context['events'] = self.author.get_events()[:10]

            # Increment view count
            Author.objects.filter(pk=self.author.pk).update(view_count=F('view_count') + 1)

        return context


# ===================================================================
# Books App
# ===================================================================

class BookPageTag(TaggedItemBase):
    content_object = ParentalKey('home.BookPage', on_delete=models.CASCADE, related_name='tagged_items')


class BooksIndexPage(Page):
    """Index page for all books"""
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    subpage_types = ['home.BookPage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Start with all books
        all_books = BookPage.objects.live().public().child_of(self)

        # Search filter
        search_query = request.GET.get('q')
        if search_query:
            all_books = all_books.search(search_query)

        # Author filter
        author_id = request.GET.get('author')
        if author_id:
            all_books = all_books.filter(author_id=author_id)

        # Category filter
        category = request.GET.get('category')
        if category:
            all_books = all_books.filter(category__icontains=category)

        # Publisher filter
        publisher = request.GET.get('publisher')
        if publisher:
            all_books = all_books.filter(publisher__icontains=publisher)

        # Year filter
        year = request.GET.get('year')
        if year:
            all_books = all_books.filter(publication_year=year)

        # Tag filter
        tag = request.GET.get('tag')
        if tag:
            all_books = all_books.filter(tags__name=tag)

        # Sort
        sort_by = request.GET.get('sort', 'recent')
        if sort_by == 'title':
            all_books = all_books.order_by('title_gurmukhi')
        elif sort_by == 'author':
            all_books = all_books.order_by('author__name_gurmukhi')
        elif sort_by == 'year':
            all_books = all_books.order_by('-publication_year')
        elif sort_by == 'popular':
            all_books = all_books.order_by('-view_count')
        else:  # recent
            all_books = all_books.order_by('-first_published_at')

        # Pagination
        paginator = Paginator(all_books, 24)
        page = request.GET.get('page')
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)

        # Get all authors for filter dropdown
        all_authors = Author.objects.all().order_by('name_gurmukhi')

        context['books'] = books
        context['all_authors'] = all_authors
        context['search_query'] = search_query
        context['current_sort'] = sort_by

        return context


class BookPage(BaseContentPage):
    """Individual book page"""

    # Cover image
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # Titles in multiple scripts
    title_gurmukhi = models.CharField(max_length=500)
    title_english = models.CharField(max_length=500, blank=True)
    title_hindi = models.CharField(max_length=500, blank=True)
    title_shahmukhi = models.CharField(max_length=500, blank=True)

    # Author
    author = models.ForeignKey(
        Author,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='books'
    )

    # Book details
    pages = models.PositiveIntegerField(null=True, blank=True, help_text="Number of pages")
    publisher = models.CharField(max_length=255, blank=True)
    printer = models.CharField(max_length=255, blank=True, help_text="Printing company")
    publication_year = models.PositiveIntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=20, blank=True, help_text="ISBN number")
    edition = models.CharField(max_length=100, blank=True, help_text="Edition (e.g., First Edition, Revised)")

    # Descriptions
    description_gurmukhi = RichTextField(blank=True, help_text="Book description in Gurmukhi")
    description_english = RichTextField(blank=True, help_text="Book description in English")
    description_hindi = RichTextField(blank=True, help_text="Book description in Hindi")

    # Categorization
    category = models.CharField(
        max_length=100,
        blank=True,
        help_text="Category: Literature, History, Religious, Poetry, etc."
    )
    tags = ClusterTaggableManager(through=BookPageTag, blank=True)

    # External links
    purchase_link = models.URLField(blank=True, help_text="Link to purchase the book")
    pdf_link = models.URLField(blank=True, help_text="Link to PDF version if available")

    # view_count is inherited from BaseContentPage

    search_fields = Page.search_fields + [
        index.SearchField('title_gurmukhi', partial_match=True, boost=5),
        index.SearchField('title_english', partial_match=True, boost=5),
        index.SearchField('description_english', boost=2),
        index.SearchField('description_gurmukhi'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('cover_image'),
        MultiFieldPanel([
            FieldPanel('title_gurmukhi'),
            FieldPanel('title_english'),
            FieldPanel('title_hindi'),
            FieldPanel('title_shahmukhi'),
        ], heading="Titles"),
        FieldPanel('author'),
        MultiFieldPanel([
            FieldPanel('pages'),
            FieldPanel('publisher'),
            FieldPanel('printer'),
            FieldPanel('publication_year'),
            FieldPanel('isbn'),
            FieldPanel('edition'),
        ], heading="Book Details"),
        MultiFieldPanel([
            FieldPanel('description_gurmukhi'),
            FieldPanel('description_english'),
            FieldPanel('description_hindi'),
        ], heading="Descriptions"),
        MultiFieldPanel([
            FieldPanel('category'),
            FieldPanel('tags'),
        ], heading="Categorization"),
        MultiFieldPanel([
            FieldPanel('purchase_link'),
            FieldPanel('pdf_link'),
        ], heading="External Links"),
    ]

    parent_page_types = ['home.BooksIndexPage']
    subpage_types = []

    def get_similar_books(self, max_books=6):
        """Get similar books based on author, category, or tags"""
        from django.db.models import Count, Q

        similar_books = None

        # First try: same author
        if self.author:
            similar_books = (
                BookPage.objects
                .live()
                .public()
                .exclude(pk=self.pk)
                .filter(author=self.author)
                .order_by('-view_count')[:max_books]
            )

        # If not enough, try same category
        if not similar_books or similar_books.count() < max_books:
            remaining = max_books - (similar_books.count() if similar_books else 0)
            category_books = (
                BookPage.objects
                .live()
                .public()
                .exclude(pk=self.pk)
                .filter(category=self.category)
                .order_by('-view_count')[:remaining]
            )

            if similar_books:
                similar_books = list(similar_books) + list(category_books)
            else:
                similar_books = category_books

        return similar_books[:max_books] if similar_books else []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['similar_books'] = self.get_similar_books()

        # Get user's reading status if authenticated
        if request.user.is_authenticated:
            try:
                user_status = UserBookStatus.objects.get(user=request.user, book=self)
                context['user_book_status'] = user_status
            except UserBookStatus.DoesNotExist:
                context['user_book_status'] = None

        return context


# ===================================================================
# User Book Status (Reading Progress Tracking)
# ===================================================================

@register_snippet
class UserBookStatus(models.Model):
    """
    Track user's reading status for books.
    Allows users to mark books as: To Read, Reading, Read, Completed, or add to Favorites.
    """
    STATUS_CHOICES = [
        ('to_read', 'To Read'),
        ('reading', 'Currently Reading'),
        ('read', 'Read'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_statuses')
    book = models.ForeignKey(BookPage, on_delete=models.CASCADE, related_name='user_statuses')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='to_read')
    is_favorite = models.BooleanField(default=False, help_text="Mark as favorite")

    # Progress tracking
    current_page = models.PositiveIntegerField(default=0, help_text="Current page number")
    notes = models.TextField(blank=True, help_text="Personal notes about the book")
    rating = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating out of 5 stars"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_reading = models.DateTimeField(null=True, blank=True, help_text="When user started reading")
    finished_reading = models.DateTimeField(null=True, blank=True, help_text="When user finished reading")

    class Meta:
        unique_together = ['user', 'book']
        verbose_name = "User Book Status"
        verbose_name_plural = "User Book Statuses"
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.book.title_english or self.book.title_gurmukhi} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        # Auto-set timestamps based on status
        if self.status == 'reading' and not self.started_reading:
            self.started_reading = timezone.now()
        elif self.status in ['read', 'completed'] and not self.finished_reading:
            self.finished_reading = timezone.now()
        super().save(*args, **kwargs)

    @property
    def progress_percentage(self):
        """Calculate reading progress as percentage"""
        if self.book.pages and self.current_page:
            return min(int((self.current_page / self.book.pages) * 100), 100)
        return 0