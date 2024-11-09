import base64
import os
from io import BytesIO

from flask import jsonify
import google.generativeai as genai
import pytesseract
from dotenv import load_dotenv
from PIL import Image, ImageOps
import typing_extensions as typing
from enum import Enum
import json

load_dotenv()

genai.configure(api_key=os.getenv("gemini"))

model = genai.GenerativeModel("gemini-1.5-flash")

class EatTime(Enum):
    BEFORE = "Before"
    AFTER = "After"

class Time(Enum):
    MORNING = "Morning"
    AFTERNOON = "Afternoon"
    EVENING = "Evening"
    NIGHT = "Night"

class med(typing.TypedDict):
    name: str
    Time: list[Time]
    eat: EatTime
    note: str

def do_ocr(b64image):
    image = Image.open(BytesIO(base64.b64decode(b64image)))

    
    gray_image = ImageOps.grayscale(image)

    scale_factor = 2
    resized_image = gray_image.resize(
        (gray_image.width * scale_factor, gray_image.height * scale_factor),
        resample=Image.LANCZOS
    )

    improved_text = pytesseract.image_to_string(resized_image)

    print(improved_text)

    return improved_text
    # resized_image.save('preprocessed_image.jpg')

def post_process(text: str) -> med:
    result = model.generate_content(
    ["I'll give you an OCR of a medicine prescription, your return json schema will be used to set reminders. Make sure to include any other info in notes",text],
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=list[med]
    ),)

    print(result.text)
    med_data = json.loads(result.text)

    merged_med_data = {}
    for entry in med_data:
        name = entry['name']
        if name in merged_med_data:
            merged_med_data[name]['Time'].extend(entry['Time'])
        else:
            merged_med_data[name] = entry

    med_data = list(merged_med_data.values())

    return med_data