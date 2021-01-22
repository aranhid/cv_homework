import numpy as np
from skimage.measure import label, regionprops
import skimage.filters as filters 
import matplotlib.pyplot as plt
import cv2
import mss
import pyautogui

def click(button):
    pyautogui.keyDown(button)

cv2.namedWindow("window", cv2.WINDOW_KEEPRATIO)

with mss.mss() as scr:           
    monitor = scr.monitors[1]
    monitor = {"top": 250, "left": 20, "width": 750, "height": 200}

    while(True):
        img = np.array(scr.grab(monitor))
        cv2.imshow("window", img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        roi = img[130:230, 80:150]
        roi = roi < filters.threshold_isodata(roi)
        # cv2.imshow("roi", roi)
        labeled = label(roi)
        # plt.imshow(labeled)
        # plt.show()
        for region in regionprops(labeled):
            # plt.imshow(region.image)
            # plt.show()
            # print(region.area)
            # print(region.eccentricity)
            if (region.area > 200 and 0.9 < region.eccentricity):
                print("OK", region.area)
                print("OK", region.eccentricity)
                click('space')
                # plt.imshow(region.image)
                # plt.show()
                # cv2.imshow("labeled", region.image)
        if cv2.waitKey(1) == ord('q'):
            break

cv2.destroyAllWindows()