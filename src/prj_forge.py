import os
import re

import gitignorefile

from src.instruction import INSTRUCTION_TEXT, INSTRUCTION_TEXT_EN
from src.utils import is_text_file


def generate_description(
    project_path: str,
    output_file: str,
    use_explanation: str,
    use_gitignore: bool,
) -> str:
    """从项目生成描述文本。"""

    description = ""

    if use_explanation:
        if use_explanation == "zh":
            description += INSTRUCTION_TEXT + "\n```fis\n"
        elif use_explanation == "en":
            description += INSTRUCTION_TEXT_EN + "\n```fis\n"

    for root, _, files in os.walk(project_path):

        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, project_path)

            if use_gitignore and (
                gitignorefile.ignored(file_path) or relative_path.startswith(".git")
            ):  # 被 .gitignore 忽略或在 .git 目录下
                # print(f"文件 {relative_path} 被 .gitignore 忽略，将跳过。")
                continue

            # print(f"读取文件: {relative_path}")

            if is_text_file(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.readlines()
                description += f"$$$ {relative_path}\n"
                description += "".join(content)
            else:
                description += f"$$$ {relative_path} [BINARY]\n"

    if use_explanation:
        description += "```"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(description)
    print(f"项目描述已保存至: {output_file}")
    return description


def read_fis_description(description_file: str) -> str:
    """读取描述文本内容。"""

    with open(description_file, "r", encoding="utf-8") as f:
        description = f.read()

    # 使用正则表达式去除注释部分
    description = re.sub(r"{/\*.*?\*/}", "", description, flags=re.DOTALL)

    # 文件包含指导信息需要截取
    if description.startswith(INSTRUCTION_TEXT):
        description = description[len(INSTRUCTION_TEXT) :].strip()

    # 文件包含 ```fis 和 ``` 需要进行提取
    if "```fis\n" in description:
        description = description.split("```fis\n")[1].rsplit("\n```")[0]

    return description


def create_project_from_fis(description_file: str, output_path: str):
    """
    从描述文本创建项目文件结构。
    """

    description = read_fis_description(description_file)

    files = description.split("$$$ ")[1:]
    for file_data in files:
        file_path, *content_lines = file_data.split("\n", 1)
        file_path = file_path.strip()
        full_path = os.path.join(output_path, file_path)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        if content_lines and "[BINARY]" not in file_path:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content_lines[0])
            print(f"文件已创建: {full_path}")
        elif "[BINARY]" in file_path:
            open(full_path, "a").close()
            print(f"空文件已创建: {full_path}")


def apply_changes_from_fis(project_path: str, changes_file: str):
    """从文件中读取变更描述并应用到项目中。"""

    changes_description = read_fis_description(changes_file)

    changes = changes_description.split("$$$ ")[1:]
    for change in changes:
        file_path, *content_lines = change.split("\n", 1)
        file_path = file_path.strip()
        full_path = os.path.join(project_path, file_path)

        # 忽略非文本文件的变更
        if "[BINARY]" in file_path:
            print(f"忽略非文本文件: {file_path}")
            continue

        if content_lines and "[REPLACE]" in file_path:
            # 文件级别变更
            file_path = file_path.replace("[REPLACE]", "").strip()
            new_content = content_lines[0]
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"修改文件 {file_path}")
        if content_lines and "[NEW]" in file_path:
            # 文件级别变更
            file_path = file_path.replace("[REPLACE]", "").strip()
            new_content = content_lines[0]
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"创建文件 {file_path}")
        if content_lines and "[DELETE]" in file_path:
            # 文件级别变更
            file_path = file_path.replace("[DELETE]", "").strip()
            os.remove(full_path)
            print(f"删除文件 {file_path}")
