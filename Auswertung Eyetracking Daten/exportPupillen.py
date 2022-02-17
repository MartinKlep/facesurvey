import json
import numpy as np
import matplotlib.pyplot as plt
import os
import csv

my_path = os.path.dirname(os.path.abspath(__file__))
header = ['time', 'User 1', 'User 2', 'User 3', 'User 4', 'User 5', 'User 6', 'User 7', 'User 8', 'User 9', 'User 10', 'User 11', 'User 12',]

# cut array for specific region
def cutArray(start, end, arr):
    start = start*90
    end = end*90
    result = arr[start:end]
    return result

incidentStartTimes = [13,15,8,10,15,30]
incidentEndTimes = [17,20,12,18,40,39]
videoEndTimes = [25,29,19,20,55,41]

videoCounter = 1
while videoCounter <= 6:
    csvdata = []
    time = []
    userCounter = 1
    while userCounter <= 12:
        filename ='Study'+ str(videoCounter) + 'Scene_'+ str(userCounter) +'.json'

        videoID = filename[5]
        userID = filename[12] 
        if filename[13] != ".":
            userID += filename[13]

        f = open(filename,)

        # regions of interest timestamps

        videoPlayStartTime = 5
        incidentStartTime = incidentStartTimes[videoCounter-1]
        incidentEndTime = incidentEndTimes[videoCounter-1]
        videoEndTime = videoEndTimes[videoCounter-1]



        data = json.load(f)

        dataLeft = []
        dataRight = []
        for i in data:
            dataLeft.append(i["Left"])
            dataRight.append(i["Left"])

        lp = []
        rp = []
        leftGaze = []
        rightGaze = []
        timestamps = []
        t = 1
        for i in dataLeft:
            tstamp = t/90
            timestamps.append(tstamp)
            t = t+1
            lp.append(i["PupilDiameter"])
            leftPupils = np.array(lp)
            lgazeRay = i["GazeRay"]
            leftGaze.append(lgazeRay["Direction"])

        for i in dataRight:
            rp.append(i["PupilDiameter"])
            rightPupils = np.array(rp)
            rgazeRay = i["GazeRay"]
            rightGaze.append(rgazeRay["Direction"])



        prePlayPupilLeft = cutArray(0, videoPlayStartTime, leftPupils)
        preIncidentPupilLeft = cutArray(videoPlayStartTime, incidentStartTime, leftPupils)
        incidentPupilLeft = cutArray(incidentStartTime, incidentEndTime, leftPupils)
        postIncidentPupilLeft = cutArray(incidentEndTime, videoEndTime, leftPupils)


        prePlayPupilRight = cutArray(0, videoPlayStartTime, rightPupils)
        preIncidentPupilRight = cutArray(videoPlayStartTime, incidentStartTime, rightPupils)
        incidentPupilRight = cutArray(incidentStartTime, incidentEndTime, rightPupils)
        postIncidentPupilRight = cutArray(incidentEndTime, videoEndTime, rightPupils)

        avgPupilLeftTotal = np.mean(leftPupils)
        avgPrePlayPupilLeft = np.mean(prePlayPupilLeft)
        avgPreIncidentPupilLeft = np.mean(preIncidentPupilLeft)
        avgIncidentPupilLeft = np.mean(incidentPupilLeft)
        avgPostIncidentPupilLeft = np.mean(postIncidentPupilLeft)

        avgPupilLeftTotal = round(avgPupilLeftTotal,2)
        avgPrePlayPupilLeft = round(avgPrePlayPupilLeft,2)
        avgIncidentPupilLeft = round(avgIncidentPupilLeft,2)
        avgPostIncidentPupilLeft  = round(avgPostIncidentPupilLeft,2)


        avgPupilRightTotal = np.mean(rightPupils)
        avgPrePlayPupilRight = np.mean(prePlayPupilRight)
        avgPreIncidentPupilRight = np.mean(preIncidentPupilRight)
        avgIncidentPupilRight = np.mean(incidentPupilRight)
        avgPostIncidentPupilRight = np.mean(postIncidentPupilRight)

        f.close()

        csvdata.append(leftPupils)

        if userCounter == 1:
            time = timestamps
        else:
            if len(timestamps) < len(time):
                time = timestamps
    


        userCounter+=1
    

    with open('pupillengraph Video ' + str(videoCounter) + '.csv', 'w', encoding='UTF8',  newline='') as f:
        writer = csv.writer(f, dialect='excel')

        writer.writerow(header)

        writedata = []
        csvindex = 0
        for i in time:
            writedata.append([str(time[csvindex]), csvdata[0][csvindex],csvdata[1][csvindex],csvdata[2][csvindex],csvdata[3][csvindex],csvdata[4][csvindex],csvdata[5][csvindex],csvdata[6][csvindex],csvdata[7][csvindex],csvdata[8][csvindex],csvdata[9][csvindex],csvdata[10][csvindex],csvdata[11][csvindex] ])
            csvindex+=1
        #writer.writerows(writedata)


    avgPupils = []
    avgindex = 0
    low = 9999999999999999999
    lowarray = []
    for i in csvdata:
        if len(i) < low:
            low = len(i)
            lowarray = i

    for i in lowarray:
        sum = csvdata[0][avgindex] + csvdata[1][avgindex] + csvdata[2][avgindex] + csvdata[3][avgindex] + csvdata[4][avgindex] + csvdata[5][avgindex] + csvdata[6][avgindex] + csvdata[7][avgindex] + csvdata[8][avgindex] + csvdata[9][avgindex] + csvdata[10][avgindex] + csvdata[11][avgindex]
        avg = sum/12
        avgPupils.append(avg)
        avgindex+=1
    
    fig, ax = plt.subplots()


    ax.plot(time, avgPupils)

    fig.suptitle("Video " + videoID + "Durchschnittliche Pupillengrößen")
    ax.set(xlabel="Zeit in s", ylabel="Pupillendurchmesser in mm" )
    plt.axvline(x=videoPlayStartTime, label='Video Start')
    plt.axvline(x=incidentStartTime,label='Kurz vor Szenario')
    plt.axvline(x=incidentEndTime, label='Nach Szenario')
    ax.grid()

    fig.savefig(my_path + "AVF Pupillen Video " + str(videoID) + '.png')

    videoCounter+=1