#!/usr/bin/env python3
import rospy
import numpy as np
from std_msgs.msg import Int16MultiArray, String
import soundfile as sf
import requests
from pyaudio_tools import get_device_index, play_audio
import time

# INPUT_DEVICE_INDEX = 12
# time.sleep(1)
INPUT_DEVICE_INDEX = get_device_index() 
tts_ogg_name = '/home/docker_current/catkin_ws/src/vad_ros1/py_files/records/tts_result.ogg'

class TTS():
    def __init__(self):
        rospy.init_node('tts_node')
        self.sub_vad = rospy.Subscriber('asr', String, self.on_tts, queue_size=1)
        
        tts_host = rospy.get_param('~tts_host', '0.0.0.0')
        tts_port = rospy.get_param('~tts_port', '4008')
        dream_host = rospy.get_param('~dream_host', '0.0.0.0')

        self.url = f"http://{tts_host}:{tts_port}/tts"
        self.dream_agent_url = f"http://{dream_host}:4242"

        
        
    def on_tts(self, asr_msg: String):
        text = asr_msg.data
        print(text, type(text))
    
        #Отправка в Dream
        dream_request = {"user_id": "xyz1", "payload": text}
        r = requests.post(url=self.dream_agent_url, json=dream_request)
        dream_response = r.json()["response"]
        print(dream_response)
        
        #Отправка в сервис tts
        files = {'response': (None, dream_response)}
        response = requests.post(self.url, files=files)
        with open(tts_ogg_name, 'wb') as f:
            f.write(response.content) 
            
        print("before play")
        play_audio(tts_ogg_name, INPUT_DEVICE_INDEX)    
        print("after play")
        
        
def main():
    node = TTS()
    rospy.spin()

if __name__ == '__main__':
    main()