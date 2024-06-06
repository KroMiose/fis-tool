import os
from pathlib import Path

import inquirer

from src.chat_models.gemini import ask_question, init_model
from src.prj_forge import (
    apply_changes_from_fis_content,
    # create_project_from_fis,
    generate_description,
)

QUESTION_PROMPT_TEMPLATE = """
{prj_fis}

请基于以上 FIS 结构来回答我的问题：
{question}
"""

GEMINI_PLACEHOLDER = ">>> [Gemini]: 正在建立连接..."


def prj_interactive_mode():
    """项目交互模式"""

    project_path: str = ""
    output_file: str = ""
    prj_fis: str = ""

    while True:
        init_model()
        project_path = inquirer.text(
            message="请输入项目根目录路径 (留空使用当前目录)",
        )
        if not project_path:
            project_path = "."
        if not os.path.exists(project_path):
            print(f"错误: 项目路径 '{project_path}' 不存在。")
            continue
        prj_name = Path(project_path).name or "local"
        output_file = f"{prj_name}_prj_desc.fis"

        if os.path.exists(output_file):
            confirm = inquirer.confirm(
                message=f"FIS 描述文件 '{output_file}' 已存在，是否覆盖？", default=True
            )

            if not confirm:
                print("操作已取消。")
                return

        options = inquirer.checkbox(
            message="请选择生成选项：(方向键选择；空格: 选择；回车: 确认)",
            choices=[
                "添加 FIS 结构说明提示词 (中文)",
                "添加 FIS 结构说明提示词 (英文)",
                "使用 .gitignore 文件过滤项目文件",
                "忽略 .fis 文件",
            ],
        )
        if "添加 FIS 结构说明提示词 (中文)" in options:
            use_explanation = "zh"
        elif "添加 FIS 结构说明提示词 (英文)" in options:
            use_explanation = "en"
        else:
            use_explanation = ""

        use_gitignore = "使用 .gitignore 文件过滤项目文件" in options
        ignore_fis = "忽略 .fis 文件" in options

        print(f"正在生成 FIS 描述文件 '{output_file}'...")
        prj_fis = generate_description(
            project_path, output_file, use_explanation, use_gitignore, ignore_fis
        )
        break

    print("项目初始化成功，进入对话交互模式。\n")
    last_res_content = ""

    while True:
        question = input("\n>>> [Command]: ")

        if not question:
            continue

        if question.startswith("/"):  # 控制命令
            if question == "/quit":
                print("退出对话模式。")
                return
            elif question == "/apply":
                print("正在应用最新 FIS 变更...")
                if inquirer.confirm(
                    message="应用 FIS 变更将直接覆盖现有项目文件，请确保可以通过 git 等工具恢复项目文件，确定继续？",
                    default=False,
                ):
                    apply_changes_from_fis_content(project_path, last_res_content)
                if inquirer.confirm(message="是否更新 FIS 描述文件？", default=True):
                    generate_description(
                        project_path,
                        output_file,
                        use_explanation,
                        use_gitignore,
                        ignore_fis,
                    )
                    print(f"FIS 描述文件 '{output_file}' 更新成功。")
        else:  # 进入 Gemini生成
            print()
            last_res_content = ""
            print("", end=GEMINI_PLACEHOLDER)
            is_first_chunk = True
            for chunk in ask_question(
                QUESTION_PROMPT_TEMPLATE.format(prj_fis=prj_fis, question=question)
            ):
                if is_first_chunk:
                    is_first_chunk = False
                    print("\r" + (len(GEMINI_PLACEHOLDER) * "  "), end="")
                    print("\r>>> [Gemini]: ", end="")
                print(chunk, end="")
                last_res_content += chunk
            print()
