from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import imutils
import numpy as np
import cv2
import math
from PIL import Image
import sys

coins = {
            'Quarter': {'Size': 0.9, 'Value': .25},
            'Dime': {'Size': 0.6, 'Value': .10},
            'Nickel': {'Size': 0.8, 'Value': .05},
            'Penny': {'Size': 0.7, 'Value': .01}
        }

coinsFound = []


'''
Resizes image if it's too big since it throws off the transform.
If camera was rotated, PIL rotates the image. try-except reverts
it back to original orientation.
'''
def resizeImage(image, width, height):
    try:
        imgName = "sample_imgs/_.jpg"
        resizingImg = Image.open(image)

        exif = resizingImg.info['exif']

        newImg = resizingImg.resize((width, height), Image.ANTIALIAS)
        newImg.save(imgName, exif=exif)
    except:
        imgName = "sample_imgs/_.jpg"
        resizingImg = Image.open(image)

        newImg = resizingImg.resize((width, height), Image.ANTIALIAS)
        newImg.save(imgName)

    return imgName


def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


def findCoins(imgName, refCoin):
    # load the image, convert it to grayscale, and blur it slightly
    image = cv2.imread(imgName)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    # perform edge detection, then perform a dilation + erosion to
    # close gaps in between object edges
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)

    # find contours in the edge map
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    # sort the contours from left-to-right and initialize the
    # 'pixels per metric' calibration variable
    (cnts, _) = contours.sort_contours(cnts)
    pixelsPerMetric = None

    # loop over the contours individually
    for c in cnts:
        # if the contour is not sufficiently large, ignore it
        if cv2.contourArea(c) < 100:
        	continue

        # compute the rotated bounding box of the contour
        orig = image.copy()
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")

        # order the points in the contour from left to right, top to bottom
        box = perspective.order_points(box)
        cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

        # loop over the original points and draw them
        for (x, y) in box:
        	cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

        # find horizontal midpoint of bounding box
        (tl, tr, br, bl) = box
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)

        # find diagonal midpoint of bounding box
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)

        # compute the Euclidean distance between the midpoints
        dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
        dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

        # compute pixel per metric ratio
        if pixelsPerMetric is None:
            if refCoin == 'p':
                pixelsPerMetric = dB / 0.73
            elif refCoin == 'd':
                pixelsPerMetric = dB / 0.7
            elif refCoin == 'n':
                pixelsPerMetric = dB / 0.83
            else:
                pixelsPerMetric = dB / 0.93

        # compute the size of the object
        dimA = dA / pixelsPerMetric
        dimB = dB / pixelsPerMetric

        if dimA > 0.6 and dimB > 0.6:
            coinsFound.append((dimA, dimB))

        # draw the object sizes on the image
        cv2.putText(orig, "{:.3f}in".format(dimA),
        	(int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
        	0.65, (0, 255, 0), 2)
        cv2.putText(orig, "{:.3f}in".format(dimB),
        	(int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
        	0.65, (0, 255, 0), 2)

        # show the output image
        #cv2.imshow("Image", orig)
        #cv2.waitKey(0)

    print coinsFound
    return coinsFound


def calculateChange(coins, coinsFound):
    sum = 0
    for key in coins:
        i = 0
        while i < len(coinsFound):
            if (abs(coins[key]['Size'] - math.floor(coinsFound[i][0] * 10)/10) == 0 or
            abs(coins[key]['Size'] - math.floor(coinsFound[i][1] * 10)/10) == 0):
                sum += coins[key]['Value']
                del coinsFound[i]
                if i == 0:
                    i = 0
                else:
                    i -= 1
            else:
                i += 1

    print "\n"
    print "Total change: " + str(sum)

###############################################################################
###############################################################################
###############################################################################


imgName = "sample_imgs/" + sys.argv[1]
refCoin = sys.argv[2]
tempImage = Image.open(imgName)
if tempImage.size[0] > 800 and tempImage.size[1] > 800:
    coinsFound = findCoins(resizeImage(imgName, 800, 600), refCoin)

else:
    coinsFound = findCoins(imgName, refCoin)

calculateChange(coins, coinsFound)
