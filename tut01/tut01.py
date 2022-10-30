from itertools import count
import os
import csv
# import pandas as pd
os.system("cls")
from datetime import datetime
start_time = datetime.now()


def fun(mod=5000):
    # main function which will implement the code
    # for changing the mod value, user can change the parameter or
    # can give another parameter in the bottom of the code

    # Opening output file and writing header
    with open('octant_output.csv', "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time', 'U', 'V', 'W', 'U Avg', 'V Avg', 'W Avg', "U'=U - U avg", "V'=V - V avg",
                        "W'=W - W avg", 'Octant', "   ", 'Octant ID', '1', '-1', '2', '-2', '3', '-3', '4', '-4'])

    file.close()
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

    file.close()
    # calcutlating average values
    Uavg = (float)(Usum)/(float)(cnt)
    Vavg = (float)(Vsum)/(float)(cnt)
    Wavg = (float)(Wsum)/(float)(cnt)
    # print(Uavg)
    # print(Vavg)
    # print(Wavg)
    # print(cnt)

    # opening to add remaining values
    f = open('octant_output.csv', "a", newline='')

    # making sure that the mod value is integer
    mod = (int)(mod)

    # tempv = 0

    # initialising cnt2 for counting total counts
    cnt2 = 0
    # making below variables as string for easier printing
    Uavg1 = (str)(Uavg)
    Vavg1 = (str)(Vavg)
    Wavg1 = (str)(Wavg)

    # making a list to store all the octant values
    octantk = []

    # implementing the output
    with open("octant_input.csv", "r", newline="") as file:
        reader = csv.DictReader(file)
        # print(reader)
        for row in reader:
            x = (float)(row['U'])
            y = (float)(row['V'])
            z = (float)(row['W'])

            x -= Uavg
            y -= Vavg
            z -= Wavg
            # determining the octant
            if x > 0 and y > 0 and z >= 0:
                octant1 += 1
                oct = 1
            elif x < 0 and y > 0 and z >= 0:
                octant2 += 1
                oct = 2
            elif x < 0 and y < 0 and z >= 0:
                octant3 += 1
                oct = 3
            elif x > 0 and y < 0 and z >= 0:
                octant4 += 1
                oct = 4
            elif x > 0 and y > 0 and z < 0:
                octantM1 += 1
                oct = -1
            elif x < 0 and y > 0 and z < 0:
                octantM2 += 1
                oct = -2
            elif x < 0 and y < 0 and z < 0:
                octantM3 += 1
                oct = -3
            elif x > 0 and y < 0 and z < 0:
                octantM4 += 1
                oct = -4
            # storing octant in octant list and also keeping count of all the individual octants
            octantk.append(oct)

    file.close()

    cnttemp = 0
    with open("octant_input.csv", "r", newline="") as file:
        reader = csv.DictReader(file)
        # print(reader)
        for row in reader:
            x = (float)(row['U'])
            y = (float)(row['V'])
            z = (float)(row['W'])

            x -= Uavg
            y -= Vavg
            z -= Wavg
            oct = octantk[cnt2]
            tempstr = "Overall Count"
            # tempstr = f"{cnttemp*mod}-{(cnttemp+1)*mod}"
            one = (str)(octantM1)
            two = (str)(octant2)
            three = (str)(octantM2)
            four = (str)(octant3)
            five = (str)(octantM3)
            six = (str)(octant4)
            seven = (str)(octantM4)
            zero = (str)(octant1)
            empt = ""
            # implementing for first row
            if(cnttemp == 1):
                tempstr = "Mod " + (str)(mod)
                empt = "User Input"
                # tempstr = ""
                one = ""
                two = ""
                three = ""
                four = ""
                five = ""
                six = ""
                seven = ""
                zero = ""
            # implementing onwards 2nd row
            elif(cnttemp >= 2):
                ty = min(cnt, (cnttemp-1)*mod)
                if(ty!=cnt):
                    ty-=1
                tempstr = f"{(cnttemp-2)*mod}-{ty}"
                one = (str)(octantk[(cnttemp-2)*(mod)                                    :min((cnttemp+1-2)*(mod)-1, cnt)].count(-1))
                # counting values corresponding to given range
                two = (str)(octantk[(cnttemp-2)*(mod)                                    :min((cnttemp+1-2)*(mod)-1, cnt)].count(2))
                three = (str)(
                    octantk[(cnttemp-2)*(mod):min((cnttemp+1-2)*(mod)-1, cnt)].count(-2))
                four = (str)(octantk[(cnttemp-2)*(mod)                                     :min((cnttemp+1-2)*(mod)-1, cnt)].count(3))
                five = (str)(
                    octantk[(cnttemp-2)*(mod):min((cnttemp+1-2)*(mod)-1, cnt)].count(-3))
                six = (str)(octantk[(cnttemp-2)*(mod)                                    :min((cnttemp+1-2)*(mod)-1, cnt)].count(4))
                seven = (str)(
                    octantk[(cnttemp-2)*(mod):min((cnttemp+1-2)*(mod)-1, cnt)].count(-4))
                zero = (str)(octantk[(cnttemp-2)*(mod)                                     :min((cnttemp+1-2)*(mod)-1, cnt)].count(1))
            cnttemp += 1
            cnt2 += 1
            # after mod value crosses 30000
            if((cnttemp-2)*mod > 30000):
                tempstr = ""
                one = ""
                two = ""
                three = ""
                four = ""
                five = ""
                six = ""
                seven = ""
                zero = ""
            # writing in rows
            fieldnames = ['Time', 'U', 'V', 'W', 'U Avg', 'V Avg', 'W Avg', "U'=U - U avg", "V'=V - V avg",
                          "W'=W - W avg", 'Octant', "   ", 'Octant ID', '1', '-1', '2', '-2', '3', '-3', '4', '-4']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow({'Time': row['Time'], 'U': x, 'V': y, 'W': z,  "U Avg": Uavg1, "V Avg": Vavg1, "W Avg": Wavg1, "U'=U - U avg": x-Uavg, "V'=V - V avg": y-Vavg,
                            "W'=W - W avg": z-Wavg, "Octant": oct, "   ": empt, "Octant ID": tempstr, "1": zero, "-1": one, "2": two, "-2": three, "3": four, "-3": five, "4": six, "-4": seven})
            Uavg1 = ""
            Vavg1 = ""
            Wavg1 = ""
    f.close()
    file.close()
    print("Code succesfully executed with mod value = " + (str)(mod))


# Calling the function with predefined value
fun()
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
