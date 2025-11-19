#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Performance Benchmark Script for Punjabi Sahit
Checks database performance, query counts, and page load times
"""
import os
import sys
import django
import time
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'punjabisahit.settings.dev')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.db import connection, reset_queries
from django.test.utils import override_settings
from django.core.cache import cache
from home.models import *

def print_header(text):
    """Print a formatted header"""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def print_metric(label, value, unit="", good_threshold=None, bad_threshold=None):
    """Print a metric with color coding based on thresholds"""
    status = ""
    if good_threshold is not None and bad_threshold is not None:
        if isinstance(value, (int, float)):
            if value <= good_threshold:
                status = " ✓ GOOD"
            elif value <= bad_threshold:
                status = " ⚠ OK"
            else:
                status = " ✗ NEEDS IMPROVEMENT"

    print(f"  {label:.<50} {value:>10} {unit:>8} {status}")

@override_settings(DEBUG=True)
def benchmark_database():
    """Check database size and table counts"""
    print_header("DATABASE OVERVIEW")

    # Get database size (PostgreSQL specific)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT pg_size_pretty(pg_database_size(current_database())) as size;
        """)
        db_size = cursor.fetchone()[0]

    print_metric("Database Size", db_size, "")

    # Count records in key tables
    print("\n  Content Counts:")
    print_metric("  - Dictionary Entries", DictionaryEntryPage.objects.count(), "entries")
    print_metric("  - Phrases", PhrasePage.objects.count(), "phrases")
    print_metric("  - Idioms", IdiomPage.objects.count(), "idioms")
    print_metric("  - Blog Posts", BlogPostPage.objects.count(), "posts")
    print_metric("  - Books", BookPage.objects.count(), "books")
    print_metric("  - Authors", Author.objects.count(), "authors")
    print_metric("  - Author Detail Pages", AuthorDetailPage.objects.count(), "pages")
    print_metric("  - Total Pages", Page.objects.count(), "pages")

@override_settings(DEBUG=True)
def benchmark_page_queries(page_name, page_func, good_queries=5, bad_queries=20):
    """Benchmark a page's database queries"""
    reset_queries()

    start_time = time.time()
    result = page_func()
    end_time = time.time()

    query_count = len(connection.queries)
    load_time = (end_time - start_time) * 1000  # Convert to ms

    print(f"\n  {page_name}:")
    print_metric("    Load Time", f"{load_time:.2f}", "ms", good_threshold=100, bad_threshold=500)
    print_metric("    Database Queries", query_count, "queries", good_threshold=good_queries, bad_threshold=bad_queries)

    # Check for slow queries (>100ms)
    slow_queries = [q for q in connection.queries if float(q['time']) > 0.1]
    if slow_queries:
        print_metric("    Slow Queries (>100ms)", len(slow_queries), "queries")

    return query_count, load_time

@override_settings(DEBUG=True)
def benchmark_all_pages():
    """Benchmark all major pages"""
    print_header("PAGE PERFORMANCE BENCHMARKS")

    results = []

    # Dictionary Index
    def dict_index():
        return list(DictionaryEntryPage.objects.live().public()[:20])
    results.append(benchmark_page_queries("Dictionary Index (20 entries)", dict_index, 3, 10))

    # Phrases Index
    def phrases_index():
        return list(PhrasePage.objects.live().public()[:20])
    results.append(benchmark_page_queries("Phrases Index (20 entries)", phrases_index, 3, 10))

    # Blog Index
    def blog_index():
        posts = list(BlogPostPage.objects.live().public()[:12])
        # Simulate template access
        for post in posts:
            _ = post.specific.intro
            _ = post.specific.tags.all()
        return posts
    results.append(benchmark_page_queries("Blog Index (12 posts)", blog_index, 5, 15))

    # Authors Index
    def authors_index():
        authors = list(Author.objects.prefetch_related('detail_pages').all()[:24])
        # Simulate template access
        for author in authors:
            _ = author.detail_pages.first()
        return authors
    results.append(benchmark_page_queries("Authors Index (24 authors)", authors_index, 2, 5))

    # Books Index
    def books_index():
        books = list(BookPage.objects.live().public()[:20])
        # Simulate template access
        for book in books:
            _ = book.specific.author
        return books
    results.append(benchmark_page_queries("Books Index (20 books)", books_index, 10, 25))

    return results

@override_settings(DEBUG=True)
def check_n_plus_one():
    """Check for N+1 query problems"""
    print_header("N+1 QUERY DETECTION")

    # Test Authors Index (known potential N+1)
    reset_queries()
    authors = Author.objects.prefetch_related('detail_pages').all()[:10]
    for author in authors:
        _ = author.detail_pages.first()  # This could cause N+1

    query_count = len(connection.queries)
    expected_queries = 2  # 1 for authors, 1 for prefetched detail_pages

    print("  Authors Index Page:")
    if query_count > 11:  # 1 + 10 (one per author)
        print_metric("    Status", "N+1 DETECTED", "")
        print_metric("    Queries for 10 authors", query_count, "queries", good_threshold=2, bad_threshold=5)
        print("    💡 Suggestion: Use prefetch_related('detail_pages')")
    else:
        print_metric("    Status", "OPTIMIZED", "")
        print_metric("    Queries for 10 authors", query_count, "queries", good_threshold=2, bad_threshold=5)

def check_database_indexes():
    """Check for missing database indexes"""
    print_header("DATABASE INDEXES")

    with connection.cursor() as cursor:
        # Check indexes on key tables
        cursor.execute("""
            SELECT
                tablename,
                indexname,
                indexdef
            FROM pg_indexes
            WHERE schemaname = 'public'
            AND tablename IN ('home_dictionaryentrypage', 'home_author', 'home_blogpostpage', 'home_bookpage')
            ORDER BY tablename, indexname;
        """)

        indexes = cursor.fetchall()

        table_index_count = {}
        for table, index, definition in indexes:
            table_index_count[table] = table_index_count.get(table, 0) + 1

        print("  Index Counts by Table:")
        for table, count in sorted(table_index_count.items()):
            print_metric(f"    {table}", count, "indexes")

        print(f"\n  Total Indexes: {len(indexes)}")

def check_cache_performance():
    """Check cache configuration"""
    print_header("CACHE CONFIGURATION")

    # Test cache
    cache_key = 'performance_test'
    cache.set(cache_key, 'test_value', 60)
    cached_value = cache.get(cache_key)

    if cached_value:
        print_metric("Cache Status", "WORKING", "")
    else:
        print_metric("Cache Status", "NOT WORKING", "")

    # Check cache backend from settings
    from django.conf import settings
    cache_backend = settings.CACHES['default']['BACKEND']
    print_metric("Cache Backend", cache_backend.split('.')[-1], "")

#def analyze_query_complexity():
#    """Analyze the complexity of queries"""
#    print_header("QUERY COMPLEXITY ANALYSIS")

#    reset_queries()

#    # Get a dictionary entry with all relationships
#    entry = DictionaryEntryPage.objects.first()
#    if entry:
#        _ = entry.specific.synonyms_gurmukhi
#        _ = entry.specific.antonyms_gurmukhi
#        _ = entry.specific.headword_gurmukhi
#        _ = entry.specific.definition_gurmukhi

#    print(f"  Dictionary Entry Detail:")
#    print_metric("    Queries", len(connection.queries), "queries", good_threshold=3, bad_threshold=8)

def generate_summary(page_results):
    """Generate overall performance summary"""
    print_header("PERFORMANCE SUMMARY")

    total_queries = sum(r[0] for r in page_results)
    avg_queries = total_queries / len(page_results)
    avg_load_time = sum(r[1] for r in page_results) / len(page_results)

    print("  Overall Metrics:")
    print_metric("Average Queries per Page", f"{avg_queries:.1f}", "queries", good_threshold=5, bad_threshold=15)
    print_metric("Average Load Time", f"{avg_load_time:.2f}", "ms", good_threshold=100, bad_threshold=300)

    print("\n  Performance Rating:")
    if avg_queries <= 5 and avg_load_time <= 100:
        rating = "EXCELLENT ⭐⭐⭐⭐⭐"
    elif avg_queries <= 10 and avg_load_time <= 200:
        rating = "GOOD ⭐⭐⭐⭐"
    elif avg_queries <= 20 and avg_load_time <= 500:
        rating = "FAIR ⭐⭐⭐"
    else:
        rating = "NEEDS IMPROVEMENT ⭐⭐"

    print(f"  Overall: {rating}")

    print("\n  Recommendations:")
    if avg_queries > 10:
        print("  • Consider adding select_related/prefetch_related for foreign keys")
    if avg_load_time > 200:
        print("  • Consider implementing page caching")
    if avg_queries > 20:
        print("  • Review and optimize database queries")
        print("  • Check for N+1 query problems")

def main():
    """Run all benchmarks"""
    print(f"\n{'#'*70}")
    print(f"  PUNJABI SAHIT - PERFORMANCE BENCHMARK")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'#'*70}")

    # Run all benchmarks
    benchmark_database()
    page_results = benchmark_all_pages()
    check_n_plus_one()
    check_database_indexes()
    check_cache_performance()
    #     analyze_query_complexity()
    generate_summary(page_results)

    print(f"\n{'#'*70}")
    print(f"  BENCHMARK COMPLETE")
    print(f"{'#'*70}\n")

if __name__ == '__main__':
    main()
