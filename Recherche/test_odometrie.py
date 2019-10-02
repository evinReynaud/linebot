import class_odometrie as co


port = "/dev/ttyACM0"
dxl_io = pypot.dynamixel.DxlIO(port)
dxl_io.set_wheel_mode([left_motor_id, right_motor_id])
