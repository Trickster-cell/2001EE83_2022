import os
# from tokenize import Number
from openpyxl import Workbook
from openpyxl import load_workbook

Mod = 5000


def decide_octant(u, v, w):
    if(u > 0 and v > 0 and w > 0):
        return "+1"
    elif(u > 0 and v > 0 and w < 0):
        return "-1"
    elif(u < 0 and v < 0 and w > 0):
        return "+3"
    elif(u < 0 and v < 0 and w < 0):
        return "-3"
    elif(u < 0 and v > 0 and w > 0):
        return "+2"
    elif(u < 0 and v > 0 and w < 0):
        return "-2"
    elif(u > 0 and v < 0 and w > 0):
        return "+4"
    elif(u > 0 and v < 0 and w < 0):
        return "-4"


wb = load_workbook(r"input_octant_transition_identify.xlsx")

sheet = wb.active

cnt = 0
octant1 = octant2 = octant3 = octant4 = 0
octantM1 = octantM2 = octantM3 = octantM4 = 0
arr = [0.0, 0.0, 0.0]
# arr.append((float)(0.0))

headings = ["U Avg", "V Avg", "W Avg", "U'=U - U avg", "V'=V - V avg",
            "W'=W - W avg", "Octant", " ", " ", "+1", "-1", "+2", "-2", "+3", "-3", "+4", "-4"]

modstr = "Mod " + (str)(Mod)

row_count = sheet.max_row
column_count = sheet.max_column
print(row_count, column_count)


for col in range(5, 5+len(headings)):
    sheet.cell(row=1, column=col).value = headings[col-5]


# exit(0)
for i in range(2, row_count + 1):
    for j in range(2, column_count + 1):
        data = sheet.cell(row=i, column=j).value
        # print(data, end='   ')
        # print(type(data))
        x = float(data)
        arr[j-2] += x
    # print('\n')
for i in range(3):
    arr[i] /= row_count-1
print(arr)
for i in range(5, 8):
    sheet.cell(row=2, column=i).value = arr[i-5]
for i in range(2, row_count+1):
    for j in range(8, 11):
        sheet.cell(row=i, column=j).value = sheet.cell(
            row=i, column=j-6).value - arr[j-8]


dict = {"+1": 0, "-1": 0, "+2": 0, "-2": 0, "+3": 0, "-3": 0, "+4": 0, "-4": 0}
keys = ["+1", "-1", "+2", "-2", "+3", "-3", "+4", "-4"]


for i in range(2, row_count+1):
    u = sheet.cell(row=i, column=8).value
    v = sheet.cell(row=i, column=9).value
    w = sheet.cell(row=i, column=10).value
    sheet.cell(row=i, column=11).value = (str)(decide_octant(u, v, w))
    dict[decide_octant(u, v, w)] += 1

sheet.cell(row=2, column=13).value = "Overall Count"
sheet.cell(row=3, column=12).value = "User Input"
sheet.cell(row=3, column=13).value = modstr


for i in range(14, 22):
    sheet.cell(row=2, column=i).value = dict[keys[i-14]]


modcnt = row_count//Mod
modcnt += 1
if row_count % Mod == 0:
    modcnt -= 1
print(modcnt)


dict2 = {"+1": 0, "-1": 1, "+2": 2, "-2": 3,
         "+3": 4, "-3": 5, "+4": 6, "-4": 7}


arr2 = [0]*8
finarr = []
# finarr.append(arr2)
for i in range(modcnt):
    finarr.append(arr2.copy())

ind = 0
cnt = 1
for i in range(2, row_count+1):
    oct = sheet.cell(row=i, column=11).value
    j = dict2[oct]
    finarr[ind][j] += 1
    cnt += 1
    if cnt == Mod:
        ind += 1
        cnt = 0

lv = 0
hv = Mod

for i in range(4, 4+modcnt):
    sheet.cell(row=i, column=13).value = str(lv) + " - " + str(hv)
    lv = hv+1
    hv += Mod
    hv = min(hv, row_count)

for i in range(4, 4+modcnt):
    for j in range(14, 22):
        sheet.cell(row=i, column=j).value = finarr[i-4][j-14]

sheet.cell(row=4+modcnt, column=13).value = "Verified"
for i in range(14, 22):
    sheet.cell(row=4+modcnt, column=i).value = 0
    for j in range(4, 4+modcnt):
        sheet.cell(
            row=4+modcnt, column=i).value += sheet.cell(row=j, column=i).value

lastval = 4+modcnt

lastval += 3
sheet.cell(row=lastval, column=13).value = "Overall Transition Count"
sheet.cell(row=lastval+1, column=14).value = "To"
sheet.cell(row=lastval+3, column=12).value = "From"
sheet.cell(row=lastval+1, column=13).value = "Count"

for i in range(8):
    sheet.cell(row=lastval+1, column=14+i).value = keys[i]
for i in range(8):
    sheet.cell(row=lastval+2+i, column=13).value = keys[i]

lv = 0
hv = Mod

for i in range(modcnt):
    lastval+=11
    sheet.cell(row=lastval+1, column=13).value = str(lv)+" - "+str(hv)
    sheet.cell(row=lastval, column=13).value = "Mod Transition Count"
    sheet.cell(row=lastval+1, column=14).value = "To"
    sheet.cell(row=lastval+3, column=12).value = "From"
    lv = hv+1
    hv += Mod
    hv = min(hv, row_count)

    for i in range(8):
        sheet.cell(row=lastval+1, column=14+i).value = keys[i]
    for i in range(8):
        sheet.cell(row=lastval+2+i, column=13).value = keys[i]

print(finarr)

# print(dict)

wb.save("output_octant_transition_identify.xlsx")
