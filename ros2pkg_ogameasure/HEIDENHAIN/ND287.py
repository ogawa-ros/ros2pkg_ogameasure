#! /usr/bin/env python3
node_name = "HEIDENHAIN_ND287"

import rclpy
import ogameasure
import time
import sys
import threading
from std_msgs.msg import Float64
from std_msgs.msg import String

class ND287(object):
    def __init__(self):
        self.node = rclpy.create_node(node_name)

        self.node.declare_parameter("port") #いらない?
        az_port = self.node.get_parameter("~az_usbport").get_parameter_value().string_value
        el_port = self.node.get_parameter("~el_usbport").get_parameter_value().string_value
        #az_port = rospy.get_param("~az_usbport")
        #el_port = rospy.get_param("~el_usbport")

        self.encorder_az = ogameasure.HEIDENHAIN.ND287(az_port)
        self.encorder_el = ogameasure.HEIDENHAIN.ND287(el_port)

        topic_name_az = '/dev/'+node_name+'/'+az_port+'/'
        topic_name_az = topic_name.replace('_','/').replace('.','_')
        topic_name_el = '/dev/'+node_name+'/'+el_port+'/'
        topic_name_el = topic_name.replace('_','/').replace('.','_')

        #Publisher
        # self.pub_az = rospy.Publisher("/dev/ND287/__port__/az", Float64, queue_size=1)
        # self.pub_el = rospy.Publisher("/dev/ND287/__port__/el", Float64, queue_size=1)
        self.pub_az = rclpy.node.create_publisher(Float64, topic_name, 1)
        self.pub_el = rclpy.node.create_publisher(Float64, topic_name, 1)
        self.az = self.get_az()





    def get_az(self):
        _az = self.encorder_az.output_position_display_value()
        az = float(_az.strip(b"\x02\x00\r\n").decode())
        return az

    def get_el(self):
        _el = self.encorder_el.output_position_display_value()
        el = float(_el.strip(b"\x02\x00\r\n").decode())
        return el

    def publish_el(self):
        while not rospy.is_shutdown():
            el = self.get_el()
            self.pub_el.publish(float(el))
            time.sleep(0.01)
            continue

    def publish_az(self):
        count = 0
        while not rospy.is_shutdown():
            az = self.az
            az2  = self.get_az()
            hensa = az2-az
            if hensa > 100: #0->360
                count = count - 1
            elif hensa < -100: #360->0
                count = count + 1
            azaz = az2 + count*360
            self.pub_az.publish(float(azaz))
            #self.pub_az.publish(float(az2))
            self.az = az2
            time.sleep(0.01)
            continue

    def start_thread(self):
        th = threading.Thread(target = self.publish_az)
        th.setDaemon(True)
        th.start()
        check = threading.Thread(target = self.publish_el)
        check.setDaemon(True)
        check.start()


def main(args=None):
    rclpy.init(args=args)
    encorder  = ND287()
    rclpy.spin(encorder.node)

    encorder.node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()



# if __name__ == '__main__':
#     rospy.init_node(node)
#     encorder = ND287()
#     encorder.start_thread()
#     rospy.spin()
