#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

def move_turtle():
    # Initialize the ROS node
    rospy.init_node('move_turtle_node', anonymous=True)
    
    # Create a publisher to send velocity commands to the turtle
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    
    # Define the rate at which the loop will run (10 Hz)
    rate = rospy.Rate(10)
    
    # Create a Twist message to set linear and angular velocity
    vel_msg = Twist()
    
    # Set linear velocity in the x direction (forward motion)
    vel_msg.linear.x = 0.0  # Adjust the speed as needed
    vel_msg.linear.y = 1.0
    vel_msg.linear.z = 0.0
    
    # Set angular velocity to zero (no rotation)
    vel_msg.angular.x = 0.0
    vel_msg.angular.y = 0.0
    vel_msg.angular.z = 0.0
    
    rospy.loginfo("Moving the turtle in a straight line...")
    
    # Keep publishing the velocity message until the node is shut down
    while not rospy.is_shutdown():
        # Publish the velocity message
        velocity_publisher.publish(vel_msg)
        
        # Sleep for the specified rate (10 Hz)
        rate.sleep()

if __name__ == '__main__':
    try:
        # Call the function to move the turtle
        move_turtle()
    except rospy.ROSInterruptException:
        pass
