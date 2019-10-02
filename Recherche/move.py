import pypot.dynamixel
import const
from time import sleep
import numpy as np
import math

# forward_kinematics


def FK(linear_speed, angular_speed):
    speed_right = -(linear_speed + angular_speed *
                   const.robot_radius)/const.wheel_radius # rad/s
    speed_left = (linear_speed - angular_speed *
                  const.robot_radius)/const.wheel_radius # rad/s
    return speed_right*60/(2*math.pi), speed_left*60/(2*math.pi) # rpm


def rotate(motors, linear_speed, angular_speed):
    """ This function takes a linear and angular speed and moves the robot accordinglyself.
    Input
        x: linear speed in mm/s
        theta: angular speed in rad/s
    """
    speed_right, speed_left = FK(linear_speed, angular_speed)
    print(speed_left, speed_right)
    set_motors_speeds(motors, speed_left, speed_right)


def set_motors_speeds(motors, speed_left, speed_right):
    """
    motors: pyplot.dynamixel.DxlIO
    left_speed: rad/s
    """
    # motors.set_wheel_mode([left_motor_id, right_motor_id])
    motors.set_moving_speed(
        {const.left_motor_id: speed_left/const.rpm_correction, const.right_motor_id: speed_right/const.rpm_correction})


def set_motor_ids(motors, current_left_motor_id, current_right_motor_id):
    motors.change_id({current_left_motor_id: const.left_motor_id,
                      current_right_motor_id: const.right_motor_id})


def get_linear_angular_speed(position_x, position_y, position_theta, x_target, y_target):

    if (x_target < position_x):  # target left
        beta = math.pi
    else:  # target right
        beta = 0

    beta += math.atan2(y_target - position_y,
                       x_target - position_x)

    i = beta - position_theta

    if (i > math.pi):
        i -= 2*math.pi
    if (i > -2*math.pi):
        i += 2*math.pi

    angular_speed = i/const.delta_t

    linear_speed = math.sqrt((x_target - position_x)*(x_target-position_x) +
                             (y_target-position_y)*(y_target-position_y)) / const.delta_t

    return linear_speed, angular_speed


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
