#!/usr/bin/env python3
import rospy
import numpy as np
from std_msgs.msg import Int16MultiArray
import soundfile as sf
import time

N_SECONDS = 1 # message size in second from topic
CHUNK = 1024
RATE = 16000
MODEL_INPUT_SECONDS = 5
TOLERANCE = 0.1
MODEL_INPUT_SAMPLES = MODEL_INPUT_SECONDS * RATE
MSG_SIZE = int(RATE / CHUNK * N_SECONDS) * CHUNK
TOPIC_INTERVAL = MSG_SIZE / RATE

class VAD():
    def __init__(self):
        rospy.init_node('save_audio_node')
        
        self.sub_image = rospy.Subscriber('audio', Int16MultiArray, self.on_audio, queue_size=10)
        self.buffer = []
   
    def on_audio(self, int_array_msg: Int16MultiArray):
        cur_msg = np.array(int_array_msg.data, dtype =np.int16)
       
        self.buffer += [cur_msg]
        print(len(self.buffer))



if __name__ == '__main__':
    try:
        vad = VAD()
        rospy.spin()
    except rospy.ROSInterruptException: pass
    finally:
        data = np.hstack((vad.buffer))
        sf.write(f"/home/docker_current/catkin_ws/src/vad_ros1/py_files/listen_node_wavs/{int(time.time())}.wav", 
                data, RATE)
