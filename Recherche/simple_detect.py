import numpy as np
import cv2
import math
import move
import const
import time
#import pypot.dynamixel

# video_capture = cv2.VideoCapture(1) # -1 for random
#video_capture.set(3, 640)
#video_capture.set(4, 360)

#out1 = cv2.VideoWriter('red_normal.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (640,180))
video_capture = cv2.VideoCapture(1)#'red_part.mp4')


lower_blue = np.array([100, 50, 50])
upper_blue = np.array([130, 255, 255])

lower_yellow = np.array([20, 50, 50])
upper_yellow = np.array([50, 255, 255])

lower_red = np.array([0, 50, 50])
upper_red = np.array([20, 255, 255])

lower_green = np.array([55, 50, 50])
upper_green = np.array([100, 255, 255])

# Changing colors
color = 2
color_switch = False
t = 0
dt = 0.01
#port = "/dev/ttyACM0"
#dxl_io = pypot.dynamixel.DxlIO(port)
#dxl_io.set_wheel_mode([const.left_motor_id, const.right_motor_id])


def Change_color(img):
    global color
    global color_switch
    if color == 0:
        return cv2.inRange(img, lower_yellow, upper_yellow)
    elif color == 1:
        return cv2.inRange(img, lower_blue, upper_blue)
    elif color == 2:
        return cv2.inRange(img, lower_red, upper_red)


def carre(motors, t):
    mod = np.fmod(t, 2)
    if mod < 1:
        return move.rotate(motors, 0.1, 0)
    else:
        return move.rotate(motors, 0, np.pi / 8)

screen_half_width = 320
band_half_width = int(1/5 * screen_half_width) #37
band_offset = int(2/5 * screen_half_width) #69

lines = [
    0,
    screen_half_width-band_offset-band_half_width, 
    screen_half_width-band_offset+band_half_width,
    screen_half_width+band_offset-band_half_width,
    screen_half_width+band_offset+band_half_width,
    2*screen_half_width]

while(video_capture.isOpened()):

        # while color_switch == False and color < 3:
    ret, frame = video_capture.read()
    crop_img = frame[180:360, 0:640]
    # out1.write(crop_img)
    crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
    # Color thresholding
    #mask_green = cv2.inRange(crop_img, low_green, upper_green)
    #mask_green_rgb = cv2.cvtColor(mask_green, cv2.COLOR_GRAY2BGR)
    # Do we see green?
    mask_green = cv2.inRange(crop_img, lower_green, upper_green)
    red = mask_green
    mean_green = np.mean(mask_green)

    #red = Change_color(crop_img)

    Kern = np.ones((3, 3), np.uint8)
    red_line = cv2.erode(red, Kern, iterations=5)
    red_line1 = cv2.dilate(red_line, Kern, iterations=9)

    bands = []
    means = []
    max = 0
    max_index = 0
    for i in range(len(lines) - 1):
        bands.append(red_line[0:180, lines[i]:lines[i + 1]])
        means.append(np.mean(bands[i]))
        if max < means[i]:
            max = means[i]
            max_index = i

    K = [0.001, 0.01, 0.001]
    speed = [0.2, 0.15, 0.05]
    K_index = np.abs(max_index - 2)

    if sum(means) < 5:
        print("There is nothing ")
    elif K_index == 2: # borders, check if max_index is negative 
        sign = 1 if max_index == 0 else -1
        print("we're in borders", max_index, K_index, means[max_index])
    elif K_index == 1: # bands
        err = (max_index-2)*(means[max_index]-means[2])
        print("Land ahoy!", max_index, K_index, err)
    else: # center
    	err = means[1] - means[3]
    	print("Center maan yee", max_index, K_index, err)



    #cv2.line(crop_img, (int(lines[0]), 0), (int(lines[0]), 180), (255,0,0), 3)
    cv2.line(crop_img, (int(lines[1]), 0), (int(lines[1]), 180), (255,0,0), 3)
    cv2.line(crop_img, (int(lines[2]), 0), (int(lines[2]), 180), (255,0,0), 3)
    cv2.line(crop_img, (int(lines[3]), 0), (int(lines[3]), 180), (255,0,0), 3)
    cv2.line(crop_img, (int(lines[4]), 0), (int(lines[4]), 180), (0,255,0),3)
    #err = left_mean - right_mean
    #mean = (left_mean + right_mean)/2
    #total = (left_mean + center_mean + right_mean)
    #err < (1+K)*mean
   # #if np.abs(total) < 5:
   # #	print("no line in sight")
    # elif left_mean > center_mean:
        #move.rotate(dxl_io, 0.1, -np.pi/6)
        # print("left")
    # elif right_mean > center_mean:
        #move.rotate(dxl_io, 0.1, np.pi/6)
    #	print("right")
    # else:
        #move.rotate(dxl_io, 0.3, 0)
    #	print("forward")

    
    #print(left_mean, right_mean)
    # carre(dxl_io,t)
    #cv2.imshow("mask", red)
    cv2.imshow("mask green", red)
    #cv2.imshow("erode", red_line)
    cv2.imshow("dilate mask", red_line1)
    cv2.imshow("avant", crop_img)

    #t += dt
    if mean_green > 70 and t > dt*10:
    	color_switch = True

    #print(color, mean_green)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#	t = 0
#	color_switch = False
#	color += 1


video_capture.release()
# out1.release()
cv2.destroyAllWindows()
