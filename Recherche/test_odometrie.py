import class_odometrie as co
import pypot.dynamixel
import const.py as const
import numpy


ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit('No port')

dxl_io = pypot.dynamixel.DxlIO(ports[0])
dxl_io.set_joint_mode([const.left_motor_id, const.right_motor_id])

odom = co.odometrie()
t=0
while(true)
  if(t == fmod(const.delta_t,10))
    dxl_io.get_moving_speed({1})
    dxl_io.get_moving_speed({2})
  t += const.delta_x
  aa
