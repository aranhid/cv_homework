import cv2
import numpy as np
import random

def find_ball(blurred, lower, upper):
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts, _ = cv2.findContours(
        mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    ball_coords = 0

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        (curr_X, curr_y), radii = cv2.minEnclosingCircle(c)
        if radii > 25:
            cv2.circle(frame, (int(curr_X), int(curr_y)),
                       int(radii), (0, 255, 255), 2)
            ball_coords = int(curr_X)

    return ball_coords
    
cam = cv2.VideoCapture(0)
cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)

masks = {
    "RED": np.array(([2, 0, 0], [4, 255, 255])),
    "GREEN": np.array(([54, 0, 0], [64, 255, 255])),
    #"BLUE": np.array(([98, 0, 0], [100, 255, 255])),
    "YELLOW": np.array(([23, 0, 0], [23, 255, 255])),
}

colors = ["RED", "YELLOW", "GREEN"]
random.shuffle(colors)

while cam.isOpened():
    ret, frame = cam.read()
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)

    queue = {}
    for colorname, mask in masks.items():
        ball = find_ball(blurred, mask[0], mask[1])
        if ball:
            queue[colorname] = ball

    answers = []
    for key in sorted(queue, key=lambda x: queue[x]):
        answers.append(key)

    if (colors == answers):
        cv2.putText(frame, f"True", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 127))
    else:
        cv2.putText(frame, f"Flase", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 127))

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

    cv2.imshow("Camera", frame)

cam.release()
cv2.destroyAllWindows()
