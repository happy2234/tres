#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import time
import math

def move_turtle():
    rospy.init_node('move_rectangle_node', anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(100)  # High loop rate for smooth control (100 Hz)
    vel_msg = Twist()

    # Set linear and angular velocities for precise movement
    vel_msg.linear.x = 0.1  # Slow linear velocity for precise straight movement
    vel_msg.angular.z = 0.0  # Initially no angular velocity (straight line)

    # Define the dimensions of the rectangle
    length = 4.0  # Length of the rectangle in arbitrary units
    breadth = 2.0  # Breadth of the rectangle in arbitrary units

    rospy.loginfo("Starting to move the turtle in a rectangular path...")

    # Move in a rectangular path by repeating the sequence of moves and turns
    for _ in range(2):  # Complete 2 sides of the rectangle (repeat path)
        rospy.loginfo("Moving straight for length...")
        move_straight(velocity_publisher, vel_msg, length)  # Move straight for length
        rospy.loginfo("Turning 90 degrees...")
        turn(velocity_publisher, 90)  # Turn 90 degrees (clockwise)
        
        rospy.loginfo("Moving straight for breadth...")
        move_straight(velocity_publisher, vel_msg, breadth)  # Move straight for breadth
        rospy.loginfo("Turning 90 degrees...")
        turn(velocity_publisher, 90)  # Turn 90 degrees (clockwise)

    rospy.loginfo("Rectangle completed. Stopping the turtle.")
    vel_msg.linear.x = 0.0  # Stop forward movement
    vel_msg.angular.z = 0.0  # Stop turning
    velocity_publisher.publish(vel_msg)

def move_straight(velocity_publisher, vel_msg, distance):
    """
    Move the turtle in a straight line for the specified distance.
    This function uses precise timing to ensure the turtle moves exactly the required distance.
    """
    travel_time = distance / vel_msg.linear.x  # Time required to cover the distance
    rospy.loginfo(f"Moving straight for distance: {distance} units (Time: {travel_time}s)")

    start_time = rospy.Time.now().to_sec()

    while rospy.Time.now().to_sec() - start_time < travel_time:
        velocity_publisher.publish(vel_msg)  # Publish the velocity command
        rospy.Rate(100).sleep()  # Sleep at 100 Hz for precise control

    rospy.loginfo(f"Moved straight for {distance} units")

def turn(velocity_publisher, angle):
    """
    Turn the turtle by a specified angle (in degrees).
    Uses time-based control to turn precisely by the specified angle.
    """
    vel_msg = Twist()
    vel_msg.angular.z = 0.5  # Set angular velocity for turning

    radians = math.radians(angle)  # Convert angle from degrees to radians

    rospy.loginfo(f"Turning by {angle} degrees ({radians} radians)")

    # Time to turn by the specified angle using the set angular velocity
    turn_time = radians / abs(vel_msg.angular.z)

    start_time = rospy.Time.now().to_sec()

    while rospy.Time.now().to_sec() - start_time < turn_time:
        velocity_publisher.publish(vel_msg)  # Publish the velocity command
        rospy.Rate(100).sleep()  # Sleep at 100 Hz for precise control

    rospy.loginfo(f"Turned by {angle} degrees")

if __name__ == '__main__':
    try:
        move_turtle()  # Call the function to move the turtle
    except rospy.ROSInterruptException:
        pass
