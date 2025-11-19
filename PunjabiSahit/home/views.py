# home/views.py
"""
View functions for the Punjabi Sahit home application.

This module contains AJAX endpoints and view handlers for:
- Book reading status management
- User interactions with books (favorites, ratings, notes)
"""

import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import UserBookStatus, BookPage


@login_required
@require_POST
def update_book_status(request):
    """
    AJAX endpoint to update user's reading status for a book.

    Args:
        request: HTTP POST request containing JSON data with:
            - book_id: ID of the book
            - status: Reading status ('to_read', 'reading', 'read', 'completed')
            - is_favorite: Boolean indicating favorite status
            - current_page: Current page number
            - rating: Rating from 1-5
            - notes: Personal notes about the book

    Returns:
        JsonResponse: Success status and updated book status data

    Raises:
        400: If invalid data is provided
        404: If book is not found
    """
    try:
        data = json.loads(request.body)
        book_id = data.get('book_id')
        status = data.get('status')
        is_favorite = data.get('is_favorite')
        current_page = data.get('current_page')
        rating = data.get('rating')
        notes = data.get('notes')

        # Validate book exists
        try:
            book = BookPage.objects.get(id=book_id)
        except BookPage.DoesNotExist:
            return JsonResponse({'error': 'Book not found'}, status=404)

        # Get or create user book status
        user_status, created = UserBookStatus.objects.get_or_create(
            user=request.user,
            book=book
        )

        # Update fields
        if status is not None:
            user_status.status = status
        if is_favorite is not None:
            user_status.is_favorite = is_favorite
        if current_page is not None:
            user_status.current_page = current_page
        if rating is not None:
            user_status.rating = rating
        if notes is not None:
            user_status.notes = notes

        user_status.save()

        return JsonResponse({
            'success': True,
            'status': user_status.get_status_display(),
            'is_favorite': user_status.is_favorite,
            'progress_percentage': user_status.progress_percentage,
            'rating': user_status.rating,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@require_POST
def delete_book_status(request):
    """
    AJAX endpoint to delete user's book status.

    Args:
        request: HTTP POST request containing JSON data with:
            - book_id: ID of the book whose status should be deleted

    Returns:
        JsonResponse: Success status

    Raises:
        400: If invalid data is provided
    """
    try:
        data = json.loads(request.body)
        book_id = data.get('book_id')

        # Delete the status
        UserBookStatus.objects.filter(
            user=request.user,
            book_id=book_id
        ).delete()

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
