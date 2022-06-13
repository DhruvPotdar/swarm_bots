#!usr/bin/env python
import rospy
import numpy as np
import math
from nav_msgs.msg import Odometry
from maze_solver.msg import Coords
from geometry_msgs.msg import Twist,Point
import time
import tf

x1 = float(input('enter goal_x: '))
y1 = float(input('enter goal_y: '))

del_time = 5

x_coord = 0
y_coord = 0
theta = 0

Loco = Twist()

def getOdom(msg):
    global x_coord
    global y_coord
    global theta

    x_coord = msg.pose.pose.position.x
    y_coord = msg.pose.pose.position.y
    theta_q = msg.pose.pose.orientation
    (roll,pitch,theta) = tf.transformations.euler_from_quaternion([theta_q.x,theta_q.y,theta_q.z,theta_q.w])
    #print(x_coord,y_coord,theta_q)

def euclidian(xi,yi,xf,yf):
    X = xf - xi
    Y = yf - yi

    return math.sqrt(X**2 + Y**2)

def manhattan(x1,x2):
    X = abs(x1 - x2)
    return X

def angular_adjustment():
    theta_err_pre = math.atan2(y1-y_coord,x1-x_coord) - theta
    int_adj = 0
    kp = 1
    kd = 0.3
    ki = 0.05

    while theta_err_pre > 0.00001:
        Loco.linear.x = 0
        theta_err = math.atan2(y1-y_coord,x1-x_coord) - theta
        diff_adj = (theta-theta_err_pre)/del_time
        int_adj += theta_err

        Loco.angular.z = min((kp*theta_err) + (kd*diff_adj) + (ki*int_adj),0.1)

        theta_err_pre = theta_err
        pub.publish(Loco)

    Loco.angular.z = 0
    pub.publish(Loco)
    print('angle = ',theta)

def linear_adjustment():
    kp = 1
    kd = 0.01
    ki = 0.5
    int_err = 0

    lin_err_pre = euclidian(x_coord,y_coord,x1,y1)
    while manhattan(x_coord,x1) > 0.01 and manhattan(y_coord,y1) > 0.01:
        lin_err = euclidian(x_coord,y_coord,x1,y1)
        diff_err = (lin_err - lin_err_pre)/del_time
        int_err += lin_err_pre
        Loco.linear.x = min((kp*lin_err + ki*int_err + kd*diff_err),0.1)
        pub.publish(Loco)
        lin_err_pre = lin_err

    Loco.linear.x = 0
    pub.publish(Loco)
    print("current co-ordinates are:",(x_coord,y_coord,theta))
    print("goal reached")

rospy.init_node('notActualController')
pub = rospy.Publisher('/cmd_vel',Twist,queue_size=5)
sub = rospy.Subscriber('/odom',Odometry,getOdom)
rate = rospy.Rate(1)

while not rospy.is_shutdown():
    sub = rospy.Subscriber('/odom',Odometry,getOdom)
    angular_adjustment()
    linear_adjustment()
    rate.sleep()