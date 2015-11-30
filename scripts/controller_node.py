#!/usr/bin/env python

import rospy
from robotics_project.msg import objectPose
from robotics_project.srv import *
from code import interact
from math import copysign

class ControllerNode():
    def __init__(self):
        rospy.init_node('controller_node')
        self.drive_request = rospy.ServiceProxy('requestDrive', requestDrive)
        self.angle_request = rospy.ServiceProxy('requestAngle', requestAngle)
        self.pose_subscriber = rospy.Subscriber(
                "/camera_node/objectPose",
                objectPose,
                self.handle_incoming_pose
        )
        rospy.sleep(5)
        print "playing soccer"
        self.play_soccer()
        rospy.spin()

    def handle_incoming_pose(self, objectPose):
        self.objectPose = objectPose

    def get_object_in_view(self, object_in_view):
        while not object_in_view: 
            self.drive_robot(0, 50)
            rospy.sleep(0.1)
        rospy.sleep(0.5)
        print "ball is in view"
        self.drive_robot(0, 0)

    def center_object(self, object_center):
        offset = object_center - 320
        while abs(offset) > 20:
            offset = object_center - 320
            print offset
            #turn_rate = copysign(1.0, offset)*50
            turn_rate = max([offset/(320/50), 25])
            print turn_rate
            self.drive_robot(0, turn_rate)
        print "centered ball, sending stop command"
        self.drive_robot(0, 0)

    def get_turn_angle(self):

    def play_soccer(self):
        #find the ball
        print "Finding ball..."
        self.get_object_in_view(self.objectPose.ball_in_view)
        print "Ball in view, centering..."
        self.center_object(self.objectPose.ball_center_x)
        print "Ball found."
        #find the angle between the ball and the goal
        print "Zeroing angle measurement..."
        angle = self.get_turn_angle()
        print "Angle zeroed, finding goal..."
        self.get_object_in_view(self.objectPose.goal_in_view)
        print "Goal in view, centering..."
        self.center_object(self.objectPose.goal_center_x)
        print "Goal found."
        angle = self.get_turn_angle()
        print "Angle between ball and goal: ", angle

        #put the ball between the robot and the goal

        #push the ball into the goal

    def drive_robot(self, velocity, rotation):
        rospy.wait_for_service('requestDrive')
        try:
            self.drive_request(velocity, rotation)
        except rospy.ServiceException, e:
            print e

    def request_angle(self):
        rospy.wait_for_service('requestAngle')
        try:
            angle = self.angle_request()
        except rospy.ServiceException, e:
            print e
        return angle

    def build_model(self, objectPose):
        """Calculate world coordinates of ball and goal, robot is (0,0)"""
        if objectPose.ball_in_view:
            ball_distance = objectPose.ball_distance
            ball_offset = objectPose.ball_center_x
            ball_coords = calculate_object_coords(ball_distance, ball_offset)
        if objectPose.goal_in_view:
            goal_distance = objectPose.goal_distance
            goal_offset = objectPose.goal_center_x
            goal_coords = calculate_object_coords(goal_distance, goal_offset)

    def calculate_object_coords(self, distance, offset): 
        pass

if __name__ == "__main__":
    controller_node = ControllerNode()
