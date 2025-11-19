# home/utils.py

"""
Utility functions for Punjabi Sahit application
"""

# Gurmukhi alphabet order for proper sorting
GURMUKHI_ALPHABET_ORDER = {
    # Independent vowels
    'ੳ': 1, 'ਅ': 2, 'ੲ': 3, 'ਸ': 4, 'ਹ': 5,

    # Consonants (Vyanjan)
    'ਕ': 6, 'ਖ': 7, 'ਗ': 8, 'ਘ': 9, 'ਙ': 10,
    'ਚ': 11, 'ਛ': 12, 'ਜ': 13, 'ਝ': 14, 'ਞ': 15,
    'ਟ': 16, 'ਠ': 17, 'ਡ': 18, 'ਢ': 19, 'ਣ': 20,
    'ਤ': 21, 'ਥ': 22, 'ਦ': 23, 'ਧ': 24, 'ਨ': 25,
    'ਪ': 26, 'ਫ': 27, 'ਬ': 28, 'ਭ': 29, 'ਮ': 30,
    'ਯ': 31, 'ਰ': 32, 'ਲ': 33, 'ਵ': 34, 'ੜ': 35,

    # Additional characters
    'ਸ਼': 36, 'ਖ਼': 37, 'ਗ਼': 38, 'ਜ਼': 39, 'ਫ਼': 40,
    'ਲ਼': 41,

    # Vowel signs (dependent vowels - Laga Matra)
    'ਾ': 100, 'ਿ': 101, 'ੀ': 102, 'ੁ': 103, 'ੂ': 104,
    'ੇ': 105, 'ੈ': 106, 'ੋ': 107, 'ੌ': 108,

    # Other diacritics
    '਼': 200,  # Nukta
    'ੰ': 201,  # Tippi/Bindi
    'ੱ': 202,  # Addak
    'ੑ': 203,  # Udaat
    '੦': 300, '੧': 301, '੨': 302, '੩': 303, '੪': 304,
    '੫': 305, '੬': 306, '੭': 307, '੮': 308, '੯': 309,

    # Punctuation
    '।': 400,  # Danda
    '॥': 401,  # Double Danda
}


def gurmukhi_sort_key(text):
    """
    Generate a sort key for Gurmukhi text based on proper Punjabi alphabetical order.

    Args:
        text (str): Gurmukhi text to generate sort key for

    Returns:
        tuple: A tuple of integers representing the sort order
    """
    if not text:
        return (999999,)

    # Convert text to lowercase equivalent if needed
    text = text.strip()

    # Generate sort key
    sort_key = []
    for char in text:
        # Get the order value for this character
        order_value = GURMUKHI_ALPHABET_ORDER.get(char, 9999)
        sort_key.append(order_value)

    return tuple(sort_key)


def sort_gurmukhi_items(items, key_func=None):
    """
    Sort a list of items containing Gurmukhi text.

    Args:
        items: List of items to sort
        key_func: Optional function to extract the Gurmukhi text from each item
                 If None, assumes items are strings

    Returns:
        list: Sorted list of items
    """
    if key_func is None:
        # Items are strings
        return sorted(items, key=gurmukhi_sort_key)
    else:
        # Items need key extraction
        return sorted(items, key=lambda item: gurmukhi_sort_key(key_func(item)))


def normalize_gurmukhi(text):
    """
    Normalize Gurmukhi text for comparison and searching.
    Handles variations in representation.

    Args:
        text (str): Gurmukhi text to normalize

    Returns:
        str: Normalized text
    """
    if not text:
        return ""

    # Remove zero-width characters
    text = text.replace('\u200b', '')  # Zero-width space
    text = text.replace('\u200c', '')  # Zero-width non-joiner
    text = text.replace('\u200d', '')  # Zero-width joiner

    # Normalize multiple spaces to single space
    import re
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def extract_first_letter_gurmukhi(text):
    """
    Extract the first significant letter from Gurmukhi text.
    Useful for alphabetical grouping.

    Args:
        text (str): Gurmukhi text

    Returns:
        str: First significant letter or empty string
    """
    if not text:
        return ""

    text = normalize_gurmukhi(text)

    # Find first character that's in our alphabet
    for char in text:
        if char in GURMUKHI_ALPHABET_ORDER:
            return char

    return ""


def is_gurmukhi_text(text):
    """
    Check if text contains Gurmukhi characters.

    Args:
        text (str): Text to check

    Returns:
        bool: True if text contains Gurmukhi characters
    """
    if not text:
        return False

    # Gurmukhi Unicode range: U+0A00 to U+0A7F
    for char in text:
        if '\u0A00' <= char <= '\u0A7F':
            return True

    return False
