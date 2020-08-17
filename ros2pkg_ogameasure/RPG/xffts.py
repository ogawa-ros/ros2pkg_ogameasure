#!/usr/bin/env python3

node_name = "RPG_XFFTS"

import rclpy
import xfftspy
import numpy
from std_msgs.msg import Float64
from std_msgs.msg import Float64MultiArray
class XFFTS(object):
    def __init__(self):
        self.node = rclpy.create_node(node_name)

        timer_period = 0.1
        topic_name = '/dev/'+node_name+'/'
        topic_name = topic_name.replace('_','/')

        #publisher
        pub_spec = {}
        pu_tp = {}
        xffts.clear_buffer()
        d = xffts.receive_once()

        for bnum in range(header['BE_num']):
            self.pub_spec[bnum] = rclpy.node.create_publisher(Float64MultiArray, topic_name+'board{0:02d}/spec''.format(bnum), 1)
            self.pub_tp[bnum] = rclpy.node.create_publisher(Float64, topic_name+'board{0:02d}/tp''.format(bnum), 1)

        xffts.clear_buffer() #いる？
        self.create_timer(timer_period, self.publish)

        def publish(self):
            spec = Float64MultiArray()
            tp = Float64()

            d = xffts.receive_once()
            for bnum in d['data']:
                spec.data = d['data'][bnum]
                tp.data = numpy.sum(d['data'][bnum])
                pub_spec[bnum].publish(spec)
                pub_tp[bnum].publish(tp)

def main(args=None):
    rclpy.init(args=args)
    xffts = XFFTS()
    rclpy.spin(xffts.node)

    sg.node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
