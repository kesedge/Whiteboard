import cv2
import win32api
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


# Selecting the desired Image and naming the output path
#FilePath = filedialog.askopenfile()
#NoteImage = FilePath.name
OutputPath = "C:\\Users\\me1ked\\Documents\\Personal Notes\\"
#OutputImage = input('Please enter name of notes...')

# Screen Width and Height
ScreenWidth = win32api.GetSystemMetrics(0)
ScreenHeight = win32api.GetSystemMetrics(1)
dimensions = str(ScreenWidth) + "x" + str(ScreenHeight)

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

# Class containing the parameters for the warping matrix
class TransformMatrix:
    def __init__(self):
        self.dstMatrix = np.float32([(0, 0),
                                     (0, 3456),
                                     (4608, 0),
                                     (4608, 3456)])

# Generating the Transform Matrix object
Transform = TransformMatrix()
TranMatrix = Transform.dstMatrix

# Getting the position of all markers
#Marker1 = MarkerFinding("Pattern1.jpg", NoteImage, 1)
#Marker2 = MarkerFinding("Pattern2.jpg", NoteImage, 2)
#Marker3 = MarkerFinding("Pattern3.jpg", NoteImage, 3)
#Marker4 = MarkerFinding("Pattern4.jpg", NoteImage, 4)

# Displaying the identified markers on the image
# display_markers(NoteImage, Marker1, Marker2, Marker3, Marker4)

# The corner points of each marker
#Coordinates = [Marker1[0], Marker2[2], Marker4[1], Marker3[2]]
#CoordinateArray = np.asarray(Coordinates, dtype = np.float32)

# Generating the warped image
#path = OutputPath + OutputImage+ ".jpg"
#path2 = OutputPath + "Enhanced Image"+ ".jpg"

#WarpedImage = Perspective_Warp(NoteImage, CoordinateArray, TranMatrix)
#cv2.imwrite(path, WarpedImage)
#print("Image rectified and stored as " + path)

class ImageFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Creating the image container
        self.container = tk.Frame(self, bg = 'white', bd = 2, relief = tk.SUNKEN)
        self.container.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        # Marker Images
        self.Marker1 = "Pattern1.jpg"
        self.Marker2 = "Pattern2.jpg"
        self.Marker3 = "Pattern3.jpg"
        self.Marker4 = "Pattern4.jpg"

        # Creating the warping point coordinates
        self.point1 = []
        self.point2 = []
        self.point3 = []
        self.point4 = []
        self.pointArray = np.ones((4,2), dtype=np.float32)
        self.warped = []

        # Initialising the display window content
        self.WindowDisplay = tk.Label(self.container)

        # Initialising the transform Matrix
        self.TransMat = TransformMatrix().dstMatrix

        # Labelling the Container
        Title = tk.Label(self, text="Image Frame", font = ("Arial Bold", 20), bg="white")
        Title.pack()

    # Displaying the image
    def display_image(self, ImagePath, container):
        # Getting the dimensions of the container
        FrameWidth = container.winfo_width()
        FrameHeight = container.winfo_height()
        dimensions = (FrameWidth, FrameHeight)

        # Resizing the image then displaying
        RawImage = Image.open(ImagePath)
        print(type(RawImage))
        ResizedImage = RawImage.resize(dimensions)
        DisplayImage = ImageTk.PhotoImage(ResizedImage)
        self.WindowDisplay.config(image=DisplayImage)
        self.WindowDisplay.image = DisplayImage
        self.WindowDisplay.pack()

    # Finding the markers in the image
    def Identify_Markers(self, M1, M2, M3, M4, ImagePath):
        SampleImage = cv2.imread(ImagePath,0)
        Temp1 = cv2.imread(M1,0)
        Temp2 = cv2.imread(M2,0)
        Temp3 = cv2.imread(M3,0)
        Temp4 = cv2.imread(M4,0)

        # Getting the template shapes
        w1, h1 = Temp1.shape[::-1]
        w2, h2 = Temp2.shape[::-1]
        w3, h3 = Temp3.shape[::-1]
        w4, h4 = Temp4.shape[::-1]

        # Finding any template matches
        res1 = cv2.matchTemplate(SampleImage, Temp1, cv2.TM_CCOEFF_NORMED)
        res2 = cv2.matchTemplate(SampleImage, Temp2, cv2.TM_CCOEFF_NORMED)
        res3 = cv2.matchTemplate(SampleImage, Temp3, cv2.TM_CCOEFF_NORMED)
        res4 = cv2.matchTemplate(SampleImage, Temp4, cv2.TM_CCOEFF_NORMED)

        # Getting match information
        minVal1, maxVal1, minLoc1, maxLoc1 = cv2.minMaxLoc(res1)
        minVal2, maxVal2, minLoc2, maxLoc2 = cv2.minMaxLoc(res2)
        minVal3, maxVal3, minLoc3, maxLoc3 = cv2.minMaxLoc(res3)
        minVal4, maxVal4, minLoc4, maxLoc4 = cv2.minMaxLoc(res4)

        # Printing background information
        print("Marker 1 found with confidence: ", maxVal1)
        print("MaxLoc1: ", maxLoc1)
        print("Marker 2 found with confidence: ", maxVal2)
        print("MaxLoc2: ", maxLoc2)
        print("Marker 3 found with confidence: ", maxVal3)
        print("MaxLoc3: ", maxLoc3)
        print("Marker 4 found with confidence: ", maxVal4)
        print("MaxLoc4: ", maxLoc4)


        # Coordinates in the form [Top Left, Top Right, Bottom Left, Bottom Right]
        M1Coordinates = [maxLoc1, (maxLoc1[0] + w1, maxLoc1[1]), (maxLoc1[0], maxLoc1[1] + h1),
                         (maxLoc1[0] + w1, maxLoc1[1] + h1)]
        M2Coordinates = [maxLoc2, (maxLoc2[0] + w2, maxLoc2[1]), (maxLoc2[0], maxLoc2[1] + h2),
                         (maxLoc2[0] + w2, maxLoc2[1] + h2)]
        M3Coordinates = [maxLoc3, (maxLoc3[0] + w3, maxLoc3[1]), (maxLoc3[0], maxLoc3[1] + h3),
                         (maxLoc3[0] + w3, maxLoc3[1] + h3)]
        M4Coordinates = [maxLoc4, (maxLoc4[0] + w4, maxLoc4[1]), (maxLoc4[0], maxLoc4[1] + h4),
                         (maxLoc4[0] + w4, maxLoc4[1] + h4)]

        # Tuples of the outer transform coordinates
        self.point1 = M1Coordinates[0] # Top Left
        self.point2 = M2Coordinates[2] # Bottom Left
        self.point3 = M3Coordinates[1] # Top Right
        self.point4 = M4Coordinates[3] # Bottom Right

        PointList = [self.point1, self.point2, self.point3, self.point4]
        self.pointArray = np.asarray(PointList, dtype=np.float32)

        # Printing the values as coordinates
        print(PointList)

    def Display_markers(self):
        print("Hello")

    # Function for printing Marker Positions
    def Marker_Positions(self):
        print(self.point1, self.point2, self.point3, self.point4)
        print(self.pointArray)

    def Enhance_Perspective(self, ImagePath, MarkerPoints, TransformMatrix):
        # Reading the input image and getting dimensions
        Img = cv2.imread(ImagePath)
        h, w = Img.shape[:2]

        # Creating the perspective transform based on the input RoI and the destination shape
        M = cv2.getPerspectiveTransform(MarkerPoints, TransformMatrix)

        # Warping the image
        self.warped = cv2.warpPerspective(Img, M, (w, h), flags=cv2.INTER_LINEAR)
        print("Image Warped")
        cv2.waitKey(0)

    def display_warped(self, image, container):
        # Get frame dimensions
        FrameWidth = container.winfo_width()
        FrameHeight = container.winfo_height()
        dimensions = (FrameWidth, FrameHeight)

        # Convert numpy array to PIL image
        ConvertedImage = Image.fromarray(image)

        NewImage = ConvertedImage.resize(dimensions)
        print(type(NewImage))
        DisplayImage = ImageTk.PhotoImage(NewImage)
        self.WindowDisplay.config(image=DisplayImage)
        self.WindowDisplay.image = DisplayImage
        self.WindowDisplay.pack()

    def PrintPointArray(self):
        print(self.pointArray)
        print(self.TransMat)

class ControlsFrame(tk.Frame):
    def __init__(self,parent, ImgFrame, *args, **kwargs):
        super().__init__(parent, ImgFrame, *args, **kwargs)

        # Labelling the Container
        Title = tk.Label(self, text="Controls Frame", font = ("Arial Bold", 20), bg="white")
        Title.grid(row=0)

        # The first step
        Step1 = tk.Label(self, text="1) Select the file path for the raw image", font = ("Arial Bold", 14), bg="white")
        Step1.grid(row = 1, sticky=tk.W)
        self.FilePath = tk.StringVar()

        # Creating the buttons
        FileButton = tk.Button(self, text="File Path", bg="blue", fg="white", font = ("Arial Bold", 12),
                               command = lambda: ImagePath(self))
        FileButton.grid(row=2, column=0, sticky=tk.W)

        # The second step
        Step2 = tk.Label(self, text="2) Optional - Display Image", font=("Arial Bold", 14), bg="white")
        Step2.grid(row=3, sticky=tk.W)

        DisplayButton = tk.Button(self, text="Display Raw Image", bg="blue", fg="white", font = ("Arial Bold", 12),
                               command = lambda: ImgFrame.display_image(self.FilePath, ImgFrame.container))
        DisplayButton.grid(row=4, column=0, sticky=tk.W)

        # The third step
        Step1 = tk.Label(self, text="3) Identify Markers In Image", font=("Arial Bold", 14), bg="white")
        Step1.grid(row=5, sticky=tk.W)
        self.FilePath = tk.StringVar()

        # Creating the buttons
        FileButton = tk.Button(self, text="Identify Markers", bg="blue", fg="white", font=("Arial Bold", 12),
                               command=lambda: ImgFrame.Identify_Markers(ImgFrame.Marker1,ImgFrame.Marker2,
                                                                         ImgFrame.Marker3,ImgFrame.Marker4,
                                                                         self.FilePath))
        FileButton.grid(row=6, column=0, sticky=tk.W)

        # The fourth step
        Step1 = tk.Label(self, text="4) Optional - Print Marker Coordinates", font=("Arial Bold", 14), bg="white")
        Step1.grid(row=7, sticky=tk.W)
        self.FilePath = tk.StringVar()

        # Creating the buttons
        FileButton = tk.Button(self, text="Print Coordinates", bg="blue", fg="white", font=("Arial Bold", 12),
                               command=lambda: ImgFrame.Marker_Positions())
        FileButton.grid(row=8, column=0, sticky=tk.W)

        # The fifth step
        Step1 = tk.Label(self, text="5) Print Point Array", font=("Arial Bold", 14), bg="white")
        Step1.grid(row=9, sticky=tk.W)
        self.FilePath = tk.StringVar()

        # Creating the buttons
        FileButton = tk.Button(self, text="Point Array Coordinates", bg="blue", fg="white", font=("Arial Bold", 12),
                               command=lambda: ImgFrame.PrintPointArray())
        FileButton.grid(row=10, column=0, sticky=tk.W)

        # The sixth step
        Step1 = tk.Label(self, text="6) Adjust Image Perspective", font=("Arial Bold", 14), bg="white")
        Step1.grid(row=11, sticky=tk.W)
        self.FilePath = tk.StringVar()

        # Creating the buttons
        FileButton = tk.Button(self, text="Warp Perspective", bg="blue", fg="white", font=("Arial Bold", 12),
                               command=lambda: ImgFrame.Enhance_Perspective(self.FilePath, ImgFrame.pointArray,
                                                                            ImgFrame.TransMat))
        FileButton.grid(row=12, column=0, sticky=tk.W)

        # The seventh step
        Step1 = tk.Label(self, text="7) Display Perspective Image", font=("Arial Bold", 14), bg="white")
        Step1.grid(row=13, sticky=tk.W)
        self.FilePath = tk.StringVar()

        # Creating the buttons
        FileButton = tk.Button(self, text="Display Perspective Image", bg="blue", fg="white", font=("Arial Bold", 12),
                               command=lambda: ImgFrame.display_warped(ImgFrame.warped, ImgFrame.container))
        FileButton.grid(row=14, column=0, sticky=tk.W)

        # Function for specifying the image
        def ImagePath(self):
            Path = tk.filedialog.askopenfile()
            self.FilePath = Path.name
            print(self.FilePath)


# Creating the required frames for placing controls

# Creating the main window
MainWindow = tk.Tk()
MainWindow.geometry(dimensions)
MainWindow.title("Whiteboard Notes Converter")

ImageContainer = ImageFrame(master = MainWindow, bg = 'white', bd = 2, relief = tk.SUNKEN)
ControlFrame = ControlsFrame(parent = MainWindow, ImgFrame=ImageContainer, bg = 'white', bd = 2, relief = tk.SUNKEN)

ImageContainer.place(relx=0, rely=0, relwidth=0.7, relheight=1)
ControlFrame.place(relx=0.7, rely=0, relwidth=0.3, relheight=1)
MainWindow.mainloop()