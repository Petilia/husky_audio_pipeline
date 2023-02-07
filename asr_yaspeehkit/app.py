from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse, JSONResponse, Response, FileResponse
import os
import uvicorn
from dotenv import load_dotenv
from base64 import b64encode
from speechkit_api import asr_from_yandex_speeckit, tts_from_yandex_speechkit

app = FastAPI()
load_dotenv()
FOLDER_ID = os.getenv('FOLDER_ID')
API_KEY = os.getenv('API_KEY')

@app.get("/")
async def homepage():
    return JSONResponse({'hello': 'world'})


@app.post("/asr")
def infer_asr(file: UploadFile = File(None)) -> JSONResponse:
    # ASR example:
    """
    ```Bash
        curl -X POST "http://localhost:4008/asr" -F 'file=@path/to/your/file.ogg'
    ```
    
    ```Python
    url = "http://localhost:4008/asr"
    files = {'file': open(tts_ogg_name, 'rb')}
    r = requests.post(url, files=files)
    r.text
    ```
    """
    
    transcript = asr_from_yandex_speeckit(FOLDER_ID, API_KEY, file.file)
    print(transcript)

    return JSONResponse(content={"transcript":transcript})


@app.post("/tts")
async def infer_tts(response: str = Form(...)) -> StreamingResponse:
    # TTS example:
    """
    ```Bash
        curl -X POST "http://localhost:8008/tts" -F "response='Меня зовут Саша'"  --output out.ogg
    ```
    
    ```Python
    tts_ogg_name = '/home/appuser/tts_result.ogg'
    text = "Привет дивный мир"
    files = {'response': (None, text)}
    response = requests.post('http://localhost:8008/tts', files=files)
    with open(tts_ogg_name, 'wb') as f:
        f.write(response.content) 
    ```
    
    """
    print(response)
    audio_response = tts_from_yandex_speechkit(response, FOLDER_ID, API_KEY)
    
    return StreamingResponse(audio_response, media_type="audio/oggopus")


if __name__ == "__main__":
    uvicorn.run("app:app", port=4008, reload=True)