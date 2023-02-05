#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int16MultiArray

import pyaudio
from pyaudio_tools import get_device_index
import numpy as np

N_SECONDS = 1 # В топики будут публиковаться соообщения длиной в столько секунд (каждые столько секунд соответственно)
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
TIMEOUT_LENGTH = 1
INPUT_DEVICE_INDEX = get_device_index() # индекс устройства с которого будет идти запись звука 

real_n_seconds = int(RATE / CHUNK * N_SECONDS) * CHUNK / RATE
print(f"real n seconds = {real_n_seconds}")

class ListenNode():
    def __init__(self) -> None:
        rospy.init_node('audio_listener_node')
       
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                frames_per_buffer=CHUNK,
                input_device_index=INPUT_DEVICE_INDEX, 
                input=True)
        
        self.publisher = rospy.Publisher('audio', Int16MultiArray, queue_size=10)
        
    def publish(self):
        while not rospy.is_shutdown():
            frames = []
            for i in range(0, int(RATE / CHUNK * N_SECONDS)):
                data = self.stream.read(CHUNK, exception_on_overflow = False)
                frames.append(data)
                
            msg = Int16MultiArray()
            msg.data = list(np.frombuffer(b''.join(frames), dtype=np.int16))
            self.publisher.publish(msg)
            rospy.loginfo(len(msg.data))
            
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        rospy.loginfo('stream closed')
            
            
if __name__ == '__main__':
    try:
        listener = ListenNode()
        listener.publish()
    except rospy.ROSInterruptException: pass