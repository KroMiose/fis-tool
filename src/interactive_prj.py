from typing import Type
import inquirer

from src.chat_models.base import Chatbot
from src.itv_flow import generate_fis_desc_by_status, generate_fis_desc_flow
from src.prj_forge import apply_changes_from_fis_content
from src.utils import read_multiline_input

QUESTION_PROMPT_TEMPLATE = """
{prj_fis}

请基于以上 FIS 结构来回答我的问题：
{question}
"""

AI_PLACEHOLDER = ">>> [AI]: 正在建立连接..."


def prj_interactive_mode():
    """项目交互模式"""
    project_path: str = ""
    output_file: str = ""
    prj_fis: str = ""

    def _gen_fis():
        nonlocal prj_fis

        while True:
            prj_fis = generate_fis_desc_flow() or ""
            if not prj_fis:
                print("生成 FIS 结构未成功，请重试。")
                continue
            break

    _gen_fis()

    from src.chat_models.gemini import GeminiChatbot
    from src.chat_models.chatgpt import ChatGPTChatbot

    chat_models = {
        "Gemini": GeminiChatbot,
        "ChatGPT": ChatGPTChatbot,
    }

    model_choice = inquirer.list_input(
        "请选择对话模型来源",
        choices=list(chat_models.keys()),
    )

    chatbot_class: Type[Chatbot] = chat_models[model_choice]
    chatbot = chatbot_class()

    print(
        "=================================\n"
        "项目初始化成功，进入对话交互模式。(输入 /? 查看可用命令，按下 Ctrl+Enter 提交输入)\n"
    )
    last_res_content = ""
    last_question = ""
    generate_flag = False

    while True:
        try:
            question = read_multiline_input("\n>>> [Command]: ")
        except KeyboardInterrupt:
            print("\n\n!! 退出交互模式。")
            return

        if not question:
            continue

        generate_flag = False

        if question.startswith("/"):  # 控制命令
            if question == "/quit":
                print("\n\n!! 退出交互模式。")
                return
            elif question == "/apply":
                print("正在应用最新 FIS 变更...")
                if inquirer.confirm(
                    message="应用 FIS 变更将直接覆盖现有项目文件，请确保可以通过 git 等工具恢复项目文件，确定继续？",
                    default=False,
                ):
                    apply_changes_from_fis_content(project_path, last_res_content)
                if inquirer.confirm(message="是否更新 FIS 描述文件？", default=True):
                    generate_fis_desc_by_status()
                    print(f"FIS 描述文件 '{output_file}' 更新成功。")
            elif question == "/restart":
                _gen_fis()
            elif question == "/r":
                if last_question:
                    question = last_question
                    generate_flag = True
                else:
                    print("没有可重试的对话。")
            elif question == "/?":
                print(
                    "可用命令：\n"
                    "/quit: 退出对话模式\n"
                    "/apply: 应用最新 FIS 变更\n"
                    "/restart: 重新生成 FIS 结构\n"
                    "/r: 重试上一次对话\n"
                    "Tips: 生成回复过程可随时使用 Ctrl+C 中断输出\n"
                )
            else:
                print(f"未知命令 '{question}'，请重新输入。")
        else:
            generate_flag = True

        if not generate_flag:
            continue

        # 进入语言模型生成
        last_res_content = ""
        last_question = question
        print(f"\n{AI_PLACEHOLDER}", end="")
        is_first_chunk = True
        try:
            for chunk in chatbot.ask_question(
                QUESTION_PROMPT_TEMPLATE.format(prj_fis=prj_fis, question=question)
            ):
                if is_first_chunk:
                    is_first_chunk = False
                    print("\r" + (len(AI_PLACEHOLDER) * "  "), end="")
                    print("\r>>> [AI]: ", end="")
                print(chunk, end="")
                last_res_content += chunk
            print()
        except KeyboardInterrupt:
            print("\n\n!! 生成已中断")
        except Exception as e:
            print(f"\n\n!! 生成失败，错误: {e}")
