import numpy as np
import cv2
import math
import move
import const
import time
import pypot.dynamixel

video_capture = cv2.VideoCapture(0) # -1 for random
video_capture.set(3, 640)
video_capture.set(4, 360)

#low_blue = np.array([0,0,100])
#upper_blue = np.array([80,80,225]) 

lower_blue = np.array([100,50,50])
upper_blue = np.array([130,255,255])

lower_yellow =np.array([20,50,50])
upper_yellow = np.array([50,255,255])

lower_red = np.array([0,50,50])
upper_red = np.array([20,255,255])

lower_green = np.array([55, 50,50])
upper_green = np.array([100, 255, 255]) 

#
#lines = [0,214,288,352,428,640]
screen_half_width = 320
band_half_width = 2/5 * screen_half_width #37
band_offset = 3/5*screen_half_width #69

lines = [
    0,
    screen_half_width-band_offset-band_half_width, 
    screen_half_width-band_offset+band_half_width,
    screen_half_width+band_offset-band_half_width,
    screen_half_width+band_offset+band_half_width,
    2*screen_half_width]

#lower_green = np.array

t = 0
dt = 2
port = "/dev/ttyACM0"
dxl_io = pypot.dynamixel.DxlIO(port)
dxl_io.set_wheel_mode([const.left_motor_id, const.right_motor_id])

def carre(motors, t):
    mod = np.fmod(t,2)
    if mod < 1:
    	return move.rotate(motors,  0.1, 0)
    else:
    	return move.rotate(motors, 0, np.pi/8)

while(True):
    ret, frame = video_capture.read()

    crop_img = frame[180:360, 0:640]

    crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)    
    
    # Color thresholding
    #mask_green = cv2.inRange(crop_img, low_green, upper_green)
    #mask_green_rgb = cv2.cvtColor(mask_green, cv2.COLOR_GRAY2BGR)
    red = cv2.inRange(crop_img, lower_yellow, upper_yellow)

    #red = crop_img & 
    Kern = np.ones((3,3), np.uint8)
    red_line = cv2.erode(red, Kern, iterations=5)
    red_line = cv2.dilate(red_line, Kern, iterations=9)

    #left_red = red_line[0:180, 0:256]
    ##center_red = red_line[0:180, 256:384]
    #right_red = red_line[0:180, 384:640]
    bands = []
    means = []
    max = 0
    max_index = 0
    for i in range(len(lines)-1):
        bands.append(red_line[0:180, lines[i]:lines[i+1]])
        means.append(np.mean(bands[i]))
        if max < means[i]:
            max = means[i]
            max_index = i

    K = [0.001, 0.01, 0.001]
    speed = [0.2, 0.15, 0.05]
    K_index = np.abs(max_index-2)
    
    if sum(means) < 5:
        move.rotate(dxl_io,-0.05,0)
    elif K_index == 2:
        move.rotate(dxl_io,speed[K_index],K[K_index]*means[max_index])
        print("we're in borders")
    else:
        err = means[max_index-1] - means[max_index+1]
        move.rotate(dxl_io,speed[K_index],K[K_index]*err) 
        print("Land ahoy!")

   	#print(err)
   #elif left_mean > 5*center_mean:
   # 	move.rotate(dxl_io, 0.1, err)
   # 	print("left")
   # elif right_mean > 5*center_mean:
   # 	move.rotate(dxl_io, 0.1, err)
   # 	print("right")
   # else:
   # 	move.rotate(dxl_io, 0.3, 0)
   # 	print("forward")

    #print(left_mean, right_mean)
    #carre(dxl_io,t)

    #cv2.imshow("frame", red_line)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break
    t += dt
    #time.sleep(dt)
    #t += dt





