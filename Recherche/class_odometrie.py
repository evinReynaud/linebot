import const.py as const
import math


class odometrie():
    def __init__(self):
        # x y yheta in the world landmark in meter
        self.position_x = 0
        self.position_y = 0
        self.theta = 0
        self.delta_t = const.delta_t

    # direct kinematics
    # speed_right and left in rad/s

    def DK(self, speed_rigth, speed_left):
        linear_speed = const.wheel_radius*(speed_rigth+speed_left)/2
        angular_speed = const.wheel_radius * \
            (speed_left-speed_left)/(2*const.robot_radius)
        return linear_speed, angular_speed

    # def odom(self,linear_speed,angular_speed):
    #    distance_wheel_rigth = linear_speed - angular_speed*robot_radius
    #    distance_wheel_left = linear_speed + angular_speed*robot_radius
    #    distance_wheel_mean = (distance_wheel_rigth + distance_wheel_left)/2
    #    distance_theta = (distance_wheel_rigth - distance_wheel_left)/(2*const.robot_radius)
    #    delta_x = distance_wheel_mean*cos(angular_speed+distance_theta/2)
    #    delta_y = distance_wheel_mean*sin(angular_speed+distance_theta/2)
    #    return delta_x, delta_y,delta_theta

    def odom(self, linear_speed, angular_speed, delta_t):
        delta_theta = angular_speed * delta_t
        delta_x = linear_speed * delta_t * math.cos(delta_theta)
        delta_y = linear_speed * delta_t * math.sin(delta_theta)
        return delta_x, delta_y, delta_theta

    def reset(self):
        self.position_x = 0
        self.position_y = 0
        self.theta = 0

    def tick_odom(self, delta_x, delta_y, delta_theta):
        self.position_x = self.position_x + delta_x
        self.position_y = self.position_y + delta_y
        self.theta = self.theta + delta_theta

    def get_position(self):
        print("Le robot est en position ")
        print(self.position_x)
        print(self.position_y)
        print(self.theta)
