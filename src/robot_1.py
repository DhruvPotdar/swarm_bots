#!usr/bin/env python3

#Node to handle everything related to robot 1

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

odom = None
def callback(msg):
    # print("Odometry")
    # print(msg)
    odom = msg

def move():
    rospy.init_node('robot_1', anonymous = False)
    pub = rospy.Publisher('robot_1/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(30) # 30Hz to sync with the rate of publishing of the odom topic
    
    vel_msg = Twist()
    vel_msg.linear.x = 0.1

    # rospy.Subscriber("robot_1/odom", Odometry, callback)

    while not rospy.is_shutdown():
        pub.publish(vel_msg)

        print("Velocity")
        print(vel_msg)
        
        rate.sleep()
    
if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException:
        pass



