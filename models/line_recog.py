import cv2
import numpy as np
import math


# TODO do some dope annotations
# TODO rename bad variable names(repetitive in CubeRecog3.py
# This code is made to detect lines of a specific color and return their angels

# check if a specific pixel is considered to be red
def is_red(red, blue, green):
    green_high = red - 100
    blue_high = red - 100

    green_in_param = 0 <= green <= green_high
    blue_in_param = 0 <= blue <= blue_high

    return green_in_param and blue_in_param


# calculates the distance of two points
def distance(point1, point2):
    xsqr = (point2[0] - point1[0]) ** 2
    ysqr = (point2[1] - point1[1]) ** 2
    return int(math.sqrt(xsqr + ysqr))


# finds the slope and the degrees of a line
def contour_slope_degrees(contour, image, x, y):
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)

    print("CHECKPOINT1")
    # find box of contours and assign them values
    point_lr = box[0]
    point_ul = box[2]
    point_ur = box[3]

    line1 = distance(point_lr, point_ur)
    line2 = distance(point_ur, point_ul)

    # determine width and height
    if line1 < line2:
        point_lr = box[1]
        point_ur = box[0]

    delta_y = point_lr[1] - point_ur[1]
    delta_x = point_lr[0] - point_ur[0]

    # Calculate angle of line
    if delta_x == 0:
        # Vertical line
        slope = None
        degrees = 90
    else:
        # Non-vertical line
        slope = (delta_y / delta_x) * -1
        radians = math.atan(slope)
        degrees = int(math.degrees(radians))

    # putting all info on image
    cv2.circle(image, (point_lr[0], point_lr[1]), 7, (0, 255, 0), -1)
    cv2.circle(image, (point_ur[0], point_ur[1]), 7, (0, 255, 0), -1)

    cv2.putText(image, "slope is: " + str(slope), (x - 25, y-75),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.putText(image, "degree is: " + str(degrees), (x - 25, y - 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.line(image, (point_lr[0], point_lr[1]), (point_ur[0], point_ur[1]), (0, 255, 0), thickness=2)
    return slope, degrees


# Actual thing that does stuff
def find_line(name):
    print(name)

    img = cv2.imread(name)
    img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)

    # split the image into numpy array?
    height, width, channels = img.shape
    blue_list, green_list, red_list = cv2.split(img)

    print("height: " + str(height))
    print("width: " + str(width))

    # loop through craps and calls on the function is_red()
    for z in range(width):
        for i in range(height):

            red = red_list[i][z]
            blue = blue_list[i][z]
            green = green_list[i][z]

            if not is_red(red, blue, green):
                green_list[i][z] = 0
                blue_list[i][z] = 0
                red_list[i][z] = 0

    # pImage will be the processed image
    pImage = cv2.merge((blue_list, green_list, red_list))

    # find mask of the black stuff
    lower = np.array([1, 1, 1], dtype="uint8")
    upper = np.array([255, 255, 255], dtype="uint8")

    mask = cv2.inRange(pImage, lower, upper)

    # get contour and craps
    try:
        im2, contour, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnt = max(contour, key=cv2.contourArea)

        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        if is_red(red_list[cY][cX], blue_list[cY][cX], green_list[cY][cX]):

            # draw the center of the shape on the image
            cv2.circle(pImage, (cX, cY), 7, (0, 255, 0), -1)

            # Put words on image
            cv2.putText(pImage, "X: " + str(cX), (cX - 25, cY - 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

            cv2.putText(pImage, "Y: " + str(cY), (cX - 25, cY - 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        else:
            # Put words on image
            cv2.putText(pImage, "NOT A LINE", (cX - 25, cY - 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 225), 2)
        slope, degrees = contour_slope_degrees(cnt, pImage, cX, cY)
        print("Slope: " + str(slope))
        print("Degrees: " + str(degrees) + "\n")

    except:
        print("SOMETHING WENT WRONG")
        pass

    wut = np.hstack((img, pImage))
    return wut


# calls the function and return stuff
cv2.imshow("IMAGE1", find_line("./test_image/line/Line1.jpg"))
cv2.imshow("IMAGE2", find_line("./test_image/line/Line2.jpg"))
cv2.imshow("IMAGE3", find_line("./test_image/line/Line3.jpg"))
cv2.imshow("IMAGE4", find_line("./test_image/line/Line4.jpg"))
cv2.imshow("IMAGE5", find_line("./test_image/line/Line5.jpg"))
cv2.imshow("IMAGE7", find_line("./test_image/line/Line7.jpg"))
cv2.imshow("IMAGE8", find_line("./test_image/line/Line8.jpg"))


cv2.waitKey(0)
