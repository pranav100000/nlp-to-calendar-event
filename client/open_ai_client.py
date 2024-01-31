import os
import numpy as np
from openai import OpenAI
from numpy.linalg import norm
import json
import retry
import logging
from dotenv import load_dotenv

class OpenAIClient:
    MODEL = "gpt-4"
    EMBEDDING_MODEL = "text-embedding-ada-002"
    calendar_event_types = ["meeting", "appointment", "reminder", "event", "N/A"]
    CATEGORIZE_CALENDAR_EVENT_TOOLS = [
        {
            "type": "function",
            "function": {
                "name": "categorize_calendar_event",
                "description": "You are a helpful calendar assistant. Given a statement, determine if a calendar event can be created from the statement, and get the type of event, date or day, start time, end time, duration, location, title, and description of the calendar event, and determine whether the event is repeating, and its frequency if it is.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "can_create_calendar_event": {
                            "type": "boolean",
                            "description": "Whether a calendar event can be created from the statement."
                        },
                        "type": {
                            "type": "string",
                            "enum": calendar_event_types,
                            "description": "The type of the calendar event."
                        },
                        "date_or_day": {
                            "type": "string",
                            "description": "The date or day of the calendar event. Could be a specific date or a day of the week. For example, 'Next Monday' or 'February 8'."
                        },
                        "event_is_all_day": {
                            "type": "boolean",
                            "description": "Whether the calendar event is an all-day event."
                        },
                        "event_is_repeating": {
                            "type": "boolean",
                            "description": "Whether the calendar event is repeating."
                        },
                        "frequency": {
                            "type": "string",
                            "description": "The frequency of the repeating calendar event. If the event is not repeating, this should be 'N/A'."
                        },
                        "start_time": {
                            "type": "string",
                            "description": "The start time of the calendar event. If the event is an all-day event, this should be 'N/A'."
                        },
                        "start_time_am_or_pm": {
                            "type": "string",
                            "enum": ["AM", "PM"],
                            "description": "Whether the start time is in the morning or the afternoon."
                        },
                        "end_time": {
                            "type": "string",
                            "description": "The end time of the calendar event. If the event is an all-day event, this should be 'N/A'."
                        },
                        "end_time_am_or_pm": {
                            "type": "string",
                            "enum": ["AM", "PM"],
                            "description": "Whether the end time is in the morning or the afternoon."
                        },
                        "duration": {
                            "type": "string",
                            "description": "The duration of the calendar event. If the event is an all-day event, this should be 'N/A'."
                        },
                        "location": {
                            "type": "string",
                            "description": "The location of the calendar event. If location is not mentioned, this should be 'N/A'."
                        },
                        "title": {
                            "type": "string",
                            "description": "A short title for the calendar event."
                        },
                        "description": {
                            "type": "string",
                            "description": "A description of the calendar event."
                        },
                    },
                    "required": ["can_create_calendar_event", "type", "date_or_day", "event_is_all_day", "event_is_repeating", "frequency", "start_time", "start_time_am_or_pm", "end_time", "end_time_am_or_pm", "duration", "location", "title", "description"]
                }
            }
        }
    ]
    
    def __init__(self) -> None:
        self.client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))
        
    @retry.retry(tries=3, delay=2)
    def categorize_calendar_event(self, statement):
        logging.debug("Categorizing: " + statement)
        response = self.client.chat.completions.create(
            model=self.MODEL,
            n=1,
            temperature=0.1,
            messages=[{"role": "user", "content": statement}],
            tools=self.CATEGORIZE_CALENDAR_EVENT_TOOLS,
            tool_choice={"type": "function", "function": {"name": "categorize_calendar_event"}}
        )
        json_resp = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        if json_resp is None: 
            raise Exception("categorize_calendar_event response is None")
        logging.debug("categorize_calendar_event response: " + str(json_resp))
        for key, value in json_resp.items():
            print(f"{key}: {value}")
        
        return json_resp


# load_dotenv()
# openai_client = OpenAIClient()
# resp = openai_client.categorize_calendar_event("I have a yoga class next Monday 10am for 45 minutes with John Doe at LA fitness.")
# print(resp)