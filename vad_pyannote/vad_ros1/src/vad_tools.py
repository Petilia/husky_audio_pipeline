import numpy as np
import torch
import time
import soundfile as sf

def get_t_end(output):
    t_start = t_end = None
    for speech in output.get_timeline().support():
        t_start, t_end = speech.start, speech.end
    return t_start, t_end

    
def preds_from_buffer(buffer, pipeline, MODEL_INPUT_SAMPLES, RATE):
    data = np.hstack((buffer))[-MODEL_INPUT_SAMPLES:]
    mapping = {"waveform" : torch.Tensor(data).unsqueeze(0), "sample_rate": RATE}
    output =  pipeline(mapping)
    return output

def process_intervals(previous_intervals, last_interval, interval_counter, prev_buffer_len, time_bias_buffer, thre=0.4):
    
    detected = False
    
    # if (last_interval[0] is None) & (len(previous_intervals) == 0):
    if (len(previous_intervals) == 0) & ((last_interval[0] is None) | (( last_interval[1] + time_bias_buffer <= prev_buffer_len) if (last_interval[1] is not None) else False)):
        # Если в пришедшем интервале ничего не задетекчено и в предыдущих ничего тоже нет, 
        # то весь буффер не содержит информации, поэтому его надо будет обновить
        t_start = t_end = None
        intervals = previous_intervals
        detected = True
        interval_counter = 0
        
        mes = "1 - Пустой новый интервал и пустые прошлые"
        return [t_start, t_end], intervals, detected, interval_counter, mes
    
    if last_interval[0] is not None:
        # Если пришедший интервал не пустой, то добавляем к его значениям смещение interval_counter
        last_interval[0] += interval_counter
        last_interval[1] += interval_counter
        
    if (last_interval[0] is not None) & (len(previous_intervals) == 0):
        # Если пришедший интервал не пустой, а в предыдущем ничего не было - просто добавляем пришедший интервал
        t_start, t_end = last_interval
        intervals = previous_intervals + [[t_start, t_end]] 
        t_start += time_bias_buffer
        t_end += time_bias_buffer
        detected = False
        
        mes = "2 - непустой пришедщий интервал и пустые прошлые"
        return [t_start, t_end], intervals, detected, interval_counter, mes
    
    # Расстояние между началом пришедшего интервала и максимальным значением конца из предыдущих интервалов
    # print(last_interval[0], np.array(previous_intervals)[:, 1].max())
    
    if last_interval[0] is not None:
        distance = last_interval[0] - np.array(previous_intervals)[:, 1].max() 
    else:
        distance = 0
  
    print(last_interval[0], last_interval[1])
    # Если дистанция больше заданного значения, значит наблюдаемый интервал закончился и начался новый интервал
    # Если интервал пустой, или он никак не расширяет наши знания - значит активность установлена
    # Если нет- значит он расширяет наш текущий интервал 
    if (distance > thre): 
        # t_start - минимальное значение конца из предыдущих отрезков, t_end - максимальное из них
        t_start, t_end = np.array(previous_intervals)[:, 0].min(), np.array(previous_intervals)[:, 1].max()
        t_start += time_bias_buffer
        t_end += time_bias_buffer
        # В intervals тогда остается только пришедший отрезок
        intervals = [[last_interval[0] - interval_counter, last_interval[1] - interval_counter]]
        detected = True
        interval_counter = 0 
        mes = "3 - Окончание текущего интервала и детектирование нового"
        return [t_start, t_end], intervals, detected, interval_counter, mes
    # elif (last_interval[0] is None) | ((last_interval[1] is not None) & (last_interval[1] + time_bias_buffer <= prev_buffer_len)):
    elif (last_interval[0] is None) | (( last_interval[1] + time_bias_buffer <= prev_buffer_len) if (last_interval[1] is not None) else 0):
        t_start, t_end = np.array(previous_intervals)[:, 0].min(), np.array(previous_intervals)[:, 1].max()
        t_start += time_bias_buffer
        t_end += time_bias_buffer
        intervals = []
        detected = True
        interval_counter = 0 
        mes = "4 - Окончание текущего интервала, после которого ничего нет"
        return [t_start, t_end], intervals, detected, interval_counter, mes
    else:
        intervals = previous_intervals + [last_interval]
        t_start, t_end = np.array(intervals)[:, 0].min(), np.array(intervals)[:, 1].max()
        t_start += time_bias_buffer
        t_end += time_bias_buffer
        mes = "5 - Дополнение интервала"
        return [t_start, t_end], intervals, detected, interval_counter, mes

def get_asr(buffer, t_interval, RATE):
    start_timestamp = int(t_interval[0] * RATE)
    end_timestamp = int(t_interval[1] * RATE)
    
    data = np.hstack((buffer))
    sf.write(f"/home/docker_current/catkin_ws/src/vad_ros1/py_files/listen_node_wavs/{int(time.time())}.wav", 
             data[start_timestamp:end_timestamp], RATE)
    
