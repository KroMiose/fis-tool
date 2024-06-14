import os
from typing import Generator, List

import inquirer
from google.generativeai.types import HarmBlockThreshold, HarmCategory

from src.chat_models.base import Chatbot
from src.chat_models.gemini_patch import patch_gemini_proxy
from src.options.choices import DynamicalChoices


class GeminiChatbot(Chatbot):
    def __init__(self):

        if not os.environ.get("GEMINI_API_PROXY"):
            proxy_url: str = inquirer.text(
                message="请输入 Gemini Proxy (留空则不使用代理)",
                default="",
            )
            proxy_url += "http://" if not proxy_url.startswith("http") else ""
            patch_gemini_proxy(proxy_url)
            confirm: bool = inquirer.confirm(
                message="是否保存 Proxy 到用户环境变量 'GEMINI_API_PROXY'？(下次无需输入)",
                default=True,
            )
            if confirm:
                os.system(f"setx GEMINI_API_PROXY {proxy_url} /m")

        import google.generativeai as genai # 必须在 patch 之后才能导入

        if not os.environ.get("GEMINI_API_KEY"):
            api_key: str = inquirer.text(
                message="请输入 Gemini API Key (使用 ctrl+shift+v 粘贴)",
                validate=lambda _, x: len(x) > 0,
            )
            genai.configure(api_key=api_key)
            confirm: bool = inquirer.confirm(
                message="是否保存 API Key 到用户环境变量 'GEMINI_API_KEY'？(下次无需输入)",
                default=True,
            )
            if confirm:
                os.system(f"setx GEMINI_API_KEY {api_key} /m")
        else:
            genai.configure(api_key=os.environ["GEMINI_API_KEY"])

        use_model = DynamicalChoices(
            prompt_message="请选择生成模型", choices=self.available_models(genai)
        ).action()
        print(f"使用模型: {use_model}")

        self._chat_model = genai.GenerativeModel(use_model)

    def ask_question(self, question: str) -> Generator[str, None, None]:
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
        response = self._chat_model.generate_content(
            question,
            safety_settings=safety_settings,
            stream=True,
        )
        for chunk in response:
            yield chunk.text

    def available_models(self, gai) -> List[str]:
        return [
            m.name
            for m in gai.list_models()
            if "generateContent" in m.supported_generation_methods
        ]
