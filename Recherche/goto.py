import math
import const
import pypot.dynamixel
from time import sleep
import numpy as np


class Goto(object):

    def __init__(self):
        self.x_target = const.x_target
        self.y_target = const.y_target
        self.theta_target = const.theta_target
        self.position_x = 0
        self.position_y = 0
        self.position_theta = 0
        self.linear_speed = 0
        self.angular_speed = 0
        self.delta_x=0
        self.delta_y=0
        self.delta_theta=0
        self.delta_t = const.delta_t
        self.distance=1000
        self.avance = True

    def DK(self, speed_rigth, speed_left):
        linear_speed = const.wheel_radius*(speed_rigth+speed_left)/2
        angular_speed = const.wheel_radius * \
            (speed_left-speed_left)/(2*const.robot_radius)
        return linear_speed, angular_speed

    def odom(self, linear_speed, angular_speed, delta_t):
        delta_theta = angular_speed * delta_t
        delta_x = linear_speed * delta_t * math.cos(delta_theta)
        delta_y = linear_speed * delta_t * math.sin(delta_theta)
        self.delta_x=delta_x
        self.delta_y= delta_y
        self.delta_theta=delta_theta
        return delta_x, delta_y, delta_theta

    def reset(self):
        self.position_x = 0
        self.position_y = 0
        self.position_theta = 0
        self.linear_speed = 0
        self.angular_speed = 0
        self.delta_x=0
        self.delta_y=0
        self.delta_theta=0

    def tick_odom(self, delta_x, delta_y, delta_theta):
        self.position_x = self.position_x + delta_x
        self.position_y = self.position_y + delta_y
        self.position_theta = self.position_theta + delta_theta

    def get_linear_angular_speed(self, position_x, position_y, position_theta, x_target, y_target):

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
        self.distance=math.sqrt((x_target - position_x)*(x_target-position_x) +
                                 (y_target-position_y)*(y_target-position_y))
        linear_speed = self.distance / const.delta_t

        self.linear_speed = linear_speed
        self.angular_speed = angular_speed

        return linear_speed, angular_speed

    def FK(self,linear_speed, angular_speed):
        speed_right = (linear_speed + angular_speed *
                       const.robot_radius)/const.wheel_radius  # rad/s
        speed_left = (linear_speed - angular_speed *
                      const.robot_radius)/const.wheel_radius  # rad/s
        return speed_right*60/(2*math.pi), speed_left*60/(2*math.pi)  # rpm

    def rotate(self,motors, linear_speed, angular_speed):
        """ This function takes a linear and angular speed and moves the robot accordinglyself.
        Input
            x: linear speed in mm/s
            theta: angular speed in rad/s
        """
        speed_right, speed_left = self.FK(linear_speed, angular_speed)
        print(speed_left, speed_right)
        self.set_motors_speeds(motors, speed_left, -speed_right)


    def set_motors_speeds(self,motors, speed_left, speed_right):
        """
        motors: pyplot.dynamixel.DxlIO
        left_speed: rad/s
        """
        # motors.set_wheel_mode([left_motor_id, right_motor_id])
        motors.set_moving_speed(
            {const.left_motor_id: speed_left/const.rpm_correction, const.right_motor_id: speed_right/const.rpm_correction})


    def stop(self):
        port = "/dev/ttyACM0"
        dxl_io = pypot.dynamixel.DxlIO(port)
        self.rotate(dxl_io, 0, 0)
        dxl_io.set_joint_mode([const.left_motor_id, const.right_motor_id])

    def run(self):

        while self.avance:
            self.get_linear_angular_speed(
                self.position_x, self.position_y, self.position_theta, self.x_target, self.y_target)
            self.rotate(self.linear_speed, self.angular_speed)
            self.odom(self.linear_speed, self.angular_speed, self.delta_t)
            self.tick_odom(self.delta_x, self.delta_y, self.delta_theta)
            if (self.distance < 0.1):
                self.avance =False
        self.stop()


if __name__ == '__main__':

    goto = Goto()
    goto.run()
