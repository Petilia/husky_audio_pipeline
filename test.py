import requests

tts_ogg_name = 'out.ogg'
text = "Привет дивный мир"
files = {'response': (None, text)}
response = requests.post('http://localhost:8008/tts', files=files)
with open(tts_ogg_name, 'wb') as f:
    f.write(response.content) 