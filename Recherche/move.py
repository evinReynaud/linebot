import pypot.dynamixel

def rotate(motors, x, theta):
    """ This function takes a linear and angular speed and moves the robot accordinglyself.
    Input
        x: linear speed in mm/s
        theta: angular speed in rad/s
    """
    left_speed = (x + theta*robot_radius)/wheel_radius
    right_speed = (x + theta*robot_radius)/wheel_radius

    set_motors_speeds(motors, left_motor_id, left_speed)

def set_motors_speeds(motors, left_speed, right_speed):
    """
    motors: pyplot.dynamixel.DxlIO
    left_speed: rad/s
    """
    motors.set_wheel_mode([left_motor_id, right_motor_id])
    motors.set_moving_speed({left_motor_id:left_speed/rpm_correction, right_motor_id:right_speed/rpm_correction})

def set_motor_ids(motors, current_left_motor_id, current_right_motor_id):
    motors.change_id({current_left_motor_id:left_motor_id, current_right_motor_id:right_motor_id})

def test():
    port = "/dev/ttyACM0"
    dxl_io = pypot.dynamixel.DxlIO(port)
    dxl_io.set_wheel_mode([left_motor_id, right_motor_id])
    rotate(dxl_io, 100, 1)
    sleep(3)
    rotate(dxl_io, 100, 1)
    sleep(3)
    rotate(dxl_io, 0, 0)
    dxl_io.set_joint_mode([left_motor_id, right_motor_id])
