import pyaudio
import wave
import os
import soundfile as sf

def get_device_index(device_name="Plantronics"):

    p = pyaudio.PyAudio()

    for i in range(p.get_device_count()):
        if device_name in p.get_device_info_by_index(i)['name']:
            index_device = i
            
    p.terminate()

    return index_device

def play_audio(filename, output_device_index, chunk=1024, 
                        device_channels=1, device_rate=48000):

    p = pyaudio.PyAudio()
    
    filename_wav = filename[0:-4] + ".wav"
    if os.path.isfile(filename_wav):
        os.remove(filename_wav)
    
    
    os.system(f"ffmpeg -i {filename} -ar 48000 {filename_wav}")
    
    wf = wave.open(filename_wav, 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(
        format = p.get_format_from_width(wf.getsampwidth()),
        channels = device_channels,
        rate = device_rate,
        output_device_index=output_device_index,
        output = True
        )
  
    data = wf.readframes(chunk)
    while data != b'':
        stream.write(data)
        data = wf.readframes(chunk)

    stream.close()
    p.terminate()