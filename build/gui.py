import tkinter as tk
from tkinter import ttk
import pickle
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class CalendarApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Google Calendar Events")
        self.geometry("800x600")
        
        # Flags to check if the tables are created
        self.table1_created = False
        self.table2_created = False

        # Initialize the treeview widgets for both tables
        self.tree = None
        self.tree1 = None
        
        self.service = None  # Google Calendar API service object

        # Create buttons for switching between tables
        self.create_buttons()

    def create_buttons(self):
        button1 = tk.Button(self, text="Show Table 1", command=self.creat_t1)
        button1.pack(pady=10)

        button2 = tk.Button(self, text="Show Table 2", command=self.creat_t2)
        button2.pack(pady=10)

    def creat_t1(self):
        if not self.table1_created:
            # Create and configure Table 1
            self.table1_frame = tk.Frame(self)
            self.table1_frame.place(y=134, x=400, height=484)

            self.tree = ttk.Treeview(self.table1_frame, columns=("Summary", "Start Time", "End Time"), show="headings")
            self.tree.heading("Summary", text="Event Summary")
            self.tree.heading("Start Time", text="Start Time")
            self.tree.heading("End Time", text="End Time")

            # Set column width
            self.tree.column("Summary", width=200)
            self.tree.column("Start Time", width=150)
            self.tree.column("End Time", width=150)

            # Fetch events for the first calendar
            events_data = self.get_calendar_events(self.service, 'divinishimwedusenge@gmail.com')
            
            # Insert event data into table
            for event in events_data:
                start_time = self.convert_utc_to_local(str(event["start"]['dateTime']))
                end_time = self.convert_utc_to_local(str(event["end"]['dateTime']))
                self.tree.insert("", "end", values=(event["summary"], start_time, end_time))

            # Style the Treeview
            self.style_treeview()

            # Place Treeview widget on the window
            self.tree.place(x=400, y=134, height=484)
            self.table1_created = True

        if self.table2_created:
            self.table2_frame.pack_forget()
            self.table2_created = False

    def creat_t2(self):
        if not self.table2_created:
            # Create and configure Table 2
            self.table2_frame = tk.Frame(self)
            self.table2_frame.place(y=134, x=400, height=484)

            self.tree1 = ttk.Treeview(self.table2_frame, columns=("Summary", "Start Time", "End Time"), show="headings")
            self.tree1.heading("Summary", text="Event Summary")
            self.tree1.heading("Start Time", text="Start Time")
            self.tree1.heading("End Time", text="End Time")

            # Set column width
            self.tree1.column("Summary", width=200)
            self.tree1.column("Start Time", width=150)
            self.tree1.column("End Time", width=150)

            # Fetch events for the second calendar
            events_data = self.get_calendar_events(self.service, 'e2bb577c71d9ce40d419b3bb474fe7b55a9474693b978a98da455cb56cc3cf91@group.calendar.google.com')
            
            # Insert event data into table
            for event in events_data:
                start_time = self.convert_utc_to_local(str(event["start"]['dateTime']))
                end_time = self.convert_utc_to_local(str(event["end"]['dateTime']))
                self.tree1.insert("", "end", values=(event["summary"], start_time, end_time))

            # Style the Treeview
            self.style_treeview()

            # Place Treeview widget on the window
            self.tree1.place(x=400, y=134, height=484)
            self.table2_created = True

        if self.table1_created:
            self.table1_frame.pack_forget()
            self.table1_created = False

    def style_treeview(self):
        # Style the Treeview widget
        style = ttk.Style()
        style.configure("Treeview",
                        font=('Arial', 10),
                        rowheight=30,  # Row height for readability
                        background="#f0f0f0",  # Default background color
                        foreground="black")  # Default text color
        style.configure("Treeview.Heading",
                        font=('Arial', 12, 'bold'),
                        background="#4CAF50",  # Green background for headers
                        foreground="white")  # White text for headers
        style.map('Treeview',
                  background=[('selected', '#A1D2A6')])  # Light green for selected rows

    def get_calendar_events(self, service, calendar_id):
        self.now = '1970-01-01T00:00:00Z'  # 'Z' indicates UTC time
        events_result = service.events().list(
            calendarId=calendar_id, timeMin=self.now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()

        events = events_result.get('items', [])
        if not events:
            print('No upcoming events found.')
        return events

    def convert_utc_to_local(self, utc_time_str):
        from datetime import datetime
        from dateutil import parser
        utc_time = parser.isoparse(utc_time_str)
        local_time = utc_time.astimezone()  # Convert UTC to local time
        return local_time.strftime("%Y-%m-%d %H:%M:%S")

    def login(self):
        # Assuming the login method and service object creation is handled here
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow

        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)

if __name__ == "__main__":
    app = CalendarApp()
    app.login()  # Login first before running the app
    app.mainloop()
