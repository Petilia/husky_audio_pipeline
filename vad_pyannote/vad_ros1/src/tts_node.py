#!/usr/bin/env python3
import rospy
import numpy as np
from std_msgs.msg import Int16MultiArray, String
import soundfile as sf
import requests
from pyaudio_tools import get_device_index, play_audio
import time
import uuid
import pymongo

client = pymongo.MongoClient("mongodb://0.0.0.0:27018/")
db = client["audio_annotation_db"]
annotations = db["annotations"]

# INPUT_DEVICE_INDEX = 12
# time.sleep(1)
uniq_dream_id = str(uuid.uuid4())
print(uniq_dream_id)
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
        
        self.previous_audio_end = 0

        
        
    def on_tts(self, asr_msg: String):
        asr_result = asr_msg.data
        
        #Отправка в Dream
        dream_request = {"user_id": uniq_dream_id, "payload": asr_result}
        r = requests.post(url=self.dream_agent_url, json=dream_request)
        dream_response = r.json()["response"]
        print(f"Запрос в Dream: {asr_result}")
        print(f"Ответ Dream: {dream_response}")
        
        # # #Отправка в сервис tts
        files = {'response': (None, dream_response)}
        response = requests.post(self.url, files=files)
        with open(tts_ogg_name, 'wb') as f:
            f.write(response.content) 
            
        print("before play")
        play_audio(tts_ogg_name, INPUT_DEVICE_INDEX)    
        print("after play")
        
        #Отправка в  Mongo
        annotation = { "asr_result": asr_result, 
                      "dream_response": dream_response
                            }
        t0 = time.perf_counter()
        annotations.insert_one(annotation)
        dt = t0 = time.perf_counter() - t0
        print("database latency = ", dt)
        
        
def main():
    node = TTS()
    rospy.spin()

if __name__ == '__main__':
    main()