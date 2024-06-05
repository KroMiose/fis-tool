import os
import sys
from pathlib import Path
from typing import Dict, cast

import inquirer

from src.prj_forge import (
    apply_changes_from_fis,
    create_project_from_fis,
    generate_description,
)
from src.interactive_prj import prj_interactive_mode


def main_interactive_mode():
    """交互式命令行工具的主函数"""

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
                            "进入项目交互模式",
                            "从项目目录生成 FIS 描述文件",
                            "从 FIS 描述文件创建项目",
                            "从 FIS 描述文件应用项目变更",
                            "退出应用",
                        ],
                    )
                ]
            ),
        )

        if answers["action"] == "进入项目交互模式":
            prj_interactive_mode()
        elif answers["action"] == "从项目目录生成 FIS 描述文件":
            project_path = inquirer.text(
                message="请输入项目根目录路径 (留空使用当前目录)", default=last_prj_path
            )
            if not project_path:
                project_path = "."
            if not os.path.exists(project_path):
                print(f"错误: 项目路径 '{project_path}' 不存在。")
                continue
            last_prj_path = project_path

            prj_name = Path(project_path).name or "local"

            output_file = inquirer.text(
                message="请输入输出描述文件路径",
                default=last_desc_path or f"{prj_name}_prj_desc.fis",
            )
            if "." not in output_file:
                output_file += ".fis"
            if os.path.exists(output_file):
                confirm = inquirer.confirm(
                    message=f"FIS 描述文件 '{output_file}' 已存在，是否覆盖？",
                    default=True,
                )

                if not confirm:
                    print("操作已取消。")
                    continue
            last_desc_path = output_file

            options = inquirer.checkbox(
                message="请选择生成选项：(方向键: 切换选项；空格: 选择；回车: 确认)",
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
            generate_description(
                project_path, output_file, use_explanation, use_gitignore, ignore_fis
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
