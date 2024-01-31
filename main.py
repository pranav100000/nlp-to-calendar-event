from client import open_ai_client
from client import google_cal_client
import parsedatetime as pdt
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
openai_client = open_ai_client.OpenAIClient()
google_cal_client = google_cal_client.GoogleCalendarClient()
cal = pdt.Calendar()
now = datetime.now()

statement = input("Enter a statement: ")
print("\n")
resp = openai_client.categorize_calendar_event(statement)

parsed_start_time = cal.parseDT(resp['date_or_day'] + ' ' + resp['start_time'] + ' ' + resp['start_time_am_or_pm'], now)
parsed_end_time = cal.parseDT(resp['date_or_day'] + ' ' + resp['end_time'] + ' ' + resp['end_time_am_or_pm'], now)

# print(f"Unparsed start time: {resp['date_or_day']} {resp['start_time']} {resp['start_time_am_or_pm']}")
# print(f"Unparsed end time: {resp['date_or_day']} {resp['end_time']} {resp['end_time_am_or_pm']}")
# print(f"Parsed start time: {parsed_start_time[0]}")
# print(f"Parsed end time: {parsed_end_time[0]}")


resp['start_time'] = parsed_start_time[0].isoformat(sep='T', timespec='seconds')
resp['end_time'] = parsed_end_time[0].isoformat(sep='T', timespec='seconds')

# print(f"isoformat start time: {resp['start_time']}")
# print(f"isoformat end time: {resp['end_time']}")


google_cal_client.create_event(resp['start_time'], resp['end_time'], resp['title'], resp['location'], resp['description'])

