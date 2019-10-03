import math
# Robot settings

# Robot radius in meter
robot_radius = 0.04

# Wheel radius in meter
wheel_radius = 0.026

# Rpm Correction in rpm
rpm_correction = 1.339

# Internal motor IDs
left_motor_id = 2
right_motor_id = 1

# Time stamp
delta_t = 0.05

# target
x_target = 0.5
y_target = 0.8
theta_target = math.pi/2

# Correction Coefficient of linear_speed
linear_speed_correction = 5

# Correction Coefficient of angular_speed

angular_speed_correction = 0.3

# Linear_speed_max

linear_speed_max = 500

# Angular_speed_max 

angular_speed_max = math.pi/3
