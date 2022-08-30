#!/usr/bin/env python3
import rospy  
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, sqrt, atan2

class TurtleBot:

    def __init__(turtle):

        #Creates a mode
        rospy.init_node('turtlebot_controller', anonymous=True)

        #Publisher
        turtle.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel',Twist, queue_size=10)

        #Subscriber
        turtle.pose_subscriber = rospy.Subscriber('/turtle1/pose',Pose, turtle.Update_Pose)

        turtle.pose = Pose()
        turtle.rate = rospy.Rate(10)
        #turtle.goal_x = 0
        #turtle.goal_y = 0

    #Function used when a new message of type "Pose" is received by the subscriber    
    def Update_Pose(turtle, data):
        turtle.pose = data
        turtle.pose.x = round(turtle.pose.x, 4)
        turtle.pose.y = round(turtle.pose.y, 4)

    #Function used to calculate distance between current pose and goal pose
    def Euclidean_Distance(turtle):
        return sqrt(pow((turtle.goal_x - turtle.pose.x), 2) 
                  + pow((turtle.goal_y - turtle.pose.y), 2))

    #Function used to calculate linear velocity (in x)  
    def Linear_Velocity(turtle):
        rospy.set_param ("beta" , 1.5)
        Beta = rospy.get_param ("beta")
        return Beta * turtle.Euclidean_Distance()

    #Function used to calculate steering angle
    def Steering_Angle(turtle):
        return atan2(turtle.goal_y - turtle.pose.y, turtle.goal_x - turtle.pose.x)

    #Function used to calculate angular velocity (in z)
    def Angular_Velocity(turtle):
        rospy.set_param ("phai" , 6)
        Phai = rospy.get_param ("phai")
        return Phai * (turtle.Steering_Angle() - turtle.pose.theta)

    #Function used to move the turtle to its goal
    def Move_To_Goal(turtle):
        goal_pose = Pose()
        #rospy.set_param ("X_GOAL" , 10)
        #turtle.goal_x = rospy.get_param ("/X_GOAL")
        #rospy.set_param ("Y_GOAL" , 10)
        #turtle.goal_y = rospy.get_param ("/Y_GOAL")
        turtle.goal_x = float(input("Set your X_Goal: "))
        turtle.goal_y = float(input("Set your Y_Goal: "))

        vel_msg = Twist()

        while turtle.Euclidean_Distance() >= 0.01:

            #Linear Velocity in X-axis
            vel_msg.linear.x = turtle.Linear_Velocity()
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0

            #Angular Velocity in Z-axis
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = turtle.Angular_Velocity()

            turtle.velocity_publisher.publish(vel_msg)

            turtle.rate.sleep()
        
        #The turtle must be stopped after reaching its goal
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        turtle.velocity_publisher.publish(vel_msg)

if __name__ == "__main__":
    try: 
        x = TurtleBot ()
        x.Move_To_Goal ()
    except rospy.ROSInterruptException:
        pass