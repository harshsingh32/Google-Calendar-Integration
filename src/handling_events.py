from django.shortcuts import redirect, render
from django.views import View
from django.conf import settings
from google.oauth2 import client
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


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
        try:
            credentials = flow.fetch_token(code=code)
        except client.FlowExchangeError:
            return redirect('error-url')  # Redirect to an error page if token exchange fails

        try:
            service = build('calendar', 'v3', credentials=credentials)
            events_result = service.events().list(calendarId='primary', maxResults=10).execute()
            events = events_result.get('items', [])
        except HttpError as e:
            return redirect('error-url')  # Redirect to an error page if there's an API error

        return render(request, 'events.html', {'events': events})

