import cv2
# import mediapipe as mp
import time
import numpy as np
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume



##############################
# wCam, hCam = 720, 720
##############################




cap = cv2.VideoCapture(0)
# # cap.set(3, wCam)
# # cap.set(4, hCam)





# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)







pTime = 0



detector = htm.handDetector(detectionConfidence=0.8)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(-20.0, None)
minVol = volRange[0]
maxVol = volRange[1]

vol = volume.GetMasterVolumeLevel()
volBar = np.interp(vol, [-37.0, 0], [400, 150])
# volPer = np.interp(vol, [-37.0, 0], [0, 100])
# vol = 0
# volBar = 400

while True:
    success, img = cap.read()

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[4])
        # print(lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        x3, y3 = lmList[12][1], lmList[12][2]
        x4, y4 = lmList[16][1], lmList[16][2]
        x5, y5 = lmList[20][1], lmList[20][2]

        cx, cy = (x1+x2)//2, (y1+y2)//2
        # cx2, cy2 = (x2+x3)//2, (y2+y3)//2


        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2),(255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        # print(length)

        length2 = math.hypot(x3-x2, y3-y2)
        # print(length2)

        if length2 > 65:


            if length < 35:
                cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
            elif length > 200:
                cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)

            # Hand range 35 - 200
            # Volume range -37 - 0

            vol = np.interp(length, [35, 200], [minVol, maxVol])
            volBar = np.interp(length, [35, 200], [400, 150])
            # volBar = np.interp(vol, [-37.0, 0], [400, 150])
            # volPer = np.interp(vol, [-37.0, 0], [0, 100])

            # print(vol)
            volume.SetMasterVolumeLevel(vol, None)

    
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    # vol = np.interp(vol, [-37, 0], [400, 150])
    cv2.rectangle(img, (53, int(volBar)), (82, 400), (255, 0, 255), cv2.FILLED)
    # cv2.putText(img, str(int(volPer)), (40,70), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)

        





    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # cv2.putText(img, str(int(fps)), (40,90), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)
    string = f'fps {int(fps)}'
    cv2.putText(img, string, (40,90), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)


    cv2.imshow("Img", img)
    cv2.waitKey(1)






