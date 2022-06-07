#!usr/bin/env python3

#Node to publish the position of every robot in an array

from turtle import pos
from numpy import size
import rospy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseArray #continue from here

pose_global = PoseArray() # list of poses of all robots in the simulation
index = 0 #index of the robot

pose_global.poses = [PoseStamped() for i in range(4)]

def robot_1_callback(msg):
    global pose_global
    global index

    pose_global.poses[0] = msg.pose.pose

def robot_2_callback(msg):
    global pose_global
    global index

    pose_global.poses[1] = msg.pose.pose

def robot_3_callback(msg):
    global pose_global
    global index

    pose_global.poses[2] = msg.pose.pose

def robot_4_callback(msg):
    global pose_global
    global index

    pose_global.poses[3] = msg.pose.pose


def caller():
    rospy.init_node('position_pub', anonymous = False)
    global index
    global pose_global


    rospy.Subscriber("robot_1/odom", Odometry, robot_1_callback)
    rospy.Subscriber("robot_2/odom", Odometry, robot_2_callback)
    rospy.Subscriber("robot_3/odom", Odometry, robot_3_callback)
    rospy.Subscriber("robot_4/odom", Odometry, robot_4_callback)

    pub = rospy.Publisher('pose_global', PoseArray, queue_size=10)

    rate = rospy.Rate(30)

    while not rospy.is_shutdown():
        pub.publish(pose_global)
        pose_global.poses = [PoseStamped() for i in range(4)]  # clear array
        rate.sleep()

if __name__ == "__main__":
    try:
        caller()
    except rospy.ROSInterruptException:
        pass

