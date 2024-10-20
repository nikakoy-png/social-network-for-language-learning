import json
import logging
import os

from openai import OpenAI
from dotenv import load_dotenv

from SingletonMeta import SingletonMeta

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


class AI(metaclass=SingletonMeta):
    def __init__(self, prompts: dict = None, model: str = None):
        self.__model = "gpt-3.5-turbo" if not model else model
        self.__prompts = prompts or {
            "help_with_understanding": ["""ANSWER FAST. Retell the content of the dialog creatively from the messages. With explanations for
             a person who does not know the language in which the messages are written. CREATIVELY RETELL. 
             The answer should be in json format {"CONTEXT": context}""", """ANSWER FAST. you act as a helper, analyze 
            the conversation and help the user find the answer. The response options should be in the 
            language of the conversati
            on. The answer should be in json format {"ANSWERS": [...]}"""],
            "help_with_grammar": """The system helps the user understand the use of grammar in the message and 
            provides explanations in the user's language. The response should be in JSON format as follows: 
            {"CONTEXT":, "ANSWER": [...]}. You must reply in the user's language. Min 2."""
        }
        self.__client = OpenAI(api_key=OPENAI_API_KEY)

    def get_help_with_understanding(self, task_type: str, messages=None, language_user: str = None) -> dict:
        response_1 = self.__client.chat.completions.create(
            model=self.__model,
            messages=[
                {"role": "system", "content": f"""{self.__prompts[task_type][0]}.
                                Here's your prompt in {language_user} language. 
                                Please provide the answer in this language. ANSWER FAST"""},
                {"role": "user", "content": f"MESSAGES: {''.join(messages)}."}
            ],
            temperature=0.4
        )
        response_2 = self.__client.chat.completions.create(
            model=self.__model,
            messages=[
                {"role": "system", "content": self.__prompts[task_type][-1]},
                {"role": "user", "content": f"MESSAGES: {''.join(messages)}. ANSWER FAST"}
            ],
            temperature=0.7
        )
        content_1 = json.loads(response_1.choices[-1].message.content)
        content_2 = json.loads(response_2.choices[-1].message.content)
        combined_response = {
            "CONTEXT": content_1["CONTEXT"],
            "ANSWERS": content_2["ANSWERS"],
        }
        return combined_response

    def get_text_response(self, messages: str, language_user: str) -> str:
        response = self.__client.chat.completions.create(
            model=self.__model,
            messages=[
                {"role": "user", "content": f"MESSAGES: {messages}. USER LANGUAGE: {language_user}"}
            ],
            temperature=0.7
        )
        return response.choices[-1].message.content

    def get_help(self, task_type: str, messages=None, language_user: str = None) -> dict:
        response = self.__client.chat.completions.create(
            model=self.__model,
            messages=[
                {"role": "system", "content": self.__prompts[task_type]},
                {"role": "user", "content": f"MESSAGES: {''.join(messages)}. USER LANGUAGE: {language_user}"}
            ],
            temperature=0.7
        )

        logging.log(msg=f"RESPONSE: {response.choices[-1].message.content}", level=logging.INFO)
        return json.loads(response.choices[-1].message.content)