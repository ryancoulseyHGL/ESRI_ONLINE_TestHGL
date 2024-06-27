import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import datetime
import sys


## Import Data

today = str(datetime.datetime.now())
today = today[:10]
today = sys.argv[1]

read_array = np.genfromtxt(sys.argv[3], delimiter = ',', skip_header=1, dtype=str)
team = sys.argv[2]

DDID = today[:4] + today[5:7] + today[8:10] + '_' + team

## Split data by line


Lines = []
Line = []
i = 0
if read_array[0, 5] == '' or read_array[0, 6] == '':
    Line.append([read_array[i, 0], read_array[i, 1], read_array[i, 2], read_array[i, 3], read_array[i, 4], read_array[i, 5], read_array[i, 6], read_array[i, 9], read_array[i, 10], read_array[i, 16], read_array[i, 12], read_array[i, 13], read_array[i, 14], today[:4] + today[5:7] + today[8:10] + '_' + team, read_array[i, 1][0:4], 'nan'])
else:
    Line.append([read_array[i, 0], read_array[i, 1], read_array[i, 2], read_array[i, 3], read_array[i, 4], read_array[i, 5], read_array[i, 6], read_array[i, 9], read_array[i, 10], read_array[i, 16], read_array[i, 12], read_array[i, 13], read_array[i, 14], today[:4] + today[5:7] + today[8:10] + '_' + team, read_array[i, 1][0:4], datetime.datetime.utcfromtimestamp(((float(read_array[i, 5])*7*86400)+(float(read_array[i, 6]) + 315964800))).strftime('%Y-%m-%d\t%H:%M:%S')])
for i in range(1, len(read_array)):
    #print(datetime.datetime.utcfromtimestamp(((float(read_array[i, 5])*7*86400)+(float(read_array[i, 6]) + 315964800))).strftime('%Y%m%d'), today[:4] + today[5:7] + today[8:10])
      
    #print(read_array[i, 14])
    if read_array[i, 14] != 'GpsContinuousTimePoint':
        continue
    if datetime.datetime.utcfromtimestamp(((float(read_array[i, 5])*7*86400)+(float(read_array[i, 6]) + 315964800))).strftime('%Y%m%d') != today[:4] + today[5:7] + today[8:10]:
        #print(datetime.datetime.utcfromtimestamp(((float(read_array[i, 5])*7*86400)+(float(read_array[i, 6]) + 315964800))).strftime('%Y%m%d'), "\t", today[:4] + today[5:7] + today[8:10])
        continue 
    
    if read_array[i, 1] == read_array[i-1, 1]:
        if read_array[i, 5] == '' or read_array[i, 6] == '':
            Line.append([read_array[i, 0], read_array[i, 1], read_array[i, 2], read_array[i, 3], read_array[i, 4], read_array[i, 5], read_array[i, 6], read_array[i, 9], read_array[i, 10], read_array[i, 16], read_array[i, 12], read_array[i, 13], read_array[i, 14], today[:4] + today[5:7] + today[8:10] + '_' + team, read_array[i, 1][0:4], 'nan'])
        else:
            Line.append([read_array[i, 0], read_array[i, 1], read_array[i, 2], read_array[i, 3], read_array[i, 4], read_array[i, 5], read_array[i, 6], read_array[i, 9], read_array[i, 10], read_array[i, 16], read_array[i, 12], read_array[i, 13], read_array[i, 14], today[:4] + today[5:7] + today[8:10] + '_' + team, read_array[i, 1][0:4], datetime.datetime.utcfromtimestamp(((float(read_array[i, 5])*7*86400)+(float(read_array[i, 6]) + 315964800))).strftime('%Y-%m-%d\t%H:%M:%S')])
    else:
        Lines.append(Line)
        Line = []
Lines.append(Line)


# Calculate velocity and throw out sample 1 for shape errors


for line in Lines:
    for i in range(1, len(line)):
        line[i].append(float(np.sqrt((float(line[i][3]) - float(line[i - 1][3]))**2 + (float(line[i][2]) - float(line[i - 1][2]))**2)))
    try:
        line.pop(0)
    except:
        break


## Find MQO Faliurs and store in arrays



## Change index to match where velocity is
Line_Excedances_45 = []
Line_Excedances_50 = []
for line in Lines:
    Line_45 = []
    Line_50 = []
    if len(line) == 0:
        continue
    #print(line[0][-1])
    for point in line:
        if point[-1] >= 0.45 and point[-1] < 0.50:
            Line_45.append(point)
        if point[-1] >= 0.50:
            Line_50.append(point)

    if len(Line_45)/len(line) > 0.02:
        Line_Excedances_45.append(Line_45)

    Line_Excedances_50.append(Line_50)


# Create velocity Plots


along_line_spacing = []
for line in Lines:
    points = []
    for point in line:
        points.append(point[-1])
    along_line_spacing.append(points)


#line_Count = 0
#for line in along_line_spacing:
#    plt.title("Along line Speed, Transect " + Lines[line_Count][0][1][:5])
#    plt.xlabel("Point along line")
#    plt.ylabel("Speed (m/s)")
#    plt.ylim([0, 1.2])
#    plt.plot(range(len(line)-2), [float(y) for y in line[1:-1]])
#    plt.show()
#    line_Count += 1


# Create XYZ with all data from the day

##Add Calculated Fields



#out_file = input("Enter Name Of Output File: ")
with open(team + "_" + "AllLines_" + today + ".xyz", 'w') as f:
    f.write("//WGS84-Zn12:PointID Code Easting[m] Northing[m] Elevation[m] StartWeek StartSecond SolutionType PDOP V_Precision H_Precision Min_Satelites Method Daily_Data_ID Transect_ID UTC_Date UTC_Time Valid X_Filt Y_Filt Velocity[m/s] Velo_Fail \n")
    line_count = 0
    for line in Lines:
        try:
            f.write("Line " + line[0][1] + '_' + line[0][13] + '\n')
            for point in line:
                for i in range(len(point) - 1):
                    f.write('\t' + str(point[i]))
                f.write('\t' + '\t' + '\t' + '\t' + '\t' + '\t' + '\n') 
        except:
            print("Done")
        line_count += 1

    f.close()


# Create XYZ with revisits


with open(team + "_" + "Raw_Faliurs_" + today + ".xyz", 'w') as f:
    f.write("//WGS84-Zn12:PointID Code Easting[m] Northing[m] Elevation[m] StartWeek StartSecond SolutionType PDOP RMS H_Precision Min_Satelites Method V_Precision Daily_Data_ID Transect_ID UTC_Date UTC_Time Velocity[m/s] \n")
    line_count = 0
    for line in Line_Excedances_50:
        f.write("Line " + str(line_count) + '\n')
        for point in line:
            for i in range(len(point)):
                f.write('\t' + str(point[i]))
            f.write('\n')    
        line_count += 1
    for line in Line_Excedances_45:
        f.write("Line " + str(line_count) + '\n')
        for point in line:
            for i in range(len(point)):
                f.write('\t' + str(point[i]))
            f.write('\n') 
        line_count += 1

    f.close()