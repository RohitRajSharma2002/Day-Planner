from tkinter import *
import datetime
from datetime import date   
from datetime import datetime as dt
import calendar
import csv
import backend #to use functions in the backend it must be imported
import os
import random

global Entries
global colors

colors = ["red", "black", "green", "blue", 'pink','yellow','orange', 'gold']
Entries = {}
Events= {}
def createFile():
    if os.path.exists("\\remindersData.csv') == False:
           # check if file exists
        with open('remindersData.csv', 'w', newline = '') as file:
            writer = csv.writer(file)
            writer.writerow(["DATE", "NAME", "TYPE", "LENGTH", 'START', 'END'])
    print(os.getcwd()) 

def countdown():
    dateList = []
    nameList = []
    with open('\\calenderData.csv', 'r') as dates:
        reader = csv.reader(dates)
        next(reader)
        for i in reader:
            dateList.append(i[0])
            nameList.append(i[1])
    curYear = dt.now().year
    for i in dateList:
        if i == "01-01":
            if dt.today().month != 1:
                curYear = date.today().year + 1
                today = str(calendar.monthrange(dt.today().year, dt.today().month)[1] - dt.today().day) 
            else:
                pass            

        timeDiff = dt.strptime(str(curYear)+"-"+ i ,'%Y-%m-%d') - dt.today()
        #print(timeDiff)
        if timeDiff < datetime.timedelta(days = 10) and timeDiff >= datetime.timedelta(days =-1):
            if timeDiff > datetime.timedelta(days = 1): #more than 1 day letf
                if i == '01-01':
                    daysTo = today + " days to go to " + nameList[dateList.index(i)]
                    break
                else: 
                    daysTo = str(int(i[-2:]) - int(dt.today().day)) + " days to go to " + nameList[dateList.index(i)]
                    break
            elif str(curYear)+"-"+i == dt.strftime(dt.today(), '%Y-%m-%d'): # if today is  the day
                daysTo = "Today is " + nameList[dateList.index(i)]
                break
            elif timeDiff < datetime.timedelta(days = 0, hours = 24): # 24H countdown
                daysTo = str(dt.strptime(str(curYear)+'-'+i, '%Y-%m-%d') - dt(year = dt.now().year, month = dt.now().month, day = dt.now().day ,minute = dt.now().minute, second = dt.now().second)) + ' to '+nameList[dateList.index(i)]
                break
        else:
            if i != dateList[-1]: # if not EOL
                daysTo = None
                pass
            else:                # IF EOL
                daysTo = None 
                break

    return daysTo

def refresh(stringvar, time):
    global plannerWindow
    if time != dt.now():
        countdown_text = countdown()
        #text_to_display = stringvar.set()
        stringvar.set(countdown_text)
        plannerWindow.update()
    plannerWindow.after(200, lambda: refresh(stringvar, time))

def defineLength():
    def proceed():
        submit_entry()
        root.destroy()
    root = Tk()
    topFrame = Frame(root)
    topFrame.pack(side = TOP)
    bottomFrame = Frame(root)
    bottomFrame.pack(side = BOTTOM) 
    contentFrame = Frame(bottomFrame)
    buttonFrame = Frame(bottomFrame)
    contentFrame.pack(side = TOP)
    buttonFrame.pack(side = BOTTOM)
    Message(topFrame,text= "Select length - \n").pack(side = TOP)
    createEntry.start = Entry(contentFrame)
    createEntry.end = Entry(contentFrame)
    Message(contentFrame, text = "From -").pack(side = LEFT, pady = (11,0))
    createEntry.start.pack(side = LEFT)
    Message(contentFrame,text= "To -").pack(side = LEFT, pady = (0,3))
    createEntry.end.pack(side = LEFT, padx = (0,5))
    Button(buttonFrame, text = "submit", command = proceed).pack()
    root.mainloop()
    
def submit_entry():
    if createEntry.eventLengthVar.get() == createEntry.subEventType[0]:
            exportData = [frontEnd.dateVar.get(),createEntry.entry.get(), createEntry.eventTypeVar.get(), createEntry.eventLengthVar.get(), 'N\A', 'N\A']
            createEntry.submitE.pack_forget()
            exportToCSV(exportData)
    else:
        try:
            exportData = [frontEnd.dateVar.get(),createEntry.entry.get(), createEntry.eventTypeVar.get(), createEntry.eventLengthVar.get(), createEntry.start.get(), createEntry.end.get()]
            exportToCSV(exportData)
        except:
            defineLength()
        else:
            createEntry.submitE.pack_forget()

        
def exportToCSV(exportData):                   # function to write to csv file
    try:
        with open('remindersData.csv', 'a', newline = '') as file:
                writer = csv.writer(file)
                #removed the square brackets around exportData, this prevented writing to the csv properly
                writer.writerow(exportData)  # export data to csv
                                                # input coming from line 60
                print("exported")
    except:
        print('something went wrong....')


def createEntry():
    

    createEntry.evenTypes = ['Reminder', 'Event']                                              # create window for entering events
    createEntry.subEventType = ['All-Day', 'Limited']                               
    replicateFrame = Frame(rightFrame, highlightbackground = colors[random.randint(0,len(colors)-1)], highlightthickness = 2)
    labelFrame = Frame(replicateFrame)
    entryFrame = Frame(replicateFrame)
    replicateFrame.pack(side = TOP)
    labelFrame.pack(side = LEFT)
    entryFrame.pack(side = RIGHT)

    createEntry.eventTypeVar = StringVar(entryFrame)
    createEntry.eventLengthVar = StringVar(entryFrame)
    createEntry.eventTypeVar.set("Select type")
    createEntry.eventLengthVar.set("Select length")
    createEntry.eventSelector = OptionMenu(entryFrame, createEntry.eventTypeVar, *createEntry.evenTypes)
    createEntry.eventSelector.pack(side = LEFT)
    createEntry.eventLength = OptionMenu(entryFrame, createEntry.eventLengthVar, *createEntry.subEventType)
    createEntry.eventLength.pack(side = LEFT)


    Label(labelFrame, text =str("Entry #" + str(frontEnd.counter))).pack()
    createEntry.entry = Entry(entryFrame)
    createEntry.entry.pack(side = TOP)
    
    createEntry.submitE = Button(entryFrame, text = "SUBMIT ENTRY", command = submit_entry)
    createEntry.submitE.pack(side = TOP)
    createEntry.addEvent = Button(entryFrame, text = "ADD EVENT", command = add_entry)
    createEntry.addEvent.pack(side = TOP)


def add_entry():                              # call the window creation function for another entry
    createEntry.addEvent.pack_forget()
    frontEnd.counter += 1
    createEntry()

def createmail():                           # convert input to email format 
    frontEnd.email_text = ""
    for i in Entries:
        frontEnd.email_text += i +" \n"
    frontEnd.submit.pack_forget()
    email()



def frontEnd(): 
    global plannerWindow, rootFrame, topFrame, bottomFrame, leftFrame, rightFrame                                          # creates the interface window
    frontEnd.counter = 1
    plannerWindow = Tk()                        # the root window
    rootFrame = Frame(plannerWindow)
    topFrame = Frame(rootFrame)
    bottomFrame = Frame(rootFrame)
    leftFrame = Frame(topFrame, highlightbackground = colors[random.randint(0,len(colors)-1)], highlightthickness = 2)
    rightFrame = Frame(topFrame)
    rootFrame.pack()
    topFrame.pack(side = TOP)
    bottomFrame.pack(side = BOTTOM)
    leftFrame.pack(side = LEFT)
    rightFrame.pack(side = RIGHT)

    todaysDate = date.today()
    curDay = int(str(date.today())[-2:])            # fetch todays date (DD)

    diff = datetime.timedelta(days = 1)             # calculate next date
    todayStr= dt.now().strftime('%a, %d, %B, %y')
    print("today is ",dt.now().strftime('%a, %d, %B, %y'))

    Message(leftFrame, text = str("today is "+ todayStr), anchor = "ne").pack(side =TOP)

    countdownString = StringVar(leftFrame)
    countdownString.set(countdown())

    if countdownString.get()!='None':
        frontEnd.eventMessage = Message(leftFrame, textvar = countdownString, relief = RAISED)
        frontEnd.eventMessage.pack(side = TOP)
        refresh(countdownString, dt.now())



    lastDay = int(calendar.monthrange(2019, 12)[1])  # get total number of days in month            
    print("days this month,", lastDay)
    remainingDays = abs(lastDay - curDay)
    print("Days remaining this month,", remainingDays)
    allDays = []
    nthDay = 0
    while remainingDays > 0:                        # when days remain, iterate over and create strings of every date
        nthDay = curDay + int(str(diff)[0])
        curDay = nthDay
        allDays.append(str(todaysDate)[0:-2]+ str(curDay))
        remainingDays = remainingDays-1

    print(allDays)
    Message(rightFrame, text = "SELECT DATE-  ").pack(side= TOP)
    frontEnd.dateVar = StringVar(rightFrame)
    frontEnd.dateVar.set(str(todaysDate))
    try:
        frontEnd.inputDay = OptionMenu(rightFrame, frontEnd.dateVar,*allDays)
    except:
        frontEnd.inputDay = OptionMenu(rightFrame, frontEnd.dateVar,todaysDate)

    frontEnd.inputDay.pack(side =TOP)

    def getVal():                                # gfetch input of selected date
        frontEnd.email_text = ""
        for i in Entries:
            frontEnd.email_text += i +" "
        frontEnd.submit.pack_forget()
        createEntry()

    frontEnd.submit = Button(bottomFrame, text = "submit", command = getVal)
    frontEnd.submit.pack(side = BOTTOM)
    plannerWindow.mainloop()


createFile()
frontEnd()
