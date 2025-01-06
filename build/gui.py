#run in thonny
import time
import requests
import os
import datetime
import json
from Adafruit_SSD1306 import SSD1306_128_64
from PIL import Image, ImageDraw, ImageFont
from gpiozero import Buzzer
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
# Replace these with your network and API credentials

# Setup I2C LCD display
display = SSD1306_128_64(rst=None)
display.begin()

display.clear()
display.display()

# Setup Buzzer
buzzer = Buzzer(1) 

def authenticate_google_calendar():
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    # The token.pickle file stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
         with open('token.pickle', 'rb') as token:
             creds = pickle.load(token)

    global service
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
        else:
             flow = InstalledAppFlow.from_client_secrets_file(
                 'credentials.json', SCOPES)
             creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
        
    
    service = build('calendar', 'v3', credentials=creds)


    # Print the events
    
    calendar_list = service.calendarList().list().execute()
    global d
    d=list()
    for calendar in calendar_list['items']:
        if calendar['summary']!="Birthdays":
            d.append(calendar['id'])

def fetch_events():
    calendar_list = service.calendarList().list().execute()
    c_id=d[0]

    now = '1970-01-01T00:00:00Z'  # 'Z' indicates UTC time
    events_result = service.events().list(
        calendarId=c_id, timeMin=now, maxResults=1, singleEvents=True,
        orderBy='startTime').execute()
    
    events = events_result.get('items', [])
    
    # If there are events, print their details
    if not events:
        print('No upcoming events found.')
        c_id=None
    else:
        c_id=None
        print(events)
        return events

def display_event(event):
    title = event['summary']
    start_time = event['start'].get('dateTime', event['start'].get('date'))
    events = events_result.get('items', [])
    # Clear display and show event details
    de=list()
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        de.append(start)
        
    
    display.clear()
    
    # Create a blank image for drawing.
    image = Image.new('1', (display.width, display.height))
    draw = ImageDraw.Draw(image)
    
    # Draw text on the image.
    font = ImageFont.load_default()
    draw.text((0, 0), "Next Event:", font=font, fill=1)
    draw.text((0, 10), title, font=font, fill=1)
    draw.text((0, 20), start_time, font=font, fill=1)
    
    # Display image.
    display.image(image)
    display.display()
    

def main(events):
    
    now=datetime.now()
    current_time = now.strftime("%H:%M")
    count=0
    d=set()

    while count< len(events):
        d.add(current_time)
        d.add(events[count][11:16])
        if len(d)==1:
            buzzer.on()  # Turn on buzzer
            time.sleep(1)  # Beep duration
            buzzer.off()
        else:
            d=set()
            

        time.sleep(60)  # Fetch events every minute

if __name__ == "__main__":
    authenticate_google_calendar()
    b=fetch_events()
    a=display_event(b)
    main(a)
