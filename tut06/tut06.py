from calendar import week
import datetime
from re import A
from time import strftime
import pandas as pd
import os
import csv

def RollSplit(att):
    roll = ""
    for i in range(0,8):
        roll+=att[i]
    return roll

def NameSplit(att):
    name = ""
    for i in range(9,len(att)):
        name+=att[i]
    return name

def MonOrThurs(weekday):
    
    if (weekday == "Monday"):
        return True
    
    if (weekday == "Thursday"):
        return True
    
    return False

def bet2n3(timeMarked):
    if(timeMarked[0]=='1' and timeMarked[1]=='4'):
        return True
    if(timeMarked=="15:00:00"):
        return True
    return False

def splitDate(timestr):
    finstr = ""
    for i in range(0,10):
        finstr+=timestr[i]
    
    return finstr

def splitTime(timestr):
    finstr = ""
    for i in range(11,len(timestr)):
        finstr+=timestr[i]
    
    return finstr


def checkDate(timestr, alldates):
    Date = splitDate(timestr)
    TimeMarked = splitTime(timestr)
    # length = len(timestr)
    # for i in range(0,10):
    #     Date+=timestr[i]
    # for i in range(11, length):
    #     TimeMarked+=(str)(timestr[i])
    
    day, month, year = (int(x) for x in Date.split('/'))
    ans = datetime.date(year, month, day)
    print(ans.strftime("%A"))
    # alldates = set(alldates)
    weekday = str(ans.strftime("%A"))
    if (MonOrThurs(weekday)):
        alldates.append(Date)
        return True
        # if(bet2n3(TimeMarked)): 
            # print("ok")
    # print(TimeMarked)
    # print(Date)
    return False    


registered = pd.read_csv('input_registered_students.csv')
# registered.reset_index()
students = []

for i in range(len(registered)):
    # print(registered.iloc[i, 0], registered.iloc[i, 1])
    strin = (str)(registered.iloc[i,0]) + " " + (str)(registered.iloc[i,1])
    students.append(strin)
    

# print(students)
fieldnames = ["Roll","Name","total_lecture_taken","attendance_count_actual","attendance_count_fake","attendance_count_absent","Percentage (attendance_count_actual/total_lecture_taken) 2 digit decimal" ]

att_sheet = pd.read_csv('input_attendance.csv')

times = []
for i in range(len(att_sheet)):
    times.append((str)(att_sheet.iloc[i,0]))
    
diffDates = []
for time in times:
    # print(time)
    checkDate(time, diffDates)

diffDates = set(diffDates)
# print(diffDates)
totalLectures = len(diffDates)
# print(totalLectures)
# print(times)

templist = []

os.makedirs('Outputtemp', exist_ok=True)
fprime = open("Outputtemp/attendance_report_consolidated.csv", "w", newline='')
fdupli = open("Outputtemp/attendance_report_duplicate.csv", "w", newline='')
writerprime= csv.writer(fprime)
writerprime.writerow(fieldnames)
duplifield = ["Timestamp","Roll","Name","Total count of attendance on that day"]
writerdupli = csv.writer(fdupli)
writerdupli.writerow(duplifield)
for student in students:
    # print(student)ṇ
    indivatt = att_sheet[att_sheet['Attendance']==student]
    
    tot_marked = (len(indivatt))
    fake_marked = 0
    dupli_marked = 0
    dicttemp = {}
    name = NameSplit(student)
    roll = RollSplit(student)
    # print(indivatt)
    for i in range(len(indivatt)):
        timestr = (str)(indivatt.iloc[i,0])
        datetemp = splitDate(timestr)
        timetemp = splitTime(timestr)
        sztemp = len(dicttemp)
        # print(timetemp)
        if (bet2n3(timetemp)==False):
            fake_marked+=1
        elif(checkDate(timestr, templist) == False):
            fake_marked+=1
        else:
            if(datetemp in dicttemp):
                dicttemp[datetemp]+=1
            else:
                dicttemp[datetemp]=1
            if(len(dicttemp)==sztemp):
                dupli_marked+=1
                writerdupli = csv.DictWriter(fdupli, fieldnames=duplifield)
                writerdupli.writerow({'Timestamp':timetemp, 'Roll':roll,'Name':name,'Total count of attendance on that day':dupli_marked})

                
    # print(tot_marked, fake_marked, dupli_marked)
    actual = tot_marked-fake_marked-dupli_marked
    fake = fake_marked+dupli_marked
    percentage = (actual*100)/totalLectures
    percentage = str(round(percentage, 2))
    filename = "Outputtemp/" + (str)(roll) +".csv"
    f = open(filename, "w", newline='')
    writer = csv.writer(f)
    writer.writerow(fieldnames)
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writerow({'Roll':roll, 'Name':name, 'total_lecture_taken':totalLectures, 'attendance_count_actual':actual, 'attendance_count_fake':fake, 'attendance_count_absent':totalLectures-actual, 'Percentage (attendance_count_actual/total_lecture_taken) 2 digit decimal':percentage})
    writerprime2 = csv.DictWriter(fprime, fieldnames=fieldnames)
    writerprime2.writerow({'Roll':roll, 'Name':name, 'total_lecture_taken':totalLectures, 'attendance_count_actual':actual, 'attendance_count_fake':fake, 'attendance_count_absent':totalLectures-actual, 'Percentage (attendance_count_actual/total_lecture_taken) 2 digit decimal':percentage})
    