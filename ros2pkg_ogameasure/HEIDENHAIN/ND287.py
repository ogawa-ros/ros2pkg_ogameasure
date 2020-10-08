#! /usr/bin/env python3
node_name = "HEIDENHAIN_ND287"

import rclpy
import ogameasure
import time
import sys
import random
from std_msgs.msg import Float64
from std_msgs.msg import String

class ND287(object):
    def __init__(self):
        self.node = rclpy.create_node(node_name)

        self.node.declare_parameter("~az_usbport")
        self.node.declare_parameter("~el_usbport")
        az_port = self.node.get_parameter("~az_usbport").get_parameter_value().string_value
        el_port = self.node.get_parameter("~el_usbport").get_parameter_value().string_value

        self.encorder_az = ogameasure.HEIDENHAIN.ND287(az_port)
        self.encorder_el = ogameasure.HEIDENHAIN.ND287(el_port)

        topic_name_az = '/dev/'+node_name+az_port
        topic_name_az = topic_name_az.replace('_','/').replace('.','_')
        topic_name_el = '/dev/'+node_name+el_port
        topic_name_el = topic_name_el.replace('_','/').replace('.','_')

        self.pub_az = self.node.create_publisher(Float64, topic_name_az, 1)
        self.pub_el = self.node.create_publisher(Float64, topic_name_el, 1)
        self.az = self.get_az()
#       self.az = self.get_az_simu()

        #ループ(スレッドの代わり)
        self.node.create_timer(0.01,self.publish_az)
        self.node.create_timer(0.01,self.publish_el)



    def get_az(self):
        _az = self.encorder_az.output_position_display_value()
        az = float(_az.strip(b"\x02\x00\r\n").decode())
        return az

    def get_el(self):
        _el = self.encorder_el.output_position_display_value()
        el = float(_el.strip(b"\x02\x00\r\n").decode())
        return el


    def get_az_simu(self):
        az = 180+random.random()
        return az

    def get_el_simu(self):
        el = 45+random.random()
        return el



    
    def publish_el(self):
        el = self.get_el()
#        el = self.get_el_simu()
        msg = Float64()
        msg.data = float(el)
        self.pub_el.publish(msg)
        

    def publish_az(self):
        count = 0
        az = self.az
        az2  = self.get_az()
 #       az2  = self.get_az_simu()
        hensa = az2-az
        if hensa > 100: #0->360
            count = count - 1
        elif hensa < -100: #360->0
            count = count + 1
        azaz = az2 + count*360
        msg = Float64()
        msg.data = float(azaz)
        self.pub_az.publish(msg)
        self.az = az2



def main(args=None):
    rclpy.init(args=args)
    encorder  = ND287()
    rclpy.spin(encorder.node)
    encorder.node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

