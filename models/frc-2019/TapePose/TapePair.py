import math


class TapePairs:
    def __init__(self, contours, center):
        self.center = center
        self.contours = contours
        self.contourPairs = []
        self.pair()

    def pair(self):
        self.contourPairs.clear()
        for i in range(len(self.contours) - 1):
            self.contourPairs.append([self.contours[i], self.contours[i + 1]])
        self.contourPairs = list(filter(lambda contourPair: self.getIntersection(contourPair), self.contourPairs))

    # return if the intersection is above the centroid or not
    def getIntersection(self, contourPair):
        def lfrPT(contour):
            leftpt = sorted(contour, key=lambda a: a[0][0])[0][0]
            rightpt = sorted(contour, key=lambda a: a[0][0])[-1][0]
            return leftpt, rightpt

        def estimateAngle(lefpt, rightpt):
            # right is: /  \ : left
            if lefpt[1] < rightpt[1]:
                return "l"
            elif lefpt[1] > rightpt[1]:
                return "r"
            else:
                return None

        leftpt0, rightpt0 = lfrPT(contourPair[0])
        leftpt1, rightpt1 = lfrPT(contourPair[1])

        angle0 = estimateAngle(leftpt0, rightpt0)
        angle1 = estimateAngle(leftpt1, rightpt1)

        return angle0 == "r" and angle1 == "l"

    def findCentroid(self, contour):
        leftpt = sorted(contour, key=lambda a: a[0][0])[0][0]
        rightpt = sorted(contour, key=lambda a: a[0][0])[-1][0]
        centroid = (int((leftpt[0] + rightpt[0]) / 2), int((leftpt[1] + rightpt[1]) / 2))
        return centroid

    def getPair(self):
        try:
            list.sort(self.contourPairs, key=lambda contourPair: self.closeCenter(self.findCentroid(contourPair[0]),
                                                                                  self.findCentroid(contourPair[1]),
                                                                                  self.center))
            c0 = self.contourPairs[0][0]
            c1 = self.contourPairs[0][1]
            # TODO Just to Minimum Bounding Rect Here
            return [c0, self.findCentroid(c0)], [c1, self.findCentroid(c1)]
        except IndexError:
            pass

    def closeCenter(self, contourCenter0, contourCenter1, center):
        return getDistance(contourCenter0, center) + getDistance(contourCenter1, center)



def getMinMax(min, max, val):
    return min <= val <= max


def getDistance(p1, p2):
    return int(math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2))
