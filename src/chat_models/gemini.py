import os
from typing import Optional

import google.generativeai as genai
import inquirer

chat_model: Optional[genai.GenerativeModel] = None


def init_model():
    if not os.environ.get("GEMINI_API_KEY"):
        api_key = inquirer.text(
            message="请输入 Gemini API Key",
            validate=lambda _, x: len(x) > 0,
        ).execute()
        genai.configure(api_key=api_key)
        confirm = inquirer.confirm(
            message="是否保存 API Key 到用户环境变量 'GEMINI_API_KEY'？(下次无需输入)",
            default=True,
        ).execute()
        if confirm:
            os.system(f"setx GEMINI_API_KEY {api_key}")
    else:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    return genai.GenerativeModel("gemini-1.5-flash")


def ask_question(question):
    global chat_model
    if not chat_model:
        chat_model = init_model()
    response = chat_model.generate_content(question)
    return response.text
