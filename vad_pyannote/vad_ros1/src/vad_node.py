#!/usr/bin/env python3
import rospy
import numpy as np
from std_msgs.msg import Int16MultiArray, String
import soundfile as sf
import time
from pyannote.audio import Pipeline
from vad_tools import process_intervals, get_t_end, preds_from_buffer, get_asr


hf_token = "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"
pipeline = Pipeline.from_pretrained("pyannote/voice-activity-detection",
                                    use_auth_token=hf_token)
print("Pipeline loaded")

N_SECONDS = 1 # message size in second from topic
CHUNK = 1024
RATE = 16000
MODEL_INPUT_SECONDS = 5
TOLERANCE = 0.1
MODEL_INPUT_SAMPLES = MODEL_INPUT_SECONDS * RATE
MSG_SIZE = int(RATE / CHUNK * N_SECONDS) * CHUNK
TOPIC_INTERVAL = MSG_SIZE / RATE

buffer_size = RATE * MODEL_INPUT_SECONDS // MSG_SIZE + 1
time_bias_buffer = (buffer_size + 1) * MSG_SIZE / RATE - MODEL_INPUT_SECONDS
print(f"MSG_SIZE = {MSG_SIZE}")



class VAD():
    def __init__(self):
        rospy.init_node('vad_node')
        
        self.sub_image = rospy.Subscriber('audio', Int16MultiArray, self.on_audio, queue_size=1)
        self.pub_vad = rospy.Publisher('segmentation', String, queue_size=10)
        self.buffer = [np.zeros(MSG_SIZE, dtype="int16")] * buffer_size
        self.intervals = []
        self.interval_counter = 0
        
    def on_audio(self, int_array_msg: Int16MultiArray):
        cur_msg = np.array(int_array_msg.data, dtype =np.int16)
        # print(max(cur_msg), min(cur_msg))
        
        self.buffer += [cur_msg]
        output = preds_from_buffer(self.buffer, pipeline, MODEL_INPUT_SAMPLES, RATE)
        t_start, t_end = get_t_end(output)
        last_interval = [t_start, t_end]
        prev_buffer_len = (len(self.buffer) - 1) * (TOPIC_INTERVAL)
        
        t_interval, self.intervals, detected, self.interval_counter, mes = process_intervals(self.intervals, last_interval, 
                                                                                             self.interval_counter, prev_buffer_len, 
                                                                                             time_bias_buffer)
        self.interval_counter += TOPIC_INTERVAL
        
        print(mes)
        print("===================")
        
        print(len(self.buffer))
        
        if detected:
            # get_asr(buffer, t_interval)
            if t_interval[1] is not None:
                delta_t = t_interval[1] - t_interval[0]
                print(f"delta_t = {delta_t}")
                get_asr(self.buffer, t_interval, RATE)
            else:
                print(f"delta_t = None")
            
            self.buffer = self.buffer[-buffer_size:]
            self.interval_counter = 0
            
            
        
        # sf.write(f"/home/docker_current/catkin_ws/src/vad_ros1/py_files/listen_node_wavs/{int(time.time())}.wav", cur_msg, 16000)
        # print(cur_msg.shape, cur_msg.dtype)
        # rospy.loginfo(cur_msg.shape)
        

def main():
    node = VAD()
    rospy.spin()

if __name__ == '__main__':
    main()

        
        
