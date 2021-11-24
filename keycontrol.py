from pynput import keyboard


import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32, Int32MultiArray, Float32MultiArray


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("robot_name", help="add your robot name, (ex)smartmbot_xx",
                    type=str)
args = parser.parse_args()
print(args.robot_name)
robot_name = args.robot_name

rclpy.init()
key_node = rclpy.create_node('pphs_cam_views')
key_node.pub_smartmbot_writing_dc_motor_vel = key_node.create_publisher(Float32MultiArray, '/'+robot_name+'/writing_dc_motor_vel', 10)

target_speed = 80


def on_press(key):    
    input_key_str = format(key)

    if input_key_str == 'Key.up':
        (vL_pwm, vR_pwm) = (target_speed, target_speed)
    elif input_key_str == 'Key.down':
        (vL_pwm, vR_pwm) = (-target_speed, -target_speed)
    elif input_key_str == 'Key.left':
        (vL_pwm, vR_pwm) = (0, target_speed)
    elif input_key_str == 'Key.right':
        (vL_pwm, vR_pwm) = (target_speed, 0)
    else:
        (vL_pwm, vR_pwm) = (0, 0)

    msg = Float32MultiArray()        
    msg.data = [float(vL_pwm), float(vR_pwm)] # PWM: []
    key_node.pub_smartmbot_writing_dc_motor_vel.publish(msg)

def on_release(key):
    msg = Float32MultiArray()        
    msg.data = [float(0), float(0)] # PWM: []
    key_node.pub_smartmbot_writing_dc_motor_vel.publish(msg)

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()



