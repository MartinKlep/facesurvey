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


        print("PupilLeftTotal " + str(avgPupilLeftTotal))
        print("PrePlayPupilLeft " +  str(avgPrePlayPupilLeft))
        print("PreIncidentPupilLeft " +  str(avgPreIncidentPupilLeft))
        print("IncidentPupilLeft " +  str(avgIncidentPupilLeft))
        print("PostIncidentPupilLeft " +  str(avgPostIncidentPupilLeft))

        print(" ")
        print("-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_")
        print(" ")

        print("PupilRightTotal " +  str(avgPupilRightTotal))
        print("PrePlayPupilRight " +  str(avgPrePlayPupilRight))
        print("PreIncidentPupilRight " +  str(avgPreIncidentPupilRight))
        print("IncidentPupilRight " +  str(avgIncidentPupilRight))
        print("PostIncidentPupilRight " +  str(avgPostIncidentPupilRight))

        print(" ")

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

        fig, (ax1, ax2) = plt.subplots(1,2,sharex=True, sharey=True)
        fig.suptitle("Video " + videoID + " Proband Nr. " + userID)
        nbins = 20

        ax1.hist2d(totalGazeX, totalGazeY, bins = nbins, cmap='plasma')
        ax1.set_title("Gesamt| ØX : " + str(avgGazeX) + " / ØY : " + str(avgGazeX) + "")

        ax2.hist2d(incidentX, incidentY, bins = nbins, cmap='plasma')
        ax2.set_title("TOI| ØX : " + str(avgIncidentX) + " / ØY : " + str(avgIncidentY) + "")


        plt.xlim(-0.5, 0.5)
        plt.ylim(-0.5, 0.5)

        fig.savefig(my_path + '/!Szene' + str(videoID) + '/Heat V' + str(videoID) + ' U' + str(userID) + '.png')

        timestamps = np.array(timestamps)


        fig, ax = plt.subplots()


        ax.plot(timestamps, leftPupils)
        ax.plot(timestamps, rightPupils)

        fig.suptitle("Video " + videoID + " Proband Nr. " + userID)
        ax.set(xlabel="Zeit in s", ylabel="Pupillendurchmesser in mm", title="ØGesamt: " + str(avgPupilLeftTotal) + "| ØPre: " + str(avgPrePlayPupilLeft) + "| ØTOI " + str(avgIncidentPupilLeft) + "| ØPost: " + str(avgPostIncidentPupilLeft) + ""  )
        plt.axvline(x=videoPlayStartTime, label='Video Start')
        plt.axvline(x=incidentStartTime,label='Kurz vor Szenario')
        plt.axvline(x=incidentEndTime, label='Nach Szenario')
        ax.grid()

        fig.savefig(my_path + '/!Szene' + str(videoID) + '/Line V' + str(videoID) + ' U' + str(userID) + '.png')



        f.close()
        userCounter+=1
    videoCounter+=1