import os
from pathlib import Path
import re

import gitignorefile

from src.instruction import INSTRUCTION_TEXT, INSTRUCTION_TEXT_EN
from src.utils import is_text_file

FILE_START_PREFIX = "$$$" + " "


def generate_description(
    project_path: str,
    output_file: str,
    use_explanation: str,
    use_gitignore: bool,
    ignore_fis: bool,
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
            file_name = os.path.basename(file_path)

            if ignore_fis and file_name.endswith(".fis"):  # 忽略 fis 文件
                # print(f"文件 {relative_path} 是 fis 文件，将跳过。")
                continue

            if use_gitignore and (
                gitignorefile.ignored(file_path) or relative_path.startswith(".git")
            ):  # 被 .gitignore 忽略或在 .git 目录下
                # print(f"文件 {relative_path} 被 .gitignore 忽略，将跳过。")
                continue

            # print(f"读取文件: {relative_path}")

            if is_text_file(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.readlines()
                description += f"{FILE_START_PREFIX}{relative_path}\n"
                description += "".join(content)
            else:
                description += f"{FILE_START_PREFIX}{relative_path} [BINARY]\n"

    if use_explanation:
        description += "```"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(description)
    print(f"项目描述已保存至: {output_file}")
    return description


def read_fis_description_from_content(description_content: str) -> str:

    # 文件包含指导信息需要截取
    if description_content.startswith(INSTRUCTION_TEXT):
        description_content = description_content[len(INSTRUCTION_TEXT) :].strip()
    if description_content.startswith(INSTRUCTION_TEXT_EN):
        description_content = description_content[len(INSTRUCTION_TEXT_EN) :].strip()

    # 使用正则表达式去除注释部分
    description_content = re.sub(
        r"{/\*.*?\*/}", "", description_content, flags=re.DOTALL
    )

    # 文件包含 ```fis 和 ``` 需要进行提取
    if "```fis\n" in description_content and "\n```" in description_content:
        # 按最长匹配原则提取 fis 代码块内容 (忽略中间可能的 ``` 截取到最后一个)
        fis_start = description_content.index("```fis\n")
        fis_end = description_content.rindex("\n```")

        description_content = description_content[fis_start + 6 : fis_end].strip()

    return description_content


def apply_changes_from_fis_content(project_path: str, content: str):
    """应用 fis 变更内容到项目中。"""

    content = read_fis_description_from_content(content)

    changes = content.split(FILE_START_PREFIX)[1:]
    for change in changes:
        file_path, *content_lines = change.split("\n", 1)
        file_path = file_path.strip()
        opt_tag = re.search(r"(\[.*\])", file_path)

        if opt_tag:
            opt_tag = opt_tag.group(1)
            file_path = file_path.replace(f"{opt_tag}", "").strip()
        full_path = Path(os.path.join(project_path, file_path))
        Path(full_path).parent.mkdir(parents=True, exist_ok=True)
        new_content = content_lines[0] if len(content_lines) else ""

        # 忽略非文本文件的变更
        if opt_tag == "[BINARY]":
            print(f"忽略非文本文件: {file_path}")
            continue

        # 文件级别变更
        if content_lines and opt_tag == "[REPLACE]":
            full_path.write_text(new_content, encoding="utf-8")
            print(f"修改文件 {file_path}")
        elif content_lines and opt_tag == "[DELETE]":
            full_path.unlink()
            print(f"删除文件 {file_path}")
        elif content_lines and file_path:
            full_path.write_text(new_content, encoding="utf-8")
            print(f"创建文件 {file_path}")


def create_project_from_fis(output_path: str, description_content: str):
    """
    从描述文本创建项目文件结构。
    """

    Path(output_path).mkdir(parents=True, exist_ok=True)
    return apply_changes_from_fis_content(output_path, description_content)


def apply_changes_from_fis_file(project_path: str, changes_file: str):
    """从文件中读取变更描述并应用到项目中。"""

    changes_description = Path(changes_file).read_text(encoding="utf-8")
    return apply_changes_from_fis_content(project_path, changes_description)
