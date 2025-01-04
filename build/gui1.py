from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, Frame,ttk,BOTH,Entry,END
import os
#import datetime
import re


# Define OUTPUT_PATH for assets
OUTPUT_PATH = Path(__file__).parent

# Dynamically set the asset path based on the context
def get_assets_path(frame_version="frame1"):
    if frame_version == "frame1":
        return OUTPUT_PATH / Path(r"C:\Users\hp\Desktop\my projects\programm\build\assets2\frame0")
    else:
        return OUTPUT_PATH / Path(r"C:\Users\hp\Desktop\my projects\programm\build\assets\frame0")

# Function to return relative path to asset
def relative_to_assets(path: str, frame_version="frame1") -> Path:
    ASSETS_PATH = get_assets_path(frame_version)
    return ASSETS_PATH / Path(path)

class Application:
    def __init__(self, window):
        self.window = window
        self.window.geometry("900x700")
        self.window.configure(bg="#FFFFFF")
        self.window.resizable(False, False)

        # Create frames
        self.frame1 = Frame1(self.window, self.show_frame2)
        self.frame2 = Frame2(self.window, self.show_frame1)

        # Initially show frame1
        self.frame1.place(x=0, y=0, relwidth=1, relheight=1)

    def show_frame1(self):
        """Switch to Frame 1"""
        self.frame2.place_forget()  # Hide frame2
        self.frame1.place(x=0, y=0, relwidth=1, relheight=1)  # Show frame1

    def show_frame2(self):
        """Switch to Frame 2"""
        self.frame1.place_forget()  # Hide frame1
        self.frame2.place(x=0, y=0, relwidth=1, relheight=1)  # Show frame2


class Frame1(Frame):
    def __init__(self, parent, switch_frame_callback):
        super().__init__(parent, bg="#FFFFFF")
        self.switch_frame_callback = switch_frame_callback

        # Initialize widgets for Frame 1
        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=700,
            width=900,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        self.create_widgets()

    def create_widgets(self):
        # Create images on the canvas
        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.canvas.create_image(450.0, 350.0, image=self.image_image_1)

        self.image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        self.canvas.create_image(450.0296325683594, 75.0, image=self.image_image_2)

        self.image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
        self.canvas.create_image(446.0518569946289, 406.0, image=self.image_image_3)

        self.image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
        self.canvas.create_image(445.5629577636719, 460.0, image=self.image_image_4)

        self.image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
        self.canvas.create_image(87.08148193359375, 83.0, image=self.image_image_5)

        # Create Button 1 with hover effect
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.login,
            relief="flat"
        )
        self.button_1.place(x=381.0, y=51.0, width=137.0, height=51.0)

        self.button_image_hover_1 = PhotoImage(file=relative_to_assets("button_hover_1.png"))
        self.button_1.bind('<Enter>', self.button_1_hover)
        self.button_1.bind('<Leave>', self.button_1_leave)

    def login(self):
        
        import pickle
        
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        
        global service

        creds = None
        SCOPES = ['https://www.googleapis.com/auth/calendar']
    # The token.pickle file stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

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
        self.switch_frame_callback()
        service = build('calendar', 'v3', credentials=creds)
        events_result = service.events().list(
        calendarId='primary', 
        maxResults=10, 
        singleEvents=True, 
        orderBy='startTime'
        ).execute()
        #print(events_result)

    # Print the events
    
        calendar_list = service.calendarList().list().execute()
        global d
        d=list()
        for calendar in calendar_list['items']:
            if calendar['summary']!="Birthdays":
                d.append(calendar['id'])
        print(d)


    # Hover effect for Button 1
    def button_1_hover(self, event):
        self.button_1.config(image=self.button_image_hover_1)

    def button_1_leave(self, event):
        self.button_1.config(image=self.button_image_1)

class Frame2(Frame):
    def __init__(self, parent, switch_frame_callback):
        super().__init__(parent, bg="#070E21")
        self.switch_frame_callback = switch_frame_callback
        self.table1_created = False
        self.table2_created = False
        
        # Frames to hold the tables
        self.table1_frame = None
        self.table2_frame = None
        
        # Initialize widgets for Frame 2
        self.canvas = Canvas(self, bg="#070E21", height=700, width=900, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png", frame_version="frame2"))
        self.canvas.create_image(463.0, 350.0, image=self.image_image_1)

        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png", frame_version="frame2"))
        self.button_1 = Button(self, image=self.button_image_1, borderwidth=0, highlightthickness=0,
                               command=lambda:print("button_1 clicked"), relief="flat")
        self.button_1.place(x=659.0, y=30.0, width=160.0, height=46.0)

        self.button_image_hover_1 = PhotoImage(file=relative_to_assets("button_hover_1.png", frame_version="frame2"))
        self.button_1.bind('<Enter>', self.button_1_hover)
        self.button_1.bind('<Leave>', self.button_1_leave)

        self.canvas.create_rectangle(21.0, 137.0, 335.0, 611.0, fill="#9FBBD3", outline="")

        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png", frame_version="frame2"))
        self.button_2 = Button(self, image=self.button_image_2, borderwidth=0, highlightthickness=0,
                               command=self.creat_t2, relief="flat")
        self.button_2.place(x=35.0, y=403.0, width=282.2049, height=80.0705)

        self.button_image_3 = PhotoImage(file=relative_to_assets("button_3.png", frame_version="frame2"))
        self.button_3 = Button(self, image=self.button_image_3, borderwidth=0, highlightthickness=0,
                               command=self.creat_t1, relief="flat")
        self.button_3.place(x=35.0, y=232.0, width=285.2049, height=80.0705)

        self.button_image_4 = PhotoImage(file=relative_to_assets("button_4.png", frame_version="frame2"))
        self.button_4 = Button(self, image=self.button_image_4, borderwidth=0, highlightthickness=0,
                               command=self.save, relief="flat")
        self.button_4.place(x=51.0, y=30.0, width=143.0, height=47.0)

        self.image_image_2 = PhotoImage(file=relative_to_assets("image_2.png", frame_version="frame2"))
        self.canvas.create_image(638.0, 374.0, image=self.image_image_2)

        self.button_image_5 = PhotoImage(file=relative_to_assets("button_5.png", frame_version="frame2"))
        self.button_5 = Button(self, image=self.button_image_5, borderwidth=0, highlightthickness=0,
                               command=self.logout, relief="flat")
        self.button_5.place(x=377.0, y=30.0, width=161.0, height=46.0)
        self.tree = ttk.Treeview(self, columns=("Summary", "Start Time", "End Time"), show="headings")
        self.tree1 = ttk.Treeview(self, columns=("Summary", "Start Time", "End Time"), show="headings")
        
        # Define column headings
    def creat_t1(self):
        if not self.table1_created:
            # Create and configure Table 1
            self.table1_frame =Frame(self)
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
            events_data = self.get_calendar_events(service, d[0])
            
            if events_data is not None:
                self.tempo1= events_data
            else:
                self.tempo1=self.tree.get_children()
            # Insert event data into table
            try:
                if events_data is not None:
                    for event in events_data:
                        start_time = self.convert_utc_to_local(str(event["start"]['dateTime']))
                        end_time = self.convert_utc_to_local(str(event["end"]['dateTime']))
                        self.tree.insert("", "end", values=(event["summary"], start_time, end_time))
                else:
                    global all_items1
                    all_items1 = [self.tree1.item(item)["values"] for item in self.tree1.get_children("")]
                    for a in all_items:
                        self.tree.insert("", "end", values=tuple(a))

            except Exception as err:
                print(err)

            # Style the Treeview
            self.style_treeview()

            # Place Treeview widget on the window
            self.tree.pack(fill=BOTH, expand=True)
            self.table1_created = True
            self.entering(self.table1_frame,self.tree)

        if self.table2_created:
            self.table2_created = False
        self.tree.bind("<BackSpace>",lambda e:self.tree.delete(self.tree.selection()))



    def creat_t2(self):
        if not self.table2_created:
            # Create and configure Table 2
            self.table2_frame =Frame(self)
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
            events_data = self.get_calendar_events(service, d[-1])
            if events_data is not None:
                self.tempo= events_data
            # Insert event data into table
            try:
                if events_data is not None:
                    for event in events_data:
                        start_time = self.convert_utc_to_local(str(event["start"]['dateTime']))
                        end_time = self.convert_utc_to_local(str(event["end"]['dateTime']))
                        self.tree1.insert("", "end", values=(event["summary"], start_time, end_time))
                
                else:
                    global all_items
                    all_items = [self.tree.item(item)["values"] for item in self.tree.get_children("")]
                    for a in all_items1:
                        self.tree1.insert("", "end", values=tuple(a))   
                        
            except Exception as err:
                print(err)

            # Style the Treeview
            self.style_treeview()

            # Place Treeview widget on the window
            self.tree1.pack(fill=BOTH, expand=True)

            self.table2_created = True

            self.entering(self.table2_frame,self.tree1)

        if self.table1_created:
            self.table1_created = False
        self.tree1.bind("<BackSpace>",lambda e:self.tree1.delete(self.tree1.selection()))

    def get_calendar_events(self,service,c_id):
        calendar_list = service.calendarList().list().execute()
        self.c_id=c_id

        self.now = '1970-01-01T00:00:00Z'  # 'Z' indicates UTC time
        self.events_result = service.events().list(
            calendarId=self.c_id, timeMin=self.now, maxResults=15, singleEvents=True,
            orderBy='startTime').execute()
        
        self.events = self.events_result.get('items', [])
        for i in self.events:
            service.events().delete(calendarId=self.c_id, eventId=i['id']).execute()
    
        # If there are events, print their details
        if not self.events:
            print('No upcoming events found.')
            self.c_id=None
        else:
            self.c_id=None
            return self.events

    def entering(self,parents,tree):
        #place the event summary
        self.entry1=Entry(parents,justify='left')
        self.entry1.insert(0,"input event")
        self.entry1.pack(side="left",fill=BOTH, expand=True)
            #place start time
        self.entry2=Entry(parents,justify='left')
        self.entry2.insert(0,"00:00")
        self.entry2.pack(side="left",fill=BOTH, expand=True)

        #place end time
        self.entry3=Entry(parents,justify='left')
        self.entry3.insert(0,"00:00")
        self.entry3.pack(side="left",fill=BOTH, expand=True)
            #button
        style = ttk.Style()
        # Configure the style for TButton
        style.configure("Custom.TButton", background="green", foreground="white")
        self.btn=ttk.Button(parents,text="ENTER",command=lambda:self.register(self.entry1,self.entry2,self.entry3,tree),style="Custom.TButton")
        self.btn.pack(side="left",fill=BOTH, expand=True)

    def tree_acces(self,access,values):
        access.insert(parent='', index=END, values=values)

    def register(self,event,strt,end,acs):
        values = [event.get(), strt.get(), end.get()]
        pattern = r'^(?:[01]\d|2[0-3]):[0-5]\d$'
        if bool(re.match(pattern, values[1])) and bool(re.match(pattern, values[2])):
            self.tree_acces(acs,values) 

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
                        foreground="black")  # White text for headers
        style.map('Treeview',
                  background=[('selected', '#A1D2A6')]) 

    def convert_utc_to_local(self, utc_time_str):
        # Convert UTC to local time for display purposes
        utc_time = datetime.datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%S%z")
        local_time = utc_time.strftime("%H:%M")
        return local_time

    def save(self):
        for a in all_items:
            event = {
                'summary': f'{a[0]}',
                'location': 'college st andre',
                'description': 'Time Table',
                'start': {
                    'dateTime': f'2025-01-01T{a[1][:2]}:{a[1][3:]}:00+02:00',  # Adjust time zone as needed
                    'timeZone': 'Africa/Maputo',
                },
                'end': {
                    'dateTime': f'2025-01-01T{a[1][:2]}:{a[1][3:]}:00+02:00',  # Adjust time zone as needed
                    'timeZone': 'Africa/Maputo',
                },
                'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=1'  # This sets it to repeat daily for 10 occurrences
        ],
                'reminders': {
                    'useDefault': True
                    
                },
                'eventType': 'default'  
            }
            event = service.events().insert(calendarId=d[0], body=event).execute()

        for a in all_items1:
            event = {
                'summary': f'{a[0]}',
                'location': 'college st andre',
                'description': 'Time Table',
                'start': {
                    'dateTime': f'2025-01-01T{a[1][:2]}:{a[1][3:]}:00+02:00',  # Adjust time zone as needed
                    'timeZone': 'Africa/Maputo',
                },
                'end': {
                    'dateTime': f'2025-01-01T{a[2][:2]}:{a[2][3:]}:00+02:00',  # Adjust time zone as needed
                    'timeZone': 'Africa/Maputo',
                },
                'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=1'  # This sets it to repeat daily for 1 occurrence
        ],
                'reminders': {
                    'useDefault': True
                    
                },
                'eventType': 'default'
            }
            event = service.events().insert(calendarId=d[-1], body=event).execute()



    def logout(self):
        if os.path.exists('token.pickle'):
            os.remove('token.pickle')
            print("Logged out successfully!")

        # You can also clear the credentials object if it's in memory
        self.switch_frame_callback()

    def button_1_hover(self, event):
        self.button_1.config(image=self.button_image_hover_1)

    def button_1_leave(self, event):
        self.button_1.config(image=self.button_image_1)


# Run the application
if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()

"""LORD OF THE MYSTERIES"""
