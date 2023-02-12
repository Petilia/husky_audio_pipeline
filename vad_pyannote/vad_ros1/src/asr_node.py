#!/usr/bin/env python3
import rospy
import numpy as np
from std_msgs.msg import Int16MultiArray, String
import soundfile as sf
import requests

# asr_host = rospy.get_param('~asr_host', '0.0.0.0')
# asr_port = rospy.get_param('~asr_port', '4009')

class ASR():
    def __init__(self):
        rospy.init_node('asr_node')
        
        self.sub_vad = rospy.Subscriber('segmentation', String, self.on_asr, queue_size=1)
        self.pub_asr = rospy.Publisher('asr', String, queue_size=10)
        
        asr_host = rospy.get_param('~asr_host', "10.147.18.193")
        asr_port = rospy.get_param('~asr_port', "4009")
        self.url = f"http://{asr_host}:{asr_port}/asr"
        print(self.url)
        
    def on_asr(self, ogg_path: String):
        files = {'file': open(ogg_path.data, 'rb')}
        r = requests.post(self.url, files=files)
        text = r.json()['transcript']
        asr_msg = String()
        asr_msg.data = text
        self.pub_asr.publish(asr_msg) 
        print(f"detected text :  {text}")
    
    
def main():
    node = ASR()
    rospy.spin()

if __name__ == '__main__':
    main()