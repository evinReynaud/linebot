import pypot.dynamixel
from time import sleep

def rotate(motors, x, theta):
    """ This function takes a linear and angular speed and moves the robot accordinglyself.
    Input
        x: linear speed in mm/s
        theta: angular speed in rad/s
    """
    left_speed = (x + theta*robot_radius)/wheel_radius
    right_speed = (x - theta*robot_radius)/wheel_radius
    print(left_speed, right_speed)
    set_motors_speeds(motors, left_speed, right_speed)

def set_motors_speeds(motors, left_speed, right_speed):
    """
    motors: pyplot.dynamixel.DxlIO
    left_speed: rad/s
    """
    #motors.set_wheel_mode([left_motor_id, right_motor_id])
    motors.set_moving_speed({left_motor_id:left_speed/rpm_correction, right_motor_id:right_speed/rpm_correction})

def set_motor_ids(motors, current_left_motor_id, current_right_motor_id):
    motors.change_id({current_left_motor_id:left_motor_id, current_right_motor_id:right_motor_id})

def test(x=500, t=2):
    port = "/dev/ttyACM0"
    dxl_io = pypot.dynamixel.DxlIO(port)
    dxl_io.set_wheel_mode([left_motor_id, right_motor_id])
    print("right")
    rotate(dxl_io, x, t)
    sleep(3)
    print("left")
    rotate(dxl_io, x, -t)
    sleep(3)
    print("stop")
    rotate(dxl_io, 0, 0)
    dxl_io.set_joint_mode([left_motor_id, right_motor_id])

def stop():
    port = "/dev/ttyACM0"
    dxl_io = pypot.dynamixel.DxlIO(port)
    rotate(dxl_io, 0, 0)
    dxl_io.set_joint_mode([left_motor_id, right_motor_id])

def find_left():
    port = "/dev/ttyACM0"
    dxl_io = pypot.dynamixel.DxlIO(port)
    dxl_io.set_wheel_mode([left_motor_id])
    dxl_io.set_moving_speed({left_motor_id:20})
