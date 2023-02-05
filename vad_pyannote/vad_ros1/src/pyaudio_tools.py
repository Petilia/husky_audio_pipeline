import pyaudio

def get_device_index(device_name="Plantronics"):

    p = pyaudio.PyAudio()

    for i in range(p.get_device_count()):
        if device_name in p.get_device_info_by_index(i)['name']:
            index_device = i

    return index_device