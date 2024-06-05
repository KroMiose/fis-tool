import os
from pathlib import Path

import inquirer

from src.chat_models.gemini import ask_question, init_model
from src.prj_forge import (
    apply_changes_from_fis,
    create_project_from_fis,
    generate_description,
)


QUESTION_PROMPT_TEMPLATE = """
{prj_fis}

请基于以上 FIS 结构来回答我的问题：
{question}
"""


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
            ],
        )
        if "添加 FIS 结构说明提示词 (中文)" in options:
            use_explanation = "zh"
        elif "添加 FIS 结构说明提示词 (英文)" in options:
            use_explanation = "en"
        else:
            use_explanation = ""

        if "使用 .gitignore 文件过滤项目文件" in options:
            use_gitignore = True

        print(f"正在生成 FIS 描述文件 '{output_file}'...")
        prj_fis = generate_description(
            project_path, output_file, use_explanation, use_gitignore
        )
        break

    print("项目初始化成功，进入对话交互模式。\n")

    while True:
        question = input(">>> 请输入指令:")
        response = ask_question(
            QUESTION_PROMPT_TEMPLATE.format(prj_fis=prj_fis, question=question)
        )
        print(response)
