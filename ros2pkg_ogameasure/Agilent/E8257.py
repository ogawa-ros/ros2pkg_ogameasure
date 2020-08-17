#! /usr/bin/env python3

node_name = "Agilent_e8257d"

import rclpy
import ogameasure
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32

class E8257d(object):
    def __init__(self):
        self.node = rclpy.create_node(node_name)
        self.power = None
        self.freq = None
        self.onoff = None

        #declare&get parameter
        self.node.declare_parameter("host")
        self.node.declare_parameter("port")
        host = self.node.get_parameter("host").get_parameter_value().string_value
        port = self.node.get_parameter("port").get_parameter_value().string_value
        com = ogameasure.ethernet(host, int(port))
        self.sg = ogameasure.Agilent.E8257D(com)
            
        topic_name = '/'+node_name+'/'+host+'/'
        topic_name = topic_name.replace('_','/').replace('.','_')

        #publisher
        self.pub_freq = rclpy.node.create_publisher(Float64, topic_name+'freq', 1)
        self.pub_power = rclpy.node.create_publisher(Float64, topic_name+'power', 1)
        self.pub_onoff = rclpy.node.create_publisher(Int32, topic_name+'onoff', 1)

        #subscriber
        self.node.create_subscription(Float64,topic_name+'freq_cmd',self.set_freq,1)
        self.node.create_subscription(Float64,topic_name+'power_cmd',self.set_power,1)
        self.node.create_subscription(Float64,topic_name+'onoff_cmd',self.set_onoff,1)
        self.node.create_subscription(Float64,topic_name+'refresh',self.refresh,1) 

        #initialize
        self.refresh()


    def set_freq(self,q):
        if self.freq != q.data:
            self.sg.freq_set(q.data)
            time.sleep(0.001)
            pass
        
        self.query_freq()
        return

    def set_power(self,q):
        if self.power != q.data:
            self.sg.power_set(q.data)
            time.sleep(0.001)
            pass
        
        self.query_power()
        return

    def set_onooff(self,q):
        if self.onoff != q.data:
            self.sg.onoff_set(q.data)
            time.sleep(0.001)
            pass
        
        self.query_onoff()
        return

    def query_freq(self):
        self.freq = self.sg.freq_query()
        self.pub_freq.publish(self.freq)
        return

    def query_power(self):
        self.power = self.sg.power_query()
        self.pub_power.publish(self.power)
        return

    def query_onoff(self):
        self.onoff = self.sg.output_query()
        self.pub_onoff.publish(self.onoff)
        return

    def refresh(self):
        self.query_freq()
        self.query_power()
        self.query_onoff()
        return

def main(args=None):
    rclpy.init(args=args)
    sg  = E8257d()
    rclpy.spin(sg.node)
    
    sg.node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
