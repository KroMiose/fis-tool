from src.options.base import ChoicesBase


class EntranceChoices(ChoicesBase):
    """入口选项"""

    _prompt_message = "请选择操作：( [↑, ↓] 切换选项; [回车] 确认 )"

    enter_prj_mode = "进入项目交互模式"
    generate_fis_desc = "从项目目录生成 FIS 描述文件"
    create_prj_from_fis = "从 FIS 描述文件创建项目"
    apply_fis_changes = "从 FIS 描述文件应用项目变更"
    quit_app = "退出应用"

    @classmethod
    def expose_choices(cls):
        return [
            cls.enter_prj_mode,
            cls.generate_fis_desc,
            cls.create_prj_from_fis,
            cls.apply_fis_changes,
            cls.quit_app,
        ]


class GeneratorChoices(ChoicesBase):
    """FIS 生成器选项"""

    _prompt_message = "请选择生成选项：( [↑, ↓] 切换选项; [空格] 选择; [回车] 确认 )"

    add_fis_desc_zh = "添加 FIS 结构说明提示词 (中文)"
    add_fis_desc_en = "添加 FIS 结构说明提示词 (英文)"
    use_gitignore = "使用 .gitignore 文件过滤项目文件"
    ignore_fis_files = "忽略 .fis 文件"
    use_custom_fis_config = "使用自定义 FIS 配置文件"

    @classmethod
    def expose_choices(cls):
        return [
            cls.add_fis_desc_zh,
            cls.add_fis_desc_en,
            cls.use_gitignore,
            cls.ignore_fis_files,
            cls.use_custom_fis_config,
        ]
