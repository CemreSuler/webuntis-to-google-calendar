"""
This is the main program
"""
import os
from os import path

import sys
import threading
import datetime
import json
import subprocess
import webuntis
import time

CURRENT = os.path.dirname(sys.argv[0])
TODAY = datetime.date.today()
END = TODAY + datetime.timedelta(days=14)

if not path.exists(CURRENT + 'config.json'):
    CONFIG = ['python3', 'config.py']
    subprocess.Popen(CONFIG).wait()

from google_cal import add_event, delete_events

with open(CURRENT + "config.json") as FILE:
    DATA = json.load(FILE)
    global USERNAME, PASSWORD, SERVER, SCHOOL, STUDENTID
    USERNAME = DATA["username"]
    PASSWORD = DATA["password"]
    SERVER = DATA["server"]
    SCHOOL = DATA["school"]
    STUDENTID = DATA["webuntis_id"]
    
try:
    if path.exists(CURRENT + "wrong_pass"):
        print("Last time wrong password, not trying again")
        exit()
    with webuntis.Session(
        username=USERNAME,
        password=PASSWORD,
        server=SERVER,
        school=SCHOOL,
        useragent='Chrome'
    ).login() as s:
        LESSON_REQ = s.timetable(student=STUDENTID, start=TODAY, end=END)
        from string import digits
        remove_digits = str.maketrans('', '', digits)
        delete_events()
        for lesson in LESSON_REQ:
            if lesson.code != 'cancelled':
                lesson.rooms = str(lesson.rooms).replace("[", "")
                lesson.rooms = str(lesson.rooms).replace("]", "")
                lesson.subjects = str(lesson.subjects).replace("[", "")
                lesson.subjects = str(lesson.subjects).replace("]", "")
                if(lesson.start.strftime("%H:%M") == "08:20"):
                    s = "1"
                
                if(lesson.start.strftime("%H:%M") == "09:10"):
                    s = "2"
                    
                if(lesson.start.strftime("%H:%M") == "10:00"):
                    s = "3"
                    
                if(lesson.start.strftime("%H:%M") == "11:10"):
                    s = "4"
                
                if(lesson.start.strftime("%H:%M") == "12:00"):
                    s = "5"
                    
                if(lesson.start.strftime("%H:%M") == "13:20"):
                    s = "6"
                
                if(lesson.start.strftime("%H:%M") == "14:10"):
                    s = "7"
                    
                if(lesson.start.strftime("%H:%M") == "15:00"):
                    s = "8"
                    
                if(lesson.start.strftime("%H:%M") == "15:50"):
                    s = "9"
                
                
                thread = threading.Thread(target=add_event, 
                    args=(lesson.start, lesson.end, s + " - " + lesson.subjects.upper().translate(remove_digits) + " - " + lesson.rooms, " ",))
                thread.start()
                time.sleep(0.2)
except webuntis.errors.BadCredentialsError:
    print("Wrong password")
    FILE = open(CURRENT + "wrong_pass", "w+")
    FILE.close()
