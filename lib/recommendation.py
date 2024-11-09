import google.generativeai as genai
import random
from typing import List, TypedDict
from dotenv import load_dotenv
import os
import json

load_dotenv()

genai.configure(api_key=os.getenv("gemini"))

model = genai.GenerativeModel("gemini-1.5-flash")


class Doctor(TypedDict):
    id: int
    userId: str
    phoneNumber: str
    aadharNumber: str
    mbbsId: str
    specialty: str
    verified: bool
    blockId: str
    appointments: list
    Prescription: list
    user: dict


# Fetch doctor data from database
def fetch_doctors_from_database() -> List[Doctor]:
    return [
        {
            "id": 1,
            "userId": "user123",
            "phoneNumber": "1234567890",
            "aadharNumber": "123456789012",
            "mbbsId": "MBBS123",
            "specialty": "Orthopedic",
            "verified": True,
            "blockId": "block1",
            "appointments": [],
            "Prescription": [],
            "user": {
                "id": 1,
                "name": "Dr. Robert Smith",
                "email": "dr.robertsmith@example.com",
            },
        },
        {
            "id": 2,
            "userId": "user456",
            "phoneNumber": "9876543210",
            "aadharNumber": "987654321012",
            "mbbsId": "MBBS456",
            "specialty": "Neurosurgeon",
            "verified": True,
            "blockId": "block2",
            "appointments": [],
            "Prescription": [],
            "user": {
                "id": 2,
                "name": "Dr. Jane Doe",
                "email": "dr.janedoe@example.com",
            },
        },
        {
            "id": 3,
            "userId": "user789",
            "phoneNumber": "5551234567",
            "aadharNumber": "555123456789",
            "mbbsId": "MBBS789",
            "specialty": "Orthopedic",
            "verified": True,
            "blockId": "block3",
            "appointments": [],
            "Prescription": [],
            "user": {
                "id": 3,
                "name": "Dr. John Brown",
                "email": "dr.johnbrown@example.com",
            },
        },
    ]


def get_doctors_by_specialty(specialty: str, doctors: List[Doctor]) -> List[Doctor]:
    specialty = specialty.lower() 
    return [doctor for doctor in doctors if specialty in doctor["specialty"].lower()]


def generate_prompt(problem: str) -> str:
    return f"""
    A patient is experiencing the following problem: {problem}
    Suggest the type of doctor they should visit and recommend some doctors by name from that specialty.
    """


def post_process(text: str):
    result = model.generate_content(
        text,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json"
        ),
    )
    
    print(result.text)  

    
    try:
        med_data = json.loads(result.text)  
        return med_data
    except json.JSONDecodeError:
        return {"error": "Failed to parse response from the model"}, 500


def recommend_doctor(problem: str):
    doctors = fetch_doctors_from_database()
    prompt = generate_prompt(problem)

    try:
        response = post_process(prompt)
    except Exception as e:
        return {"error": str(e)}, 500

    print("Model Response:", response)  

    if "error" in response:
        return response, 500

    try:
        specialty = response.get("doctor_type")  
        doctor_names = response.get("doctors")
    except KeyError:
        return {"error": "Could not determine a suitable doctor specialty."}, 400

    print("Extracted Specialty:", specialty)  

    if not specialty or not doctor_names:
        return {"error": f"No doctors found for the specialty {specialty}"}, 404

   
    matching_doctors = get_doctors_by_specialty(specialty, doctors)
    doctor_info = {
        "doctor_type": specialty,
        "doctors": [doctor["user"]["name"] for doctor in matching_doctors]
    }

    return doctor_info



