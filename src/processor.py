#!usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseArray
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Point
import sys

pose_global = PoseArray() # list of poses of all robots in the simulation
index = 0 #index of the current robot

pose_local = PoseArray() # list of poses of all robots that the current robot is able to sense

def pose_global_callback(msg):
    global pose_global
    global index
    pose_global = msg
    

def caller():
    global index
    global pose_global
    global pose_local

    rospy.init_node('robot_{}/processor'.format(index), anonymous = False)

    rospy.Subscriber("/pose_global", PoseArray, pose_global_callback)
    
    

    
