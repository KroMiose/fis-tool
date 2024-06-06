import os
from typing import Optional
import google.generativeai as genai
import inquirer
from google.generativeai.types import HarmCategory, HarmBlockThreshold

chat_model: Optional[genai.GenerativeModel] = None


def init_model():
    if not os.environ.get("GEMINI_API_KEY"):
        api_key: str = inquirer.text(
            message="请输入 Gemini API Key",
            validate=lambda _, x: len(x) > 0,
        )
        genai.configure(api_key=api_key)
        confirm: bool = inquirer.confirm(
            message="是否保存 API Key 到用户环境变量 'GEMINI_API_KEY'？(下次无需输入)",
            default=True,
        )
        if confirm:
            os.system(f"setx GEMINI_API_KEY {api_key}")
    else:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    return genai.GenerativeModel("gemini-1.5-pro")


def ask_question(question):
    global chat_model
    if not chat_model:
        chat_model = init_model()
    # 模型配置
    generation_config = {
        "temperature": 0.8,  # 控制采样温度，较高的值会使输出更具创造性但可能不太连贯 (0 - 1)
        # "top_p": 0.95,  # 控制 Nucleus sampling 的概率质量阈值 (0 - 1)
        # "top_k": 40,  # 控制采样时考虑的词汇数量 (0 - inf)
        # "max_output_tokens": 1024,  # 输出的最大 token 数量
    }
    # 安全设置
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT:
        HarmBlockThreshold.BLOCK_NONE,  # 默认不屏蔽
        HarmCategory.HARM_CATEGORY_HATE_SPEECH:
        HarmBlockThreshold.BLOCK_NONE,  # 默认不屏蔽
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT:
        HarmBlockThreshold.BLOCK_NONE,  # 默认不屏蔽
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT:
        HarmBlockThreshold.BLOCK_NONE,  # 默认不屏蔽
    }
    # 可选安全设置
    # HarmBlockThreshold.BLOCK_NONE # 不屏蔽任何内容
    # HarmBlockThreshold.BLOCK_ONLY_HIGH # 仅屏蔽可能性高的内容
    # HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,  # 屏蔽可能性为中或高的危险内容
    # HarmBlockThreshold.BLOCK_LOW_AND_ABOVE # 屏蔽可能性为低及以上的内容
    response = model.generate_content(
        question,
        generation_config=generation_config,  # 模型配置
        safety_settings=safety_settings,  # 安全审查
        stream=True,
    )
    for chunk in response:
        yield chunk.text
