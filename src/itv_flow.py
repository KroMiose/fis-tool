import os
from pathlib import Path

import inquirer

from src.options.choices import GeneratorChoices
from src.prj_forge import (
    apply_changes_from_fis_file,
    generate_description,
)
from src.utils import format_path


class Status:
    """用户配置状态类"""

    project_path: str = ""
    fis_file: str = ""
    use_explanation: str = ""
    use_gitignore: bool = False
    ignore_fis: bool = False
    use_custom_fis_config: bool = False


def generate_fis_desc_flow():
    Status.project_path = inquirer.text(
        message="请输入项目根目录路径 (留空使用当前目录)", default=Status.project_path
    )
    if not Status.project_path:
        Status.project_path = "."
    Status.project_path = format_path(Status.project_path)
    if not os.path.exists(Status.project_path):
        print(f"错误: 项目路径 '{Status.project_path}' 不存在。")
        return

    prj_name = Path(Status.project_path).name or "local"

    Status.fis_file = inquirer.text(
        message="请输入输出描述文件路径",
        default=Status.fis_file or f"{Status.project_path}/{prj_name}_prj_desc.fis",
    )
    if "." not in Status.fis_file:
        Status.fis_file += ".fis"
    if os.path.exists(Status.fis_file):
        confirm = inquirer.confirm(
            message=f"FIS 描述文件 '{Status.fis_file}' 已存在，是否覆盖？",
            default=True,
        )

        if not confirm:
            print("操作已取消。")
            return

    options = GeneratorChoices.checkbox()
    if GeneratorChoices.add_fis_desc_zh in options:
        Status.use_explanation = "zh"
    elif GeneratorChoices.add_fis_desc_en in options:
        Status.use_explanation = "en"
    else:
        Status.use_explanation = ""

    Status.use_gitignore = GeneratorChoices.use_gitignore in options
    Status.ignore_fis = GeneratorChoices.ignore_fis_files in options
    Status.use_custom_fis_config = GeneratorChoices.use_custom_fis_config in options

    print(f"正在生成 FIS 描述文件 '{Status.fis_file}'...")

    return generate_fis_desc_by_status()


def generate_fis_desc_by_status():
    return generate_description(
        project_path=Status.project_path,
        fis_file=Status.fis_file,
        use_explanation=Status.use_explanation,
        use_gitignore=Status.use_gitignore,
        ignore_fis=Status.ignore_fis,
        use_custom_fis_config=Status.use_custom_fis_config,
    )


def apply_fis_changes_flow():
    Status.project_path = inquirer.text(
        message="请输入项目根目录路径 (留空使用当前目录)", default=Status.project_path
    )
    if not Status.project_path:
        Status.project_path = "."

    if not os.path.exists(Status.project_path):
        print(f"错误: 项目路径 '{Status.project_path}' 不存在。")
        return
    fis_file = inquirer.text(message="请拖动 FIS 文件到此处", default=Status.fis_file)
    if not os.path.exists(fis_file):
        print(f"错误: FIS 文件 '{fis_file}' 不存在。")
        return

    apply_changes_from_fis_file(Status.project_path, fis_file)
