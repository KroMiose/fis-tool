import argparse

from src.interactive_main import main_interactive_mode
from src.prj_forge import (
    apply_changes_from_fis,
    create_project_from_fis,
    generate_description,
)


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
        help="使用 .gitignore 文件过滤项目文件",
    )
    generate_parser.add_argument(
        "-if",
        "--ignore-fis",
        action="store_true",
        help="忽略 .fis 文件",
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
            args.project_path,
            args.output,
            args.explanation,
            args.gitignore,
            args.ignore_fis,
        )
    elif args.command == "create":
        create_project_from_fis(args.description_file, args.output)
    elif args.command == "apply":
        apply_changes_from_fis(args.project_path, args.changes_file)
    else:
        # 如果没有指定子命令，则进入交互式模式
        main_interactive_mode()


if __name__ == "__main__":
    main()
