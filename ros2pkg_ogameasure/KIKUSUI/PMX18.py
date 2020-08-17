#! /usr/bin/env python3

node_name = "KIKUSUI_pmx18"

import rclpy
import ogameasure
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32

class PMX18_2A(object):
    def __init__(self):
        self.node = rclpy.create_node(node_name)
        self.volt = None
        self.curr = None
        self.onoff = None

        #declare&get parameter
        self.node.declare_parameter("host")
        self.node.declare_parameter("port")
        host = self.node.get_parameter("host").get_parameter_value().string_value
        port = self.node.get_parameter("port").get_parameter_value().string_value
        com = ogameasure.ethernet(host, int(port))
        self.ps = ogameasure.KIKUSUI.PMX18_2A(com)

        topic_name = '/dev/'+node_name+'/'+host+'/'
        topic_name = topic_name.replace('_','/').replace('.','_')

        #publisher
        self.pub_volt = rclpy.node.create_publisher(Float64, topic_name+'vol', 1)
        self.pub_curr = rclpy.node.create_publisher(Float64, topic_name+'cur', 1)
        self.pub_onoff = rclpy.node.create_publisher(Int32, topic_name+'onoff', 1)

        #subscriber
        self.node.create_subscription(Float64,topic_name+'vol_cmd',self.set_volt,1)
        self.node.create_subscription(Float64,topic_name+'cur_cmd',self.set_curr,1)
        self.node.create_subscription(Int32,topic_name+'onoff_cmd',self.set_onoff,1)
        self.node.create_subscription(Float64,topic_name+'refresh',self.refresh,1)

        #initialize
        self.refresh()


    def set_volt(self,q):
        if self.volt != q.data:
            self.ps.volt_set(q.data)
            time.sleep(0.001)
            pass

        self.query_volt()
        return

    def set_curr(self,q):
        if self.curr != q.data:
            self.ps.current_set(q.data)
            time.sleep(0.001)
            pass

        self.query_curr()
        return

    def set_onooff(self,q):
        if self.onoff != q.data:
            if q.data == 1:
                self.ps.set_ON()
            else:
                self.set_OFF()
            time.sleep(0.001)
            pass

        self.query_onoff()
        return

    def query_volt(self):
        self.volt = self.ps.query_volt()
        self.pub_volt.publish(self.volt)
        return

    def query_curr(self):
        self.curr = self.ps.query_curr()
        self.pub_curr.publish(self.curr)
        return

    def query_onoff(self):
        self.onoff = self.ps.query_output_onoff()
        self.pub_onoff.publish(self.onoff)
        return

    def refresh(self):
        self.query_volt()
        self.query_curr()
        self.query_onoff()
        return

def main(args=None):
    rclpy.init(args=args)
    ps  = PMX18_2A()
    rclpy.spin(ps.node)

    sg.node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
