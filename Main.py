import cv2
import numpy as np
import time

from Decryptor import decrypt

cap = cv2.VideoCapture(0)
text = ''
check = 0
start = 0
end = 0
decryptedText = 'Output:'

while True:
    _, frame = cap.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # test color
    low_white = np.array([255, 255, 255])
    high_white = np.array([255, 255, 255])
    mask = cv2.inRange(img, low_white, high_white)

    pixelCount = cv2.countNonZero(mask)

    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (20, 30)
    fontScale = 1
    fontColor = (209, 80, 0)
    lineType = 2
    dif = end - start

    cv2.putText(mask, f'Count: {pixelCount}', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
    cv2.putText(mask, text, (20, 60), font, fontScale, fontColor, lineType)
    # cv2.putText(mask, f'Time: {dif}', (20, 120), font, fontScale, fontColor, lineType)
    # cv2.putText(mask, f'Check: {check}', (20, 150), font, fontScale, fontColor, lineType)
    cv2.putText(mask, decryptedText, (20, 90), font, fontScale, fontColor, lineType)

    if pixelCount > 6000:
        # cv2.putText(mask, 'Light on', (20, 60), font, fontScale, fontColor, lineType)

        if check == 0:
            start = time.time()
            check = 1

        if check == 2:
            if dif < 0.6:
                check = 0
            elif dif < 1.6:
                text += ' '
                check = 0
            elif dif < 3:
                text += '  '
                check = 0

            start = time.time()

        end = time.time()

    else:
        # cv2.putText(mask, 'Light off', (20, 60), font, fontScale, fontColor, lineType)

        if check == 1:
            if dif > 0.7:
                text += '-'
            else:
                if dif > 0.3:
                    text += '.'
            start = time.time()
            check = 2

        if check == 2:
            end = time.time()

    cv2.imshow("White ", mask)
    # cv2.imshow("White frame", img)

    key = cv2.waitKey(1)
    if key == 32:
        decryptedText += decrypt(text)

    if key == 27:
        break
