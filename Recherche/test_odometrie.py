import class_odometrie.py as co
import pypot.dynamixel
import time
import const.py as const
import numpy
import math


ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit('No port')

dxl_io = pypot.dynamixel.DxlIO(ports[0])
dxl_io.set_joint_mode([const.left_motor_id, const.right_motor_id])

odom = co.odometrie()
t = time.time()
while(True):
    if time.time() - t > const.delta_t:
        t = time.time()
        rpm_r = dxl_io.get_moving_speed({1})
        rpm_l = dxl_io.get_moving_speed({2})
        print rpm_r # right
        print rpm_l # left

        wr= rpm_r*2*math.pi/60 ## ??
        wl= rpm_l*2*math.pi/60 ##

        linear_speed, angular_speed = odom.DK(wr, wl)
        print linear_speed
        print angular_speed





