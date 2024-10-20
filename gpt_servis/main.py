from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests

from AI import AI

app = FastAPI()
load_dotenv()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


class HelpRequest(BaseModel):
    messages: str
    language_user: str


# @app.post("/api/v1/help_with_understanding/")
# async def help_with_understanding(request: HelpRequest):
#     ai = AI()
#     response = ai.get_help_with_understanding("help_with_understanding", request.messages, request.language_user)
#     return response


@app.post("/api/v1/help_with_understanding/")
async def help_with_understanding(request: HelpRequest):
    ai = AI()
    response = ai.get_help_with_understanding("help_with_understanding", request.messages, request.language_user)
    return {"CONTEXT": 'Es folgte ein Gespräch mit Standardfragen zum Zustand des Gesprächspartners. Anschließend fragte der Gesprächspartner, warum Sie Ukrainisch lernen und ob Sie sich für Kultur interessieren.', 'ANSWERS': [
        'Так, ваша культура дуже цікава. Хочу краще зрозуміти історію та традиції.', 'Так, дуже подобається ваша музика і література. Хочу читати в оригіналі.', 'Так, ваша культура дуже багата і різноманітна. Хочу відчути її глибше.',
        'Так, хочу більше подорожувати Україною і краще спілкуватися з місцевими.'
    ]}


@app.post("/api/v1/help_with_grammar/")
async def help_with_grammar(request: HelpRequest):
    ai = AI()
    response = ai.get_help("help_with_grammar", request.messages, request.language_user)
    return response


@app.post("/api/v1/get_text_response/")
async def get_text_response(request: HelpRequest):
    ai = AI()
    response = ai.get_text_response(request.messages, request.language_user)
    return {"response": response}


def register_service_in_registry():
    service_data = {
        'service_name': os.environ.get('SERVICE_NAME'),
        'description': 'Description',
        'version_number': os.environ.get('VERSION_NUMBER'),
        'service_url': os.environ.get('SERVICE_URL')
    }

    registry_url = os.environ.get('REGISTRY_SERVICE_URL')

    try:
        response = requests.post(registry_url, json=service_data)
        response.raise_for_status()
        print(f"The radio now includes the “communicator” service: {response.status_code}")
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")


register_service_in_registry()
