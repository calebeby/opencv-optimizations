import cv2
import math
import numpy as np
import timeit

# Before: 0.206 usec per loop
# After:        usec per loop

class LiftFinder:
    HEIGHT = 240
    WIDTH = 320
    img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)

    def __init__(self):
        pass

    def get_img(self):
        return cv2.imread('test.jpg')

    def send_img(self):
        cv2.imwrite('output.jpg', self.img)

    def process_image(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower = np.array([70, 230, 40])
        upper = np.array([90, 255, 255])

        filtered = cv2.inRange(hsv, lower, upper)
        blurred = cv2.GaussianBlur(filtered, (7, 7), 0)

        output = blurred

        im2, orig_contours, hierarchy = cv2.findContours(
            output, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # loop over the contours
        for c in orig_contours:
            cv2.drawContours(img, [c], -1, (255, 0, 255), 2)

        x = []
        y = []

        def find_center(contour):
            M = cv2.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            return cX, cY

        # find two largest contours by area
        contour_areas = np.array(list(map(cv2.contourArea, orig_contours)))
        contours = [orig_contours[i] for i in np.argsort(contour_areas)[-2:]]

        # find center of each contour
        for c in contours:
            cX, cY = find_center(c)
            x.append(cX)
            y.append(cY)

            cv2.drawContours(img, [c], -1, (0, 0, 255), 2)

        goal_x = int(np.mean(x))
        goal_y = int(np.mean(y))
        cv2.circle(self.img, (goal_x, goal_y), 5, (0, 0, 255), -1)

        self.img = img

lift_finder = LiftFinder()

def main():
    print('hiya')
    img = lift_finder.get_img()
    for i in range(0, 10000):
        print(i)
        lift_finder.process_image(img)

    lift_finder.send_img()

t = timeit.Timer(main)

try:
    print(t.timeit(number=1))
except:
    t.print_exc()

# unoptimized: 7.1s
