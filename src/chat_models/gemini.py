import os
from typing import List, Optional

import google.generativeai as genai
import inquirer
from google.generativeai.types import (
    HarmBlockThreshold,
    HarmCategory,
)

from src.options.choices import DynamicalChoices

_chat_model: Optional[genai.GenerativeModel] = None


def init_model():
    global _chat_model

    if _chat_model:
        return _chat_model
    print("")

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
        prompt_message="请选择生成模型", choices=available_models()
    ).action()
    print(f"使用模型: {use_model}")

    _chat_model = genai.GenerativeModel(use_model)
    return _chat_model


def ask_question(question):
    chat_model: genai.GenerativeModel = init_model()
    # 安全设置 (没有生效，暂不清楚原因)
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,  # 默认不屏蔽
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,  # 默认不屏蔽
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,  # 默认不屏蔽
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,  # 默认不屏蔽
    }
    # 可选安全设置
    # HarmBlockThreshold.BLOCK_NONE # 不屏蔽任何内容
    # HarmBlockThreshold.BLOCK_ONLY_HIGH # 仅屏蔽可能性高的内容
    # HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,  # 屏蔽可能性为中或高的危险内容
    # HarmBlockThreshold.BLOCK_LOW_AND_ABOVE # 屏蔽可能性为低及以上的内容
    response = chat_model.generate_content(
        question,
        safety_settings=safety_settings,  # 安全审查
        stream=True,
    )
    for chunk in response:
        yield chunk.text


def available_models() -> List[str]:
    return [
        m.name
        for m in genai.list_models()
        if "generateContent" in m.supported_generation_methods
    ]
