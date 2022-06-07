#!usr/bin/env python3

from turtle import pos
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseArray
from geometry_msgs.msg import PoseStamped


pose_global = PoseArray() # list of poses of all robots in the simulation
index = 1 #index of the current robot

pose_local = PoseArray() # list of poses of all robots that the current robot is able to sense

def pose_global_callback(msg):
    global pose_global
    global index
    pose_global = msg
    

def processor():
    global index
    global pose_global
    global pose_local

    rospy.init_node('processor', anonymous = False) #namespaces not allowed in node definitions

    rospy.Subscriber("/pose_global", PoseArray, pose_global_callback)

    for i in range(len(pose_global.poses)):
        if pose_global.poses[index] != pose_global.poses[i] and pose_global.poses[index] - pose_global.poses[i] < 0.5:
            pose_local.poses.append(pose_global.poses[i])

    pub_odom = rospy.Publisher('robot_{}/odom'.format(index), Odometry, queue_size=10)
    rate = rospy.Rate(30)

    while not rospy.is_shutdown():
        pub_odom.publish(pose_local)
        pose_local = PoseArray() # reset pose array to update to new pose after every iteration
        rate.sleep()


if __name__ == "__main__":
    try:
        processor()
    except rospy.ROSInterruptException:
        pass
    
    

    
