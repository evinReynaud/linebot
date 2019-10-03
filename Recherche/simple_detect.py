import numpy as np
import cv2
import math
import move
import const
import time
#import pypot.dynamixel

#video_capture = cv2.VideoCapture(1) # -1 for random
#video_capture.set(3, 640)
#video_capture.set(4, 360)

#out1 = cv2.VideoWriter('red_normal.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (640,180))
video_capture = cv2.VideoCapture('red_normal.avi')

green_flag = False

lower_blue = np.array([100,50,50])
upper_blue = np.array([130,255,255])

lower_yellow =np.array([20,50,50])
upper_yellow = np.array([50,255,255])

lower_red = np.array([0,50,50])
upper_red = np.array([20, 255, 255])

lower_green = np.array([55, 50,50])
upper_green = np.array([100, 255, 255]) 

#Changing colors
color = 0

t = 0
dt = 0.01
#port = "/dev/ttyACM0"
#dxl_io = pypot.dynamixel.DxlIO(port)
#dxl_io.set_wheel_mode([const.left_motor_id, const.right_motor_id])

def Change_color(img):
	global color
	if color == 0:
		return cv2.inRange(img, lower_yellow, upper_yellow)
	elif color == 1:
		return cv2.inRange(img, lower_blue, upper_blue)
	elif color == 2:
		return cv2.inRange(img, lower_red, upper_red)


def carre(motors, t):
    mod = np.fmod(t,2)
    if mod < 1:
    	return move.rotate(motors,  0.1, 0)
    else:
    	return move.rotate(motors, 0, np.pi/8)

while(video_capture.isOpened()):

	while not green_flag and color < 3:
	    
	    ret, frame = video_capture.read()
	    crop_img = frame#[180:360, 0:640]
	    #out1.write(crop_img)
	    crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)    
	    # Color thresholding
	    #mask_green = cv2.inRange(crop_img, low_green, upper_green)
	    #mask_green_rgb = cv2.cvtColor(mask_green, cv2.COLOR_GRAY2BGR)
	    red = Change_color(crop_img) 

	    Kern = np.ones((3,3), np.uint8)
	    red_line = cv2.erode(red, Kern, iterations=5)
	    red_line1 = cv2.dilate(red_line, Kern, iterations=9)

	    left_red = red_line[0:180, 0:256]
	    center_red = red_line[0:180, 256:384]
	    right_red = red_line[0:180, 384:640]

	    left_mean = np.mean(left_red)
	    right_mean = np.mean(right_red)
	    center_mean = np.mean(center_red)

	    K = 0.5
	    err = left_mean - right_mean
	    #mean = (left_mean + right_mean)/2
	    total = (left_mean + center_mean + right_mean)
	    #err < (1+K)*mean
	    if np.abs(total) < 5:
	    	print("no line in sight")
	    elif left_mean > center_mean:
	    	#move.rotate(dxl_io, 0.1, -np.pi/6)
	    	print("left")
	    elif right_mean > center_mean:
	    	#move.rotate(dxl_io, 0.1, np.pi/6)
	    	print("right")
	    else:
	    	#move.rotate(dxl_io, 0.3, 0)
	    	print("forward")

	    print(left_mean, right_mean)
	    #carre(dxl_io,t)
	    cv2.imshow("mask", red)
	    cv2.imshow("erode", red_line)
	    cv2.imshow("dilate", red_line1)
	    cv2.imshow("avant", frame)
	    

	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break

    	t += dt

video_capture.release()
#out1.release()
cv2.destroyAllWindows()

