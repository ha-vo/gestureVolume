import math

import cv2
import mediapipe
import numpy as np

import HandTracking
import time
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

detectHand = HandTracking()
cap = cv2.VideoCapture(0)
ptime = 0
cTime = 0

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
vol = volume.GetVolumeRange()
minVol = vol[0]
maxVol = vol[1]

while True:
    success, img = cap.read()
    img = detectHand.findHands(img)
    positionHand = detectHand.findPosition(img)

    # position of thump tip
    x1,y1 = positionHand[4][1], positionHand[4][2]

    #postion of pointer tip
    x2, y2 = positionHand[8][1], positionHand[8][2]

    #distance between thump tip and pointer tip
    distance = math.hypot(x2-x1,y2-y1)

    # from distance between 2 finger to volumn
    vol = np.interp(distance,[50,300], [minVol,maxVol])
    volume.SetMasterVolumeLevel(-vol, None)

    cTime = time.time()
    fps = 1 / (cTime - ptime)
    ptime = time.time()

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)

