import cv2
import win32api
import numpy as np
from tkinter import filedialog

InputFile = filedialog.askopenfile()



# Screen Width and Height
ScreenWidth = win32api.GetSystemMetrics(0)
ScreenHeight = win32api.GetSystemMetrics(1)

# Marker Finding function
def MarkerFinding(Template, SourceImage, Index):
    # Reading the source image and the specified template
    Whiteboard = cv2.imread(SourceImage, 0)
    Marker = cv2.imread(Template, 0)
    w, h = Marker.shape[::-1]

    # Finding any template matches
    res = cv2.matchTemplate(Whiteboard, Marker, cv2.TM_CCOEFF_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)

    print("Marker ", Index, " found with confidence: ", maxVal)

    # Getting the coordinates of the bounding boxes
    TopLeft = maxLoc
    TopRight = (TopLeft[0] + w, TopLeft[1])
    BottomLeft = (TopLeft[0], TopLeft[1] + h)
    BottomRight = (TopLeft[0] + w, TopLeft[1] + h)

    # Returning the specific parameters per marker
    if Index == 1 or Index == 4:
        return TopLeft, BottomRight

    elif Index == 2:
        return TopLeft, BottomRight, BottomLeft

    else:
        return TopLeft, BottomRight, TopRight

def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")
    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]


    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    # return the warped image
    return warped

# Reading the Noteboard Image and pattern
# NoteImage = cv2.imread('20200403_115257.png', 0)
# NoteImage = cv2.imread('20200406_141234.jpg', 0)
NoteImage = '20200406_141234.jpg'

# Getting the position of all markers
Marker1 = MarkerFinding("Pattern1.jpg", NoteImage, 1)
Marker2 = MarkerFinding("Pattern2.jpg", NoteImage, 2)
Marker3 = MarkerFinding("Pattern3.jpg", NoteImage, 3)
Marker4 = MarkerFinding("Pattern4.jpg", NoteImage, 4)

Coordinates = [Marker1[0], Marker2[2], Marker4[1], Marker3[2]]

# Displaying the images with the identified markers
DisplayImage = cv2.imread(NoteImage)
cv2.rectangle(DisplayImage, Marker1[0], Marker1[1], (0,0,255), 4)
cv2.rectangle(DisplayImage, Marker2[0], Marker2[1], (0,255,255), 4)
cv2.rectangle(DisplayImage, Marker3[0], Marker3[1], (0,255,0), 4)
cv2.rectangle(DisplayImage, Marker4[0], Marker4[1], (255,0,0), 4)
ResizedDisplay = cv2.resize(DisplayImage, (ScreenWidth, ScreenHeight))
cv2.imshow("Marker Image", ResizedDisplay)
cv2.waitKey(0)
print(Coordinates)

warped_image = four_point_transform(DisplayImage, Coordinates)
cv2.imwrite('Test.jpg', warped_image)
cv2.waitKey(0)