import cv2
import numpy as np
import math

# Cam test splits a image and loop through the 3 dimensional list and set a specific parameter for each individual pixel
# TODO it takes 7-10 second to process one single image (Cube 1) make it faster
# TODO look into Numpy and different ways of processing images

"""
This is a model that works but probably could not be implemented without optimization. Takes too long for one image 
to process (7-10 seconds)
"""

# TODO Find pixel of Camera so that the pixels are aligned

# TODO FIND MULTIPLE CONTOURS

# TODO PUT DIRECTIONS ON 2018 ROBOTIC FRC


def find_centroid(contour, img):

    try:

        # compute the center of the contour
        M = cv2.moments(contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        # create a list for the big contours
        eligible = []

        for x in range(len(contour)):
            if cv2.moments(x)["m00"] >= 0:
                eligible.append(contour[x])

        # box the stuff
        for i in range(len(eligible)):

            x, y, w, h = cv2.boundingRect(eligible[i])

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # draw the center of the shape on the image
            cv2.circle(img, (cX, cY), 7, (0, 0, 255), -1)

            # Put words on image
            cv2.putText(img, "X: " + str(cX), (cX - 25, cY - 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 2)

            cv2.putText(img, "Y: " + str(cY), (cX - 25, cY - 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 2)

    except ZeroDivisionError:
        pass

    return img


def find_mask(img):

    # find images that are not black and turn them white
    lower = np.array([1, 1, 1], dtype="uint8")
    upper = np.array([255, 255, 255], dtype="uint8")

    # Use a mask to find the contour and plot the rectangle
    mask = cv2.inRange(img, lower, upper)

    return mask


def find_color(name):

    print(name)

    wut = cv2.imread(name)
    img = cv2.resize(wut, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
    height, width, channels = img.shape
    # Split image into 3 two dimensional list
    blue_list, green_list, red_list = cv2.split(img)

    # print("height: " + str(height))
    # print("width: " + str(width))

    # loop through all of red_list to access the array inside
    for x in range(width):
        # loop through individual values in the inner most list, and those values are the red values of the pixels
        for i in range(height):

            # Assign values so it's easier to manage
            red = red_list[i][x]
            blue = blue_list[i][x]
            green = green_list[i][x]

            # Setting the green high and low parameter, it's proportional to red
            green_low = red - 30
            green_high = red + 18

            # difference is the difference between red/green and blue, since blue is not usually used in yellow
            # the difference needs to be big
            difference = (int(green) + int(red))/2 - int(blue)

            # Similarity detects the similarities in red blue and green, used for excluding grey, white, black pixel
            similarity = (abs(int(green)-int(red)) + abs(int(red)-int(blue)) + abs(int(green)-int(blue)))

            # green has to be inside parameter
            green_in_param = green_low <= green <= green_high

            # if the difference bigger between red and blue is higher than 80, it is NOT yellow
            isYellow = difference >= 55

            # if the sum of the differences of all 3 rbg values are within 30, that means that it's grey
            isGrey = similarity <= 30

            # if either of those statements are false, it will set te pixel to black
            if not green_in_param or not isYellow or isGrey:
                green_list[i][x] = 0
                blue_list[i][x] = 0
                red_list[i][x] = 0

    # Merge and create the processed image
    final_image = cv2.merge((blue_list, green_list, red_list))

    try:
        # final image is the separated image, find_mask
        # find mask finds the correct format of image findContour will use
        im2, contours, hierarchy = cv2.findContours(find_mask(final_image), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnt = max(contours, key=cv2.contourArea)

        find_centroid(cnt, final_image)

    except ValueError:
        pass

    # Return the final image side by side with the original with np.hstack
    # hm = np.hstack([img, name])
    return final_image


# could only return one at a time, find out why?
# calls the function and return stuff

cv2.imshow("IMAGE2", find_color("./test_image/cubes/Cube1.jpg"))
# cv2.imshow("IMAGE2", find_color("./test_image/cubes/Cube2.jpg"))
# cv2.imshow("IMAGE2", find_color("./test_image/cubes/Cube3.jpg"))
# cv2.imshow("IMAGE2", find_color("./test_image/cubes/Cube4.jpg"))
# cv2.imshow("IMAGE2", find_color("./test_image/cubes/Cube5.jpg"))
# cv2.imshow("IMAGE2", find_color("./test_image/cubes/Cube7.jpg"))
# cv2.imshow("IMAGE2", find_color("./test_image/cubes/Cube8.jpg"))
# cv2.imshow("IMAGE2", find_color("./test_image/cubes/Cube9.jpg"))

cv2.waitKey(0)
