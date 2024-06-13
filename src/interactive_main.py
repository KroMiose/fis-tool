import sys

from src.interactive_prj import prj_interactive_mode
from src.itv_flow import apply_fis_changes_flow, generate_fis_desc_flow
from src.options.choices import EntranceChoices


def main_interactive_mode():
    """交互式命令行工具的主函数"""

    while True:
        answers = EntranceChoices.action()

        if answers is EntranceChoices.enter_prj_mode:
            prj_interactive_mode()
        elif answers is EntranceChoices.generate_fis_desc:
            generate_fis_desc_flow()
        elif answers is EntranceChoices.create_prj_from_fis:
            apply_fis_changes_flow()
        elif answers is EntranceChoices.apply_fis_changes:
            apply_fis_changes_flow()
        elif answers == "退出应用":
            sys.exit(0)
