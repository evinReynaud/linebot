import math
import const
import pypot.dynamixel
import class_odometrie
import time
import numpy as np

odom = class_odometrie.odometrie()
class Goto(object):

    def __init__(self):
        self.x_target = const.x_target
        self.y_target = const.y_target
        self.theta_target = const.theta_target
        self.position_x = 0
        self.position_y = 0
        self.theta = 0
        self.linear_speed = 0
        self.angular_speed = 0
        self.delta_t = const.delta_t
        self.distance = 1000
        self.avance = True
        self.motors = pypot.dynamixel.DxlIO(pypot.dynamixel.get_available_ports()[0])
    def reset(self):
        self.position_x = 0
        self.position_y = 0
        self.theta = 0
        self.linear_speed = 0
        self.angular_speed = 0
        self.delta_x = 0
        self.delta_y = 0
        self.delta_theta = 0

    def get_linear_angular_speed(self, position_x, position_y, theta, x_target, y_target):

        if (x_target < position_x):  # target left
            beta = math.pi
        else:  # target right
            beta = 0

        beta += math.atan2(y_target - position_y,
                           x_target - position_x)
        beta = beta % (2*math.pi)
        i = beta - theta

        if (i > math.pi):
            i -= 2*math.pi
        elif (i < -math.pi):
            i += 2*math.pi

        angular_speed = i*const.angular_correction
        if angular_speed > const.angular_speed_max:
            angular_speed = const.angular_speed_max
        self.distance = math.sqrt((x_target - position_x)*(x_target - position_x)+(y_target-position_y)*(y_target-position_y))
        linear_speed = self.distance*const.linear_correction
        if linear_speed > const.linear_speed_max:
            linear_speed = const.linear_speed_max
        self.linear_speed = linear_speed
        self.angular_speed = angular_speed

        return linear_speed, angular_speed

    def FK(self, linear_speed, angular_speed):
        speed_right = (linear_speed + angular_speed *const.robot_radius)/const.wheel_radius  # rad/s
        speed_left = (linear_speed - angular_speed *const.robot_radius)/const.wheel_radius  # rad/s
        return speed_right*60/(2*math.pi), speed_left*60/(2*math.pi)  # rpm

    def rotate(self, motors, linear_speed, angular_speed):
        """ This function takes a linear and angular speed and moves the robot accordinglyself.
        Input
            x: linear speed in m/s
            theta: angular speed in rad/s
        """
        speed_right, speed_left = self.FK(linear_speed, angular_speed)
        print(speed_left, speed_right)
        self.set_motors_speeds(motors, speed_left, -speed_right)

    def set_motors_speeds(self, motors, speed_left, speed_right):
        """
        motors: pyplot.dynamixel.DxlIO
        left_speed: rad/s
        """
        # motors.set_wheel_mode([left_motor_id, right_motor_id])
        motors.set_moving_speed(
            {const.left_motor_id: speed_left/const.rpm_correction, const.right_motor_id: speed_right/const.rpm_correction})

    def stop(self):
        self.rotate(self.motors, 0, 0)
        self.motors.set_joint_mode([const.left_motor_id, const.right_motor_id])

    def run(self):
        seft.motors.set_wheel_mode([const.left_motor_id,const.right_motor_id])
        t = time.time()
        while self.avance:
            if time.time()-t > self.delta_t:
                t = time.time()
                self.get_linear_angular_speed(self.position_x, self.position_y, self.theta, self.x_target, self.y_target)
                self.rotate(self.linear_speed, self.angular_speed)
                delta_x, delta_y,delta_theta = odom.odom(self.linear_speed, self.angular_speed, self.delta_t)
                odom.tick_odom(delta_x,delta_y,delta_theta)
                print(self.distance)
            if (self.distance < 0.01):
                self.avance = False
        self.stop()
if __name__ == '__main__':
    goto = Goto()
    goto.run()
