import cv2
import win32api
import numpy as np
import tkinter as tk
from tkinter import filedialog

# Making sure that the TK window remains closed
MainWindow = tk.Tk()
MainWindow.withdraw()

# Selecting the desired Image and naming the output path
FilePath = filedialog.askopenfile()
NoteImage = FilePath.name
OutputPath = "C:\\Users\\me1ked\\Documents\\Personal Notes\\"
OutputImage = input('Please enter name of notes...')

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

# Function for displaying markers
def display_markers(Disp_Image, M1, M2, M3, M4):
    # Displaying the images with the identified markers
    DisplayImage = cv2.imread(Disp_Image)

    # Reconstruct identified markers for display
    cv2.rectangle(DisplayImage, M1[0], M1[1], (0, 0, 255), 4)
    cv2.rectangle(DisplayImage, M2[0], M2[1], (0, 255, 255), 4)
    cv2.rectangle(DisplayImage, M3[0], M3[1], (0, 255, 0), 4)
    cv2.rectangle(DisplayImage, M4[0], M4[1], (255, 0, 0), 4)

    # Resizing images for display
    ResizedDisplay = cv2.resize(DisplayImage, (ScreenWidth, ScreenHeight))
    cv2.imshow("Identified Markers", ResizedDisplay)
    cv2.waitKey(0)

# Function for rectifying the image perspective
def Perspective_Warp(ImgPath, RoI, DestinationShape):
    Img = cv2.imread(ImgPath)
    h, w = Img.shape[:2]

    # Creating the perspective transform based on the input RoI and the destination shape
    M = cv2.getPerspectiveTransform(RoI, DestinationShape)

    # Warping the image
    warped = cv2.warpPerspective(Img, M, (w, h), flags=cv2.INTER_LINEAR)
    return warped

# Function for enhancing image contrast
def ContrastEnhancement(Image):
    # Enhancing the contrast of the image row by row, col by col and c by c
    alpha = 1.5
    beta = 0

    dimensions = Image.shape
    ContrastImage = np.zeros(dimensions, Image.dtype)


    for y in range(Image.shape[0]):
        for x in range(Image.shape[1]):
            for c in range(Image.shape[2]):
                ContrastImage[y, x, c] = np.clip(alpha * Image[y, x, c] + beta, 0, 255)

    return ContrastImage

# Class containing the parameters for the warping matrix
class TransformMatrix:
    def __init__(self):
        self.dstMatrix = np.float32([(0, 0),
                                     (0, 3456),
                                     (4608, 3456),
                                     (4608, 0)])

# Generating the Transform Matrix object
Transform = TransformMatrix()
TranMatrix = Transform.dstMatrix

# Getting the position of all markers
Marker1 = MarkerFinding("Pattern1.jpg", NoteImage, 1)
Marker2 = MarkerFinding("Pattern2.jpg", NoteImage, 2)
Marker3 = MarkerFinding("Pattern3.jpg", NoteImage, 3)
Marker4 = MarkerFinding("Pattern4.jpg", NoteImage, 4)

# Displaying the identified markers on the image
# display_markers(NoteImage, Marker1, Marker2, Marker3, Marker4)

# The corner points of each marker
Coordinates = [Marker1[0], Marker2[2], Marker4[1], Marker3[2]]
print(Coordinates)
CoordinateArray = np.asarray(Coordinates, dtype = np.float32)

# Generating the warped image
path = OutputPath + OutputImage+ ".jpg"
path2 = OutputPath + "Enhanced Image"+ ".jpg"

WarpedImage = Perspective_Warp(NoteImage, CoordinateArray, TranMatrix)
cv2.imwrite(path, WarpedImage)
print("Image rectified and stored as " + path)
