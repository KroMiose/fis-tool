import os
from typing import Generator, List

import httpx
import inquirer
import openai

from src.chat_models.base import Chatbot
from src.options.choices import DynamicalChoices


class ChatGPTChatbot(Chatbot):
    def __init__(self):
        self._api_key = os.environ.get("OPENAI_API_KEY")
        self._base_url = os.environ.get("OPENAI_BASE_URL")
        self._proxy = os.environ.get("OPENAI_PROXY")

        if not self._api_key:
            self._api_key = inquirer.text(
                message="请输入 OpenAI API Key (使用 ctrl+shift+v 粘贴)",
                validate=lambda _, x: len(x) > 0,
            )
            openai.api_key = self._api_key
            confirm: bool = inquirer.confirm(
                message="是否保存 API Key 到用户环境变量 'OPENAI_API_KEY'？(下次无需输入)",
                default=True,
            )
            if confirm:
                os.system(f"setx OPENAI_API_KEY {self._api_key} /m")
        else:
            self._api_key = os.environ["OPENAI_API_KEY"]
            openai.api_key = self._api_key

        if not self._base_url:
            self._base_url = inquirer.text(
                message="请输入 OpenAI API Base URL (留空使用官方 API)",
                default="https://api.openai.com/v1",
            )
            confirm: bool = inquirer.confirm(
                message="是否保存 API Key 到用户环境变量 'OPENAI_BASE_URL'？(下次无需输入)",
                default=True,
            )
            if confirm:
                os.system(f"setx OPENAI_BASE_URL {self._base_url} /m")
        else:
            self._base_url = os.environ["OPENAI_BASE_URL"]

        if not self._proxy:
            self._proxy = inquirer.text(
                message="请输入 OpenAI 代理 URL (留空不使用代理)",
                default="",
            )
            self._proxy += "http://" if not self._proxy.startswith("http") else ""
            confirm: bool = inquirer.confirm(
                message="是否保存 OpenAI 代理地址到用户环境变量 'OPENAI_PROXY'？(下次无需输入)",
                default=True,
            )
            if confirm:
                os.system(f"setx OPENAI_PROXY {self._proxy} /m")
        else:
            self._proxy = os.environ["OPENAI_PROXY"]

        try:
            models = self.available_models()
        except openai.AuthenticationError:
            print(
                "OpenAI API Key 无效或非官方 API，无法获取最新模型列表，使用内置模型列表"
            )
            models = [
                "gpt-3.5-turbo",
                "gpt-3.5-turbo-0125",
                "gpt-3.5-turbo-0301",
                "gpt-3.5-turbo-0613",
                "gpt-3.5-turbo-1106",
                "gpt-3.5-turbo-16k",
                "gpt-3.5-turbo-16k-0613",
                "gpt-3.5-turbo-instruct",
                "gpt-4",
                "gpt-4-0125-preview",
                "gpt-4-0314",
                "gpt-4-0613",
                "gpt-4-1106-preview",
                "gpt-4-32k",
                "gpt-4-32k-0314",
                "gpt-4-32k-0613",
                "gpt-4-all",
                "gpt-4-turbo-preview",
                "gpt-4o",
                "gpt-4o-2024-05-13",
                "自定义",
            ]
        self._model = DynamicalChoices(
            prompt_message="请选择生成模型", choices=models
        ).action()
        if self._model == "自定义":
            self._model = inquirer.text(
                message="请输入自定义模型名称",
                validate=lambda _, x: len(x) > 0,
            )

        print(f"使用模型: {self._model}")

    def ask_question(self, question: str) -> Generator[str, None, None]:
        proxy_client = (
            httpx.Client(proxy=httpx.Proxy(self._proxy), follow_redirects=True)
            if self._proxy
            else None
        )
        response = openai.OpenAI(
            api_key=self._api_key, http_client=proxy_client, base_url=self._base_url
        ).chat.completions.create(
            model=self._model or "gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an experienced software master.",
                },
                {"role": "user", "content": question},
            ],
            stream=True,
        )

        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                yield content

    def available_models(self) -> List[str]:
        models = openai.models.list()
        return [str(model.id) for model in models if "gpt" in str(model.id)]
