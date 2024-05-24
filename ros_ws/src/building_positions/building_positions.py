#!/usr/bin/env python
import time
import os
import socket

import rospy
import tf2_ros

from std_msgs.msg import String
from sensor_msgs.msg import Joy

from AbstractVirtualCapability import AbstractVirtualCapability, VirtualCapabilityServer, formatPrint
from ViconPosition import ViconPosition

tfBuffer = None
listener = None


def get_position(vicon_name):
	try:
		"""
		world_str = rospy.get_param('~world')
		position_str = rospy.get_param('~position')
		map_str = rospy.get_param('~map')
		"""

		current = tfBuffer.lookup_transform('world', vicon_name, rospy.Time(0), rospy.Duration(1.0))
		return [current.transform.translation.x, current.transform.translation.y, current.transform.translation.z]
	except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as error:
		rospy.logwarn(error)
		return [100,100,100] #[repr(error).replace("\"", "").replace("\'", "")]


if __name__ == '__main__':
	try:
		# starts the node
		rospy.init_node('building_positions')
		rate = rospy.Rate(25)

		tfBuffer = tf2_ros.Buffer()
		listener = tf2_ros.TransformListener(tfBuffer)

		server = VirtualCapabilityServer(int(rospy.get_param('~semantix_port')), "0.0.0.0")
		kobuki = ViconPosition(server)

		kobuki.functionality["GetViconPosition"] = get_position

		kobuki.start()
		rospy.loginfo("ROS node started successfully")

		while not rospy.is_shutdown() and server.running:
			rate.sleep()
	except KeyError as e:
	        rospy.logerr("Environment variable missing: %s", e)
	except Exception as e:
	        rospy.logerr("Unhandled exception: %s", e)
