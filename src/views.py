# calendar_api/views.py

from django.shortcuts import redirect
from django.views import View
from django.conf import settings
from google.oauth2 import client


class GoogleCalendarInitView(View):
    def get(self, request):
        flow = client.OAuth2WebServerFlow(
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            redirect_uri=settings.GOOGLE_REDIRECT_URI,
            scope='https://www.googleapis.com/auth/calendar.readonly',
        )
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
        )
        request.session['oauth2_state'] = state
        return redirect(authorization_url)


class GoogleCalendarRedirectView(View):
    def get(self, request):
        code = request.GET.get('code')
        state = request.GET.get('state')
        if state != request.session.get('oauth2_state'):
            return redirect('error-url')  # Redirect to an error page if state doesn't match

        flow = client.OAuth2WebServerFlow(
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            redirect_uri=settings.GOOGLE_REDIRECT_URI,
            scope='https://www.googleapis.com/auth/calendar.readonly',
        )
        flow.fetch_token(code=code)

        credentials = flow.credentials
        # Use the credentials to fetch events from the user's calendar

        return redirect('success-url')  # Redirect to a success page

