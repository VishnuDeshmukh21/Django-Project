from django.shortcuts import redirect
from django.urls import reverse

class FirebaseUidMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the requested path
        path = request.path

        # Check if the request is for the profile view or edit page
        if path.startswith('/accounts/profile/'):
            # Only process the middleware logic for profile view and edit requests
            if not request.user.is_authenticated:
                # If user is not authenticated, redirect to the login page
                return redirect(reverse('login'))

        response = self.get_response(request)
        return response
