from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle
import os
from google.auth.transport.requests import Request

# Scopes required to access and modify Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'google_cal_creds.json'
TOKEN_FILE = 'token.pickle'


class GoogleCalendarClient:
    
    def __init__(self):
        creds = None
        # Check if token file exists
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials are available, request user authorization
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)


    def create_event(self, start_time_str, end_time_str, summary, location, description, all_day=False, recurrence_rule=None):
        if all_day:
            # For all-day events, use 'date' key instead of 'dateTime'
            event['start'] = {'date': start_time_str}
            event['end'] = {'date': end_time_str}
        else:
            # For specific-time events, use 'dateTime' and 'timeZone'
            event['start'] = {
                'dateTime': start_time_str,
                'timeZone': 'Your/Timezone',
            }
            event['end'] = {
                'dateTime': end_time_str,
                'timeZone': 'Your/Timezone',
            }
        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_time_str,
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': end_time_str,
                'timeZone': 'America/Los_Angeles',
            },
        }
            
        if recurrence_rule:
            event['recurrence'] = [recurrence_rule]
        

        event = self.service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")

# Example usage
# gcc = GoogleCalendarClient()
# gcc.create_event('2024-02-15T09:00:00', '2024-02-15T10:00:00', 'Meeting with Bob', '123 Main St', 'Discussing project updates')
