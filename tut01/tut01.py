import os
import csv
os.system("cls")


# Opening output file and writing header
with open('octant_output.csv', "w", ) as file:
    writer = csv.writer(file)
    writer.writerow(['Time', 'U', 'V', 'W', 'U Avg', 'V Avg', 'W Avg', "U'=U - U avg", "V'=V - V avg", "W'=W - W avg",'Octant', "   ", 'Octant ID', '1', '-1', '2', '-2', '3', '-3', '4', '-4'])

    
# initializing variables
cnt = 0
octant1 = octant2 = octant3 = octant4 = 0
octantM1 = octantM2 = octantM3 = octantM4 = 0
Usum = Vsum = Wsum = 0

# adding all values to get sum
with open("octant_input.csv", "r") as file:
    reader = csv.DictReader(file)
    print(reader)
    for row in reader:
        cnt = cnt+1
        x = (float)(row['U'])
        y = (float)(row['V'])
        z = (float)(row['W'])
        Usum += x
        Vsum += y
        Wsum += z

Uavg = (float)(Usum)/(float)(cnt)
Vavg = (float)(Vsum)/(float)(cnt)
Wavg = (float)(Wsum)/(float)(cnt)
print(Uavg)
print(Vavg)
print(Wavg)
print(cnt)

f = open("octant_output.csv", "a")
# fieldnames = ['U Avg', 'V Avg', 'W Avg']
# writer = csv.DictWriter(f, fieldnames=fieldnames)
# writer.writerow({'U Avg': Uavg, 'V Avg': Vavg, 'W Avg': Wavg})

mod = input("Enter mod value: ")
# print(mod)
mod = (int)(mod)

list = []

tempv = 0
cnt2 = 0


temp = [0, 0, 0, 0, 0, 0, 0, 0]

Uavg1 = (str)(Uavg)
Vavg1 = (str)(Vavg)
Wavg1 = (str)(Wavg)


with open("octant_input.csv", "r") as file:
    reader = csv.DictReader(file)
    # print(reader)
    for row in reader:
        x = (float)(row['U'])
        y = (float)(row['V'])
        z = (float)(row['W'])
        
        fieldnames = ['Time', 'U', 'V', 'W', 'U Avg', 'V Avg', 'W Avg', "U'=U - U avg", "V'=V - V avg", "W'=W - W avg",'Octant', "   ", 'Octant ID', '1', '-1', '2', '-2', '3', '-3', '4', '-4']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow({'Time': row['Time'], 'U': x, 'V': y, 'W': z, "U'=U - U avg": x-Uavg, "V'=V - V avg": y-Vavg, "W'=W - W avg": z-Wavg, "U Avg": Uavg1, "V Avg": Vavg1,"W Avg": Wavg1})
        Uavg1 = ""
        Vavg1 = ""
        Wavg1 = ""
        x -= Uavg
        y -= Vavg
        z -= Wavg
        if x > 0 and y > 0 and z >= 0:
            temp[0] = temp[0] + 1
            octant1 = octant1+1
        elif x < 0 and y > 0 and z >= 0:
            temp[2] = temp[2] + 1
            octant2 = octant2+1
        elif x < 0 and y < 0 and z >= 0:
            temp[4] = temp[4] + 1
            octant3 = octant3+1
        elif x > 0 and y < 0 and z >= 0:
            temp[6] = temp[6] + 1
            octant4 = octant4+1
        elif x > 0 and y > 0 and z < 0:
            temp[1] = temp[1] + 1
            octantM1 = octantM1+1
        elif x < 0 and y > 0 and z < 0:
            temp[3] = temp[3] + 1
            octantM2 = octantM2+1
        elif x < 0 and y < 0 and z < 0:
            temp[5] = temp[5] + 1
            octantM3 = octantM3+1
        elif x > 0 and y < 0 and z < 0:
            temp[7] = temp[7] + 1
            octantM4 = octantM4+1
        # print(cnt)
        cnt2 = cnt2+1
        if (cnt2 == mod):
            # print(1)
            cnt2=0
            # print(temp)
            list.append(temp)
            temp = [0, 0, 0, 0, 0, 0, 0, 0]
            if x > 0 and y > 0 and z >= 0:
                temp[0] = temp[0] + 1
            # octant1 = octant1+1
            elif x < 0 and y > 0 and z >= 0:
                temp[2] = temp[2] + 1
            # octant2 = octant2+1
            elif x < 0 and y < 0 and z >= 0:
                temp[4] = temp[4] + 1
                # octant3 = octant3+1
            elif x > 0 and y < 0 and z >= 0:
                temp[6] = temp[6] + 1
                # octant4 = octant4+1
            elif x > 0 and y > 0 and z < 0:
                temp[1] = temp[1] + 1
                # octantM1 = octantM1+1
            elif x < 0 and y > 0 and z < 0:
                temp[3] = temp[3] + 1
                # octantM2 = octantM2+1
            elif x < 0 and y < 0 and z < 0:
                temp[5] = temp[5] + 1
                # octantM3 = octantM3+1
            elif x > 0 and y < 0 and z < 0:
                temp[7] = temp[7] + 1
            # octantM4 = octantM4+1
if(temp!=[0, 0, 0, 0, 0, 0, 0, 0]):
    list.append(temp)
print(list)
    
# print(temp)
# print(cnt2)
# print(octant1)
# print(octantM1)
# print(octant2)
# print(octantM2)
# print(octant3)
# print(octantM3)
# print(octant4)
# print(octantM4)
# print(list)
