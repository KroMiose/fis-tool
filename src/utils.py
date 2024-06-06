import locale
import os
import sys


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
