#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

print("Pipeline")
from pyannote.audio import Pipeline
print("Pipeline")



def create_random_image():
    rospy.init_node('ASR_node')
    pub_asr = rospy.Publisher('asr_result', String, queue_size=10)

    while not rospy.is_shutdown():
        msg = String()
        msg.data = "hello world"
        print(msg.data)
        pub_asr.publish(msg)

        # pub_asr.publish("hello world")
      


if __name__ == '__main__':
    try:
        create_random_image()
    except rospy.ROSInterruptException: pass
