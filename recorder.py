import subprocess
import time
import pygame

import rospy
from sensor_msgs.msg import Joy

topics = ['/visual_odom', '/lidar_odom']

class Recorder:
    def __init__(self, topics):
        self.topics = topics
        self.process = None
        self.recording = False
        # sound notification init
        pygame.mixer.init()
        self.record_sound = pygame.mixer.Sound("sounds/record.mp3")
        self.stop_sound = pygame.mixer.Sound("sounds/stop.mp3")

    def record():
        if not self.recording:
            self.process = subprocess.Popen(['rosbag', 'record'] + self.topics, cwd='bags')
            self.recording = True
            self.record_sound.play()
            
        
    def stop():
        if self.recording:
            self.process.terminate()
            self.recording = False
            self.stop_sound.play()
        

def joy_callback(msg):
    global recorder
    share_button = msg.buttons[8]
    options_button = msg.buttons[9]
    if share_button:
        recorder.record()
    elif options_button:
        recorder.stop()


if __name__ == "__main__":
    recorder = Recorder(topics=topics)
    rospy.init_node("rosbag_recorder", anonymous=True)
    rospy.Subscriber("/joy_teleop/joy", Joy, joy_callback)
    rospy.spin()

