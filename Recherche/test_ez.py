import numpy as np
import cv2
import pypot.dynamixel
import math
import move
import time
import const
import time

# Get Video feedback from webcam
video_capture = cv2.VideoCapture(0) # -1 for random
video_capture.set(3, 640)
video_capture.set(4, 360)
 
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

t = 0
dt = 0.001
port = "/dev/ttyACM0"
dxl_io = pypot.dynamixel.DxlIO(port)
dxl_io.set_wheel_mode([2, 1])

# Detect green_flag
green_flag = False


def Change_color(img,color):
    global green_flag
    if green_flag == False:
        new_mask = cv2.inRange(crop_img, low_yellow, upper_yellow)
    else:
        if color == 1: # Blue
            new_mask = cv2.inRange(crop_img, low_blue, upper_blue)
        elif color == 2:
            new_mask = cv2.inRange(crop_img, low_red, upper_red)

    return new_mask




# Basic Correction function to change the orientation of the robot
def Correction(motors, error):
	if error < 0:
		rotate(motors, 50, np.pi/4)
	else
		rotate(motors, 50, -np.pi/4)

def Look_for_line(motors):
	rotate(motors, 0, np.pi/3)

def Candidate(cnts):
    len_cnts = len(cnts)
    if len_cnts == 1:
        box = cv2.minAreaRect(cnts[0])
    else:
        candidates=[]
        off_bottom = 0
        for con_num in range(len_cnts):
            box = cv2.minAreaRect(cnts[con_num])
            (x_min,y_min), (w_min,h_min), ang = box
            box_points = cv2.boxPoints(box)
            (x_box, y_box) = box_points[0]
            if y_box > 358:
                off_bottom += 1 
            candidates.append((y_box, con_num,x_min,y_min))
        candidates = sorted(candidates)
        if off_bottom > 1:
            candidates_off_bottom = []
            for con_num in range((len_cnts - off_bottom), len_cnts):
                (y_highest, con_highest, x_min, y_min) = candidates[con_num]
                total_dist = (np.abs(x_min - x_last)**2 + np.abs(y_min - y_last)**2)**0.5
                candidates_off_bottom.append((total_dist,con_highest))
            candidates_off_bottom = sorted(candidates_off_bottom)
        else:
            (y_highest, con_highest, x_min, y_min) = candidates[len_cnts - 1]
            box = cv2.minAreaRect(cnts[con_highest])

    return box

while(True):
    ret, frame = video_capture.read()

    crop_img = frame
    # Color thresholding
    #mask_green = cv2.inRange(crop_img, low_green, upper_green)
    #mask_green_rgb = cv2.cvtColor(mask_green, cv2.COLOR_GRAY2BGR)
    red = cv2.inRange(crop_img, low_red, upper_red)

    Kern = np.ones((3,3), np.uint8)
    red_line = cv2.erode(red, Kern, iterations=5)
    red_line = cv2.dilate(red_line, Kern, iterations=9)
    img, cnts, hierarchy = cv2.findContours(red_line.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #Suppose we only have one big contour to play with
    if len(cnts) > 0:
    	red_box = Candidate(cnts)
    	(x_min,y_min), (w_min,h_min), ang = red_box
    	if ang < - 45:
    		ang += 90
    	if w_min < h_min and ang > 0:
    		ang -= 90
    	if w_min > h_min and ang < 0:
    		ang += 90

    	halfway = 320 # Basically the width by half
    	error = int(x_min - halfway)
    	ang = int(ang)
    	box = cv2.boxPoints(red_box)
    	box = np.int0(box)

    	cv2.drawContours(crop_img, [box], 0, (0,255,0), 3)
    	cv2.putText(crop_img,str(ang), (10,40), cv2.FONT_HERSHEY_SIMPLEX,1, (0,0,255), 2)
    	cv2.putText(crop_img,str(error), (10,320), cv2.FONT_HERSHEY_SIMPLEX,1, (255,0,0), 2)
    	cv2.line(crop_img, (int(x_min), int(y_min)), (halfway, int(y_min)), (255,0,0), 3)
    	Rad_Angle = math.radians(ang)
<<<<<<< HEAD
    	error_angle = math.radians(error/4)
    	move.rotate(dxl_io,1000, dt*Rad_Angle)
    	Correction(dxl_io, dt*error_angle)
    	time.sleep(dt)
=======
		err = math.radians(error/4)
        rotate(dxl_io, 300,dt*err + dt*Rad_Angle)
        time.sleep(dt)
>>>>>>> ce5c36cad41c5be65dfc3544a01fe047bc8741a7
    	print(error, ang)
    else:
    	print("I don't see a line")
    	Look_for_line(dxl_io)
    	time.sleep(dt)
    #Display the resulting frame
    #cv2.imshow('frame',crop_img)
    if cv2.waitKey(20) & 0xFF == ord('k'):
        move.stop()
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #Pas de temps
    t += dt
