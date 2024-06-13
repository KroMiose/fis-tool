import inquirer

from src.chat_models.gemini import ask_question
from src.itv_flow import generate_fis_desc_by_status, generate_fis_desc_flow
from src.prj_forge import (
    apply_changes_from_fis_content,
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
        prj_fis = generate_fis_desc_flow() or ""
        if not prj_fis:
            print("生成 FIS 结构未成功，请重试。")
            continue
        break

    print("=================================")
    print("项目初始化成功，进入对话交互模式。(输入 /? 查看可用命令)\n")
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
                    generate_fis_desc_by_status()
                    print(f"FIS 描述文件 '{output_file}' 更新成功。")
            elif question == "/?":
                print(
                    "可用命令：\n"
                    "/quit: 退出对话模式\n"
                    "/apply: 应用最新 FIS 变更\n"
                    "Tips: 生成回复过程可随时使用 Ctrl+C 中断输出\n"
                )
        else:  # 进入 Gemini生成
            last_res_content = ""
            print(f"\n{GEMINI_PLACEHOLDER}", end="")
            is_first_chunk = True
            try:
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
            except KeyboardInterrupt:
                print("\n\n!! 生成已中断")
