

def is_text_file(file_path: str):
    """判断文件是否是文本文件。"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            f.read(1024)
        return True
    except UnicodeDecodeError:
        return False
