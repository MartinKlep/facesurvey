import json
import numpy as np
import matplotlib.pyplot as plt
import os

my_path = os.path.dirname(os.path.abspath(__file__))

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
    overallGazeX = []
    overallGazeY = []
    toiGazeX = []
    toiGazeY = []
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

        leftGaze = []
        rightGaze = []
        for i in dataLeft:
            lgazeRay = i["GazeRay"]
            leftGaze.append(lgazeRay["Direction"])

        for i in dataRight:
            rgazeRay = i["GazeRay"]
            rightGaze.append(rgazeRay["Direction"])

        leftGazeX = []
        leftGazeY = []
        for i in leftGaze:
            leftGazeX.append(i["x"])
            leftGazeY.append(i["y"])

        rightGazeX = []
        rightGazeY = []
        for i in rightGaze:
            rightGazeX.append(i["x"])
            rightGazeY.append(i["y"])


        totalGazeX = leftGazeX
        for i in rightGazeX:
            totalGazeX.append(i)

        totalGazeY = leftGazeY
        for i in rightGazeY:
            totalGazeY.append(i)

        prePlayLeftX = cutArray(0, videoPlayStartTime, leftGazeX)
        preIncidentLeftX = cutArray(videoPlayStartTime, incidentStartTime, leftGazeX)
        incidentLeftX = cutArray(incidentStartTime, incidentEndTime, leftGazeX)
        postIncidentLeftX = cutArray(incidentEndTime, videoEndTime, leftGazeX)

        prePlayLeftY = cutArray(0, videoPlayStartTime, leftGazeY)
        preIncidentLeftY = cutArray(videoPlayStartTime, incidentStartTime, leftGazeY)
        incidentLeftY = cutArray(incidentStartTime, incidentEndTime, leftGazeY)
        postIncidentLeftY = cutArray(incidentEndTime, videoEndTime, leftGazeY)

        prePlayRightX = cutArray(0, videoPlayStartTime, rightGazeX)
        preIncidentRightX = cutArray(videoPlayStartTime, incidentStartTime, rightGazeX)
        incidentRightX = cutArray(incidentStartTime, incidentEndTime, rightGazeX)
        postIncidentRightX = cutArray(incidentEndTime, videoEndTime, rightGazeX)

        prePlayRightY = cutArray(0, videoPlayStartTime, rightGazeY)
        preIncidentRightY = cutArray(videoPlayStartTime, incidentStartTime, rightGazeY)
        incidentRightY = cutArray(incidentStartTime, incidentEndTime, rightGazeY)
        postIncidentRightY = cutArray(incidentEndTime, videoEndTime, rightGazeY)

        prePlayX = prePlayLeftX 
        for i in prePlayRightX:
            prePlayX.append(i)

        prePlayY = prePlayLeftY
        for i in prePlayRightY:
            prePlayY.append(i)

        preIncidentX = preIncidentLeftX 
        for i in preIncidentRightX:
            preIncidentX.append(i)

        preIncidentY = preIncidentLeftY 
        for i in preIncidentRightY:
            preIncidentY.append(i)

        incidentX = incidentLeftX
        for i in incidentRightX:
            incidentX.append(i)

        incidentY = incidentLeftY
        for i in incidentRightY:
            incidentY.append(i)

        postIncidentX = postIncidentLeftX 
        for i in postIncidentRightX:
            postIncidentX.append(i)

        postIncidentY = postIncidentLeftY
        for i in postIncidentRightY:
            postIncidentY.append(i)

        avgGazeX = round(np.mean(totalGazeX),2)
        avgGazeY = round(np.mean(totalGazeY),2)
        avgIncidentX = round(np.mean(incidentX),2)
        avgIncidentY = round(np.mean(incidentY),2)

        for i in totalGazeX:
            overallGazeX.append(i)
        
        for i in totalGazeY:
            overallGazeY.append(i)

        for i in incidentX:
            toiGazeX.append(i)

        for i in incidentY:
            toiGazeY.append(i)

       
        f.close()
        userCounter+=1


    fig, (ax1, ax2) = plt.subplots(1,2,sharex=True, sharey=True)
    fig.suptitle("Video " + videoID )
    nbins = 20

    ax1.hist2d(overallGazeX, overallGazeY, bins = nbins, cmap='plasma')
    ax1.set_title("Gesamt Gaze")

    ax2.hist2d(toiGazeX, toiGazeY, bins = nbins, cmap='plasma')
    ax2.set_title("TOI Gaze")


    plt.xlim(-0.5, 0.5)
    plt.ylim(-0.5, 0.5)

    fig.savefig(my_path + '/Overall' + '/Heat V' + str(videoID) + '.png')
    videoCounter+=1




