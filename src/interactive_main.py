import os
import sys
from pathlib import Path

import inquirer

from src.interactive_prj import prj_interactive_mode
from src.options.choices import GeneratorChoices, EntranceChoices
from src.prj_forge import (
    apply_changes_from_fis_file,
    create_project_from_fis,
    generate_description,
)


def main_interactive_mode():
    """交互式命令行工具的主函数"""

    last_prj_path: str = ""
    last_desc_path: str = ""

    while True:
        answers = EntranceChoices.action()

        if answers is EntranceChoices.enter_prj_mode:
            prj_interactive_mode()
        elif answers is EntranceChoices.generate_fis_desc:
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

            options = GeneratorChoices.checkbox()
            if GeneratorChoices.add_fis_desc_zh in options:
                use_explanation = "zh"
            elif GeneratorChoices.add_fis_desc_en in options:
                use_explanation = "en"
            else:
                use_explanation = ""

            use_gitignore = GeneratorChoices.use_gitignore in options
            ignore_fis = GeneratorChoices.ignore_fis_files in options

            print(f"正在生成 FIS 描述文件 '{output_file}'...")
            generate_description(
                project_path, output_file, use_explanation, use_gitignore, ignore_fis
            )

        elif answers is EntranceChoices.create_prj_from_fis:
            description_file = inquirer.text(message="请输入 FIS 描述文件路径")
            if not os.path.exists(description_file):
                print(f"错误:  FIS 描述文件 '{description_file}' 不存在。")
                continue
            output_path = inquirer.text(
                message="请输入输出项目路径", default=last_prj_path
            )
            create_project_from_fis(description_file, output_path)

        elif answers is EntranceChoices.apply_fis_changes:
            project_path = inquirer.text(
                message="请输入项目根目录路径", default=last_prj_path
            )
            if not os.path.exists(project_path):
                print(f"错误: 项目路径 '{project_path}' 不存在。")
                continue
            changes_file = inquirer.text(message="请拖动 FIS 文件到此处")
            if not os.path.exists(changes_file):
                print(f"错误: FIS 文件 '{changes_file}' 不存在。")
                continue

            apply_changes_from_fis_file(project_path, changes_file)
        elif answers == "退出应用":
            sys.exit(0)
