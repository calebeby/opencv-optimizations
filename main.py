import cv2
import math
import numpy as np
import timeit

# Before: 0.206 usec per loop
# After:        usec per loop

class LiftFinder:
    HEIGHT = 480
    WIDTH = 640
    lower = np.array([70, 230, 40])
    upper = np.array([90, 255, 255])

    def __init__(self):
        self.img = np.empty(shape=(self.HEIGHT, self.WIDTH, 3), dtype=np.uint8)
        self.hsv = np.empty(shape=(self.HEIGHT, self.WIDTH, 3), dtype=np.uint8)
        self.filtered = np.empty(shape=(self.HEIGHT, self.WIDTH, 1), dtype=np.uint8)
        self.blurred = np.empty(shape=(self.HEIGHT, self.WIDTH, 1), dtype=np.uint8)

    def get_img(self):
        return cv2.imread('test.jpg')

    def send_img(self):
        cv2.imwrite('output.jpg', self.img)

    def process_image(self, img):
        self.img = img
        cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV, dst=self.hsv)

        cv2.inRange(self.hsv, self.lower, self.upper, dst=self.filtered)
        cv2.GaussianBlur(self.filtered, (7, 7), 0, dst=self.blurred)

        _, all_contours, _ = cv2.findContours(
            self.blurred, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # draw all contours in purple
        for c in all_contours:
            cv2.drawContours(img, [c], -1, (255, 0, 255), 2)

        x = []
        y = []

        def find_center(contour):
            M = cv2.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            return cX, cY

        # find two largest contours by area
        contour_areas = np.array(list(map(cv2.contourArea, all_contours)))
        contours = [all_contours[i] for i in np.argsort(contour_areas)[-2:]]

        # find center of each contour
        for c in contours:
            cX, cY = find_center(c)
            x.append(cX)
            y.append(cY)

            cv2.drawContours(self.img, [c], -1, (0, 0, 255), 2)

        goal_x = int(np.mean(x))
        goal_y = int(np.mean(y))
        cv2.circle(self.img, (goal_x, goal_y), 5, (0, 0, 255), -1)

lift_finder = LiftFinder()

def main():
    print('hiya')
    img = lift_finder.get_img()
    for i in range(0, 500):
        print(i)
        lift_finder.process_image(img)
    lift_finder.send_img()

t = timeit.Timer(main)

try:
    print(t.timeit(number=1))
except:
    t.print_exc()

# unoptimized: 7.1s
