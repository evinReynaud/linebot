import pypot.dynamixel
import const.py as const
from time import sleep
import numpy as np
import math

# forward_kinematics


def FK(linear_speed, angular_speed):
    speed_right = (linear_speed + angular_speed *
                   const.robot_radius)/const.wheel_radius
    speed_left = (linear_speed - angular_speed *
                  const.robot_radius)/const.wheel_radius
    return speed_right, speed_left  # rad/s


def rotate(motors, x, theta):
    """ This function takes a linear and angular speed and moves the robot accordinglyself.
    Input
        x: linear speed in mm/s
        theta: angular speed in rad/s
    """
    left_speed = (x + theta*const.robot_radius)/const.wheel_radius
    right_speed = (x - theta*const.robot_radius)/const.wheel_radius
    print(left_speed, right_speed)
    set_motors_speeds(motors, left_speed, right_speed)


def set_motors_speeds(motors, left_speed, right_speed):
    """
    motors: pyplot.dynamixel.DxlIO
    left_speed: rad/s
    """
    # motors.set_wheel_mode([left_motor_id, right_motor_id])
    motors.set_moving_speed(
        {const.left_motor_id: left_speed/const.rpm_correction, const.right_motor_id: right_speed/const.rpm_correction})


def set_motor_ids(motors, current_left_motor_id, current_right_motor_id):
    motors.change_id({current_left_motor_id: const.left_motor_id,
                      current_right_motor_id: const.right_motor_id})


def get_angle_dist_target(position_x, position_y, position_theta, x_target, y_target, x_theta):

    if(position_y > y_target)  # see if target is at my right or my left
    {
        signe = 1  # right
    }
    else
    {
        signe = -1  # left
    }

    angle = signe * math.atan2(x_target-position_x, y_target-position_y)

    dist_cible = math.sqrt((x_target - position_x)*(x_target-position_x) +
                           (y_target-position_y)*(y_target-position_y))

    return angle, dist_cible


def test(x=500, t=2):
    port = "/dev/ttyACM0"
    dxl_io = pypot.dynamixel.DxlIO(port)
    dxl_io.set_wheel_mode([const.left_motor_id, const.right_motor_id])
    print("right")
    rotate(dxl_io, x, t)
    sleep(3)
    print("left")
    rotate(dxl_io, x, -t)
    sleep(3)
    print("stop")
    rotate(dxl_io, 0, 0)
    dxl_io.set_joint_mode([const.left_motor_id, const.right_motor_id])


def stop():
    port = "/dev/ttyACM0"
    dxl_io = pypot.dynamixel.DxlIO(port)
    rotate(dxl_io, 0, 0)
    dxl_io.set_joint_mode([const.left_motor_id, const.right_motor_id])


def find_left():
    port = "/dev/ttyACM0"
    dxl_io = pypot.dynamixel.DxlIO(port)
    dxl_io.set_wheel_mode([const.left_motor_id])
    dxl_io.set_moving_speed({const.left_motor_id: 20})
