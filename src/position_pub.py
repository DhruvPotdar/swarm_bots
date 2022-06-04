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

def callback(msg):
    # print("Odometry")
    # print(msg)
    global pose_global
    global index

    pose_global.poses.append(msg.pose.pose)
    # pose_global.poses[index-1].header.frame_id = index
    # pose_global[index - 1]  = index
    # print(pose_global[index -1])

def caller():
    rospy.init_node('position_pub', anonymous = False)
    global index
    global pose_global
    for j in range(1,4):
        index = j
        print(index)
        rospy.Subscriber("robot_{}/odom".format(index), Odometry, callback)

    pub = rospy.Publisher('pose_global', PoseArray, queue_size=10)

    rate = rospy.Rate(30)
    while not rospy.is_shutdown():
        pub.publish(pose_global)

        pose_global = PoseArray() # clear array
        # print("Pose")
        # print(pose)
        rate.sleep()

if __name__ == "__main__":
    try:
        caller()
    except rospy.ROSInterruptException:
        pass

