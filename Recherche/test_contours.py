import numpy as np
import cv2
import imutils
import math

# Get Video feedback from webcam
video_capture = cv2.VideoCapture(1) # -1 for random
#video_capture.set(3, 400)
#video_capture.set(4, 300)
 
# Upper bounds defines, TODO :: define it in a better way
low_red = np.array([0,0,100])
upper_red = np.array([80,80,225]) 

low_green = np.array([0,100,0])
upper_green = np.array([80,225,80]) 

low_blue = np.array([100,0,0])
upper_blue = np.array([225,80,225]) 

# TODO : get the right boundaries for yellow 
low_yellow = np.array([0,100,100])
upper_yellow = np.array([80,225,225]) 

color = 0 # represents colors, 0 : red, 1 : blue, 2 : yellow

while(True):
    # Capture the frames
    global mask
    global mask_rgb

    ret, frame = video_capture.read()

    # Crop the image
    crop_img = frame#[150:300, 0:400]

    # Color thresholding
    mask_green = cv2.inRange(crop_img, low_green, upper_green)
    mask_green_rgb = cv2.cvtColor(mask_green, cv2.COLOR_GRAY2BGR)
    
    # User  
    if (cv2.waitKey(10) & 0xFF == ord('b')):
        color = 1   
    if cv2.waitKey(10) & 0xFF == ord('y'):
        color = 2
    if cv2.waitKey(10) & 0xFF == ord('r'):
        color = 0

    if color == 1 :
        mask = cv2.inRange(crop_img, low_blue, upper_blue)
        mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        mask = mask_rgb | mask_green_rgb
        print("bleue")
    elif color == 2:
        mask = cv2.inRange(crop_img, low_yellow, upper_yellow)
        mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        mask = mask_rgb | mask_green_rgb
        print("yellow")
    else:
        mask = cv2.inRange(crop_img, low_red, upper_red)
        mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        mask = mask_rgb | mask_green_rgb
        print("red")

    crop_img = crop_img & mask

    # Convert to grayscale
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    # Gaussian blur
    gray = cv2.GaussianBlur(gray,(7,7),0)
    #Get edges of the red line
    edges = cv2.Canny(gray, 200, 100)
    edges = cv2.dilate(edges, None, iterations=1)
    edges = cv2.erode(edges, None, iterations=1)

    #ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
    # Find the contours of the frame
    contours = cv2.findContours(edges.copy(), 1, cv2.CHAIN_APPROX_NONE)
    contours = imutils.grab_contours(contours)

    # Find the biggest contour (if detected)
    if len(contours) > 0:
        #c = max(contours, key=cv2.contourArea)
        #M = cv2.moments(c)
        #if M['m00'] != 0:
        #    cx = int(M['m10']/M['m00'])
        #    cy = int(M['m01']/M['m00'])
        #else:
        #    cx = 0
        #cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
        #cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
        #cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)

        #if cx >= 120:
        #    print("Turn Left!")
        #if cx < 120 and cx > 50:
        #    print("On Track!")
        #if cx <= 50:
        #    print("Turn Right")

        # sorting the contours to find the largest and smallest one
        c1 = max(contours, key=cv2.contourArea)
        c2 = min(contours, key=cv2.contourArea)

        # determine the most extreme points along the contours
        #extLeft1 = tuple(c1[c1[:, :, 0].argmin()][0])
        extRight1 = tuple(c1[c1[:, :, 0].argmax()][0])
        #extLeft2 = tuple(c2[c2[:, :, 0].argmin()][0])
        extRight2 = tuple(c2[c2[:, :, 0].argmax()][0])

        Ang = np.cos(np.pi/4)

        cimg = cv2.drawContours(crop_img, contours, -1, (0,255,0), 2)
        # compute the distance between the points (x1, y1) and (x2, y2)
        #dist1 = math.sqrt( ((extLeft1[0]-extRight1[0])**2)+((extLeft1[1]-extRight1[1])**2) )
        #dist2 = math.sqrt( ((extLeft2[0]-extRight2[0])**2)+((extLeft2[1]-extRight2[1])**2) )
        #Angle1 = np.arctan2( extLeft1[1]-extRight1[1]*Ang, extLeft1[0]-extRight1[0]*Ang )
        #Angle2 = np.arctan2( extLeft2[1]-extRight2[1]*Ang, extLeft2[0]-extRight2[0]*Ang )

        # draw lines
        #cv2.line(cimg, extLeft1, extRight1, (255,0,0), 1)
        cv2.line(cimg, extLeft2, extRight2, (255,0,0), 1)

        # draw the distance text
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 0.5
        fontColor = (255,255,255)
        lineType = 1
        #cv2.putText(cimg,str(Angle1),(140,150),font, fontScale, fontColor, lineType)
        #cv2.putText(cimg,str(Angle2),(280,150),font, fontScale, fontColor, lineType)
    else:
        print("I don't see the line")

    #Display the resulting frame
    cv2.imshow('frame',crop_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break