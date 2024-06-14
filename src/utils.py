import locale
import os
import sys
import threading
import time

import keyboard


def shell_init():
    # 设置输出编码为 UTF-8
    preferred_encoding = locale.getpreferredencoding()
    if preferred_encoding.lower() != "utf-8":
        sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf-8", buffering=1)
        sys.stderr = open(sys.stderr.fileno(), mode="w", encoding="utf-8", buffering=1)
    # 设置终端编码为 UTF-8
    if os.name == "nt":
        os.system("chcp 65001")
    # 清屏
    os.system("cls" if os.name == "nt" else "clear")


def is_text_file(file_path: str):
    """判断文件是否是文本文件。"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            f.read(1024)
        return True
    except UnicodeDecodeError:
        return False


def format_path(path):
    return path.replace("\\\\", "\\").replace("\\", "/")


def read_multiline_input(prompt: str):
    """读取多行输入; Ctrl+Enter 结束输入, Enter / Shift+Enter 键换行"""

    end_input = False

    def check_ctrl_enter():
        nonlocal end_input
        while True:
            if (
                keyboard.is_pressed("ctrl")
                and keyboard.is_pressed("enter")
                and not keyboard.is_pressed("shift")
            ):
                end_input = True
                time.sleep(0.05)
                keyboard.release("ctrl")
                keyboard.release("enter")
                time.sleep(0.05)
                keyboard.press_and_release("enter")
                break

    lines = []
    print(prompt, end="")

    # 启动一个线程来检测 Ctrl+Enter
    thread = threading.Thread(target=check_ctrl_enter, daemon=True)
    thread.start()

    while True:
        lines.append(input())
        if end_input:
            break

    thread.join()  # 等待线程结束
    return "\n".join(lines).strip()
