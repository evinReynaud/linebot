import math
import const1 as const
import pypot.dynamixel
import time
import numpy as np

# last version
class Goto(object):

    def __init__(self):
        self.x_target = const.x_target
        self.y_target = const.y_target
        self.theta_target = const.theta_target
        self.delta_x = 0
        self.delta_y = 0
        self.delta_theta = 0
        self.position_x = 0
        self.position_y = 0
        self.position_theta = 0
        self.linear_speed = 0
        self.angular_speed = 0
        self.delta_t = const.delta_t
        self.distance = 1000
        self.avance = True
        self._turn = False
        self.motors = pypot.dynamixel.DxlIO(
            pypot.dynamixel.get_available_ports()[0])

    def DK(self, speed_rigth, speed_left):
        vr = -const.wheel_radius*speed_rigth
        vl = const.wheel_radius*speed_left
        linear_speed = (vl+vr)/2
        angular_speed = (vr-vl)/(2*const.robot_radius)
        return linear_speed, angular_speed

    def odom(self, linear_speed, angular_speed, delta_t):
        self.delta_theta = angular_speed * delta_t
        self.delta_x = linear_speed * delta_t * math.cos(self.position_theta)
        self.delta_y = linear_speed * delta_t * math.sin(self.position_theta)

    def tick_odom(self, delta_x, delta_y, delta_theta):
        self.position_x = self.position_x + delta_x
        self.position_y = self.position_y + delta_y
        self.position_theta = self.position_theta + delta_theta

    def reset(self):
        self.position_x = 0
        self.position_y = 0
        self.position_theta = 0
        self.linear_speed = 0
        self.angular_speed = 0
        self.delta_x = 0
        self.delta_y = 0
        self.delta_theta = 0

    def get_i(self, position_x, position_y, position_theta, x_target, y_target):
        print("************ GET i *****************")
        beta = math.atan2(y_target - position_y,
                          x_target - position_x)
        i = beta - position_theta

        if (i > math.pi):
            i -= 2*math.pi
        elif (i < -math.pi):
            i += 2*math.pi
        print(i)
        return i

    def get_linear_angular_speed(self, position_x, position_y, position_theta, x_target, y_target):

        i = self.get_i(position_x, position_y,
                       position_theta, x_target, y_target)

        angular_speed = i*const.angular_speed_correction
        if angular_speed > const.angular_speed_max:
            angular_speed = const.angular_speed_max
        self.distance = math.sqrt(
            (x_target - position_x)*(x_target - position_x)+(y_target-position_y)*(y_target-position_y))
        linear_speed = self.distance*const.linear_speed_correction
        if linear_speed > const.linear_speed_max:
            linear_speed = const.linear_speed_max
        self.linear_speed = linear_speed
        self.angular_speed = angular_speed

    def FK(self, linear_speed, angular_speed):
        speed_right = (linear_speed + angular_speed *
                       const.robot_radius)/const.wheel_radius  # rad/s
        speed_left = (linear_speed - angular_speed *
                      const.robot_radius)/const.wheel_radius  # rad/s
        return -speed_right*60/(2*math.pi), speed_left*60/(2*math.pi)  # rpm

    def rotate(self, linear_speed, angular_speed):
        """ This function takes a linear and angular speed and moves the robot accordinglyself.
        Input
            x: linear speed in m/s
            theta: angular speed in rad/s
        """
        self.motors.set_wheel_mode([const.left_motor_id, const.right_motor_id])
        speed_right, speed_left = self.FK(linear_speed, angular_speed)
        #print(speed_left, speed_right)
        self.set_motors_speeds(self.motors, speed_left, speed_right)

    def set_motors_speeds(self, motors, speed_left, speed_right):
        """
        motors: pyplot.dynamixel.DxlIO
        left_speed: rad/s
        """
        motors.set_moving_speed(
            {const.left_motor_id: speed_left/const.rpm_correction, const.right_motor_id: speed_right/const.rpm_correction})

    def stop(self):
        self.rotate(0, 0)
        #self.motors.set_joint_mode([const.left_motor_id, const.right_motor_id])

    def turn(self, i):
        #self.motors.set_wheel_mode([const.left_motor_id, const.right_motor_id])
        t = time.time()
        self.linear_speed = 0
        self.delta_theta = 0
        self._turn = True

        while self._turn:
            print("turn")
            if time.time()-t > self.delta_t:
                print(time.time() - t)
                t = time.time()
                i = i-self.delta_theta
                print(i)
                if (abs(i) < 0.03):
                    self._turn = False
                    print("================= arret   TURN ===============")
                    self.stop()
                else:
                    self.angular_speed = i*const.angular_speed_correction
                    if self.angular_speed > const.angular_speed_max:
                        self.angular_speed = const.angular_speed_max
                        print("speed and max")
                    if self.angular_speed < const.angular_speed_min:
                        self.angular_speed = const.angular_speed_min
                        print("speed and min")

                    self.rotate(self.linear_speed, self.angular_speed)
                    self.odom(self.linear_speed,
                              self.angular_speed, self.delta_t)
                    self.tick_odom(self.delta_x, self.delta_y,
                                   self.delta_theta)

        self.stop()

    def run(self):

        t = time.time()
        i = self.get_i(self.position_x, self.position_y,
                       self.position_theta, self.x_target, self.y_target)
        self.turn(i)
        while self.avance:
            # print("run")
            if time.time()-t > self.delta_t:
                t = time.time()
                self.get_linear_angular_speed(
                    self.position_x, self.position_y, self.position_theta, self.x_target, self.y_target)
                #speed_right,speed_left = self.FK(self.linear_speed,self.angular_speed)
                self.rotate(self.linear_speed, self.angular_speed)
                self.odom(self.linear_speed, self.angular_speed, self.delta_t)
                # self.odom3(speed_right/const.rpm_correction,speed_left/const.rpm_correction,const.delta_t)
                self.tick_odom(self.delta_x, self.delta_y, self.delta_theta)
                print("************ distance **************")
                print(self.distance)
                if (self.distance < 0.005):
                    self.avance = False
                    self.stop()
                    print("================= arret   GO ===============")
        self.stop()
        i = const.theta_target - self.position_theta
        if (i > math.pi):
            i -= 2*math.pi
        elif (i < -math.pi):
            i += 2*math.pi
        if (abs(i) > 0.03):
            self.turn(i)
        self.stop()


if __name__ == '__main__':
    goto = Goto()
    print("*************** START *********************")
    goto.run()
