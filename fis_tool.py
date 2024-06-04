import os
import re
import sys
from pathlib import Path
from typing import Dict, cast
import argparse

import inquirer

from instruction import INSTRUCTION_TEXT, INSTRUCTION_TEXT_EN


def is_text_file(file_path: str):
    """判断文件是否是文本文件。"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            f.read(1024)
        return True
    except UnicodeDecodeError:
        return False


def check_file_ignore(file_path: str, gitignore_content: str):
    """检查文件是否在.gitignore中忽略。"""
    if not gitignore_content:
        return False
    for pattern in gitignore_content.split("\n"):
        if pattern.startswith("#"):
            continue
        if re.match(pattern, file_path):
            return True
    return False


def generate_description(
    project_path: str,
    output_file: str,
    use_explanation: str,
    use_gitignore: bool,
):
    """从项目生成描述文本。"""

    description = ""

    if use_explanation:
        if use_explanation == "zh":
            description += INSTRUCTION_TEXT + "\n```fis\n"
        elif use_explanation == "en":
            description += INSTRUCTION_TEXT_EN + "\n```fis\n"

    if use_gitignore:
        gitignore_path = os.path.join(project_path, ".gitignore")
        if os.path.exists(gitignore_path):
            with open(gitignore_path, "r", encoding="utf-8") as f:
                gitignore_content = f.read()

    for root, _, files in os.walk(project_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, project_path)

            if use_gitignore and check_file_ignore(relative_path, gitignore_content):
                continue

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


def read_fis_description(description_file: str):
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


def interactive_mode():
    """交互式命令行工具的主函数。"""

    last_prj_path: str = ""
    last_desc_path: str = ""

    while True:
        answers = cast(
            Dict,
            inquirer.prompt(
                [
                    inquirer.List(
                        "action",
                        message="请选择操作：",
                        choices=[
                            # "从远程仓库生成 FIS 描述文件",
                            "从项目目录生成 FIS 描述文件",
                            "从 FIS 描述文件创建项目",
                            "从 FIS 描述文件应用项目变更",
                            "退出应用",
                        ],
                    )
                ]
            ),
        )

        if answers["action"] == "从项目目录生成 FIS 描述文件":
            project_path = inquirer.text(
                message="请输入项目根目录路径", default=last_prj_path
            )
            if not os.path.exists(project_path):
                print(f"错误: 项目路径 '{project_path}' 不存在。")
                continue
            last_prj_path = project_path

            prj_name = Path(project_path).name

            output_file = inquirer.text(
                message="请输入输出描述文件路径",
                default=last_desc_path or f"{prj_name}_pro_desc.fis",
            )
            if "." not in output_file:
                output_file += ".fis"
            if os.path.exists(output_file):
                confirm = inquirer.confirm(
                    message=f"文件 '{output_file}' 已存在，是否覆盖？", default=True
                )

                if not confirm:
                    continue
            last_desc_path = output_file

            options = inquirer.list_input(
                message="请选择选项：(方向键选择；空格: 选择；回车: 确认)",
                choices=[
                    "添加 FIS 结构说明提示词 (中文)",
                    "添加 FIS 结构说明提示词 (英文)",
                    "使用 .gitignore 文件忽略项目文件",
                ],
            )
            if "添加 FIS 结构说明提示词 (中文)" in options:
                use_explanation = "zh"
            elif "添加 FIS 结构说明提示词 (英文)" in options:
                use_explanation = "en"
            else:
                use_explanation = ""

            if "使用 .gitignore 文件忽略项目文件" in options:
                use_gitignore = True

            generate_description(
                project_path, output_file, use_explanation, use_gitignore
            )

        elif answers["action"] == "从 FIS 描述文件创建项目":
            description_file = inquirer.text(message="请输入 FIS 描述文件路径")
            if not os.path.exists(description_file):
                print(f"错误:  FIS 描述文件 '{description_file}' 不存在。")
                continue
            output_path = inquirer.text(
                message="请输入输出项目路径", default=last_prj_path
            )
            create_project_from_fis(description_file, output_path)

        elif answers["action"] == "从 FIS 描述文件应用项目变更":
            project_path = inquirer.text(
                message="请输入项目根目录路径", default=last_prj_path
            )
            if not os.path.exists(project_path):
                print(f"错误: 项目路径 '{project_path}' 不存在。")
                continue
            changes_file = inquirer.text(message="请拖动 FIS 文件到此处: ")
            if not os.path.exists(changes_file):
                print(f"错误: FIS 文件 '{changes_file}' 不存在。")
                continue

            apply_changes_from_fis(project_path, changes_file)
        elif answers["action"] == "退出应用":
            sys.exit(0)


def main():
    """交互式命令行工具的主函数。"""

    parser = argparse.ArgumentParser(description="FIS (File Interaction Script) 工具")

    # 定义子命令
    subparsers = parser.add_subparsers(dest="command")

    # 生成 FIS 描述文件命令
    generate_parser = subparsers.add_parser(
        "generate", help="从项目目录生成 FIS 描述文件"
    )
    generate_parser.add_argument("project_path", help="项目根目录路径")
    generate_parser.add_argument(
        "-o", "--output", help="输出描述文件路径", default=None
    )
    generate_parser.add_argument(
        "-e",
        "--explanation",
        choices=["zh", "en"],
        help="添加 FIS 结构说明提示词 (zh: 中文; en: 英文)",
        default=None,
    )
    generate_parser.add_argument(
        "-g",
        "--gitignore",
        action="store_true",
        help="使用 .gitignore 文件忽略项目文件",
    )

    # 从 FIS 描述文件创建项目命令
    create_parser = subparsers.add_parser("create", help="从 FIS 描述文件创建项目")
    create_parser.add_argument("description_file", help="FIS 描述文件路径")
    create_parser.add_argument("-o", "--output", help="输出项目路径", default=None)

    # 应用 FIS 描述文件中的变更命令
    apply_parser = subparsers.add_parser("apply", help="从 FIS 描述文件应用项目变更")
    apply_parser.add_argument("project_path", help="项目根目录路径")
    apply_parser.add_argument("changes_file", help="FIS 变更文件路径")

    args = parser.parse_args()

    # 根据子命令执行对应功能
    if args.command == "generate":
        generate_description(
            args.project_path, args.output, args.explanation, args.gitignore
        )
    elif args.command == "create":
        create_project_from_fis(args.description_file, args.output)
    elif args.command == "apply":
        apply_changes_from_fis(args.project_path, args.changes_file)
    else:
        # 如果没有指定子命令，则进入交互式模式
        interactive_mode()


if __name__ == "__main__":
    main()
