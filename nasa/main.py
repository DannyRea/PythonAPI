from config import settings
import json
import requests
from starlette.responses import StreamingResponse
from io import BytesIO
import os
nasa_api_key = settings.settings.NASA_OPEN_API_KEY


def get_apod():
    print(nasa_api_key)
    print("here in funct")

    r = requests.get(
        "https://api.nasa.gov/planetary/apod?api_key={}".format(nasa_api_key), stream=True)

    io = BytesIO()

    url = json.loads(r.text)['url']
    image = requests.get(url)
    file_name = url.split('/')[-1]

    with open(file_name, 'wb') as f:
        io.write(image.content)
    os.unlink(file_name)
    io.seek(0)
    return StreamingResponse(io, media_type="image/jpg")
