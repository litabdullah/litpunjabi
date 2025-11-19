"""
Middleware for tracking page view counts in the Punjabi Sahit application.

This middleware automatically increments the view_count field for any page
that inherits from BaseContentPage when it's successfully viewed.
"""

from django.db.models import F
from home.models import BaseContentPage


class PageViewCounterMiddleware:
    """
    Middleware to automatically track page views for content pages.

    This middleware increments the view_count field for any page that has it
    (typically pages inheriting from BaseContentPage). The increment is done
    atomically using F() expressions to avoid race conditions.

    The counter only increments for:
    - GET requests
    - Successful responses (status 200)
    - Non-preview requests
    - Pages with a view_count field
    """

    def __init__(self, get_response):
        """
        Initialize the middleware.

        Args:
            get_response: The next middleware or view in the chain
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Process the request and increment view count if applicable.

        Args:
            request: The HTTP request object

        Returns:
            HttpResponse: The response from the next middleware/view
        """
        response = self.get_response(request)

        # We only want to count views for GET requests that are successful (status 200)
        # and are not in the admin preview.
        if (
            response.status_code == 200
            and hasattr(request, 'wagtail_page')
            and not request.is_preview
        ):
            # Get the actual page object
            page = request.wagtail_page

            # Check if this page is one of our content types by seeing if
            # it has the 'view_count' attribute. This is a simple and effective check.
            if hasattr(page, 'view_count'):
                # Use F() expression to perform an atomic update, which is highly
                # efficient and avoids race conditions.
                page_model = page.specific_class
                page_model.objects.filter(pk=page.pk).update(view_count=F('view_count') + 1)
        
        return response