import re
from typing import List

import yaml

from src.setting import DEFAULT_FIS_CONFIG_FILE
from src.utils import format_path


class FisConfig:
    def __init__(self, config_file):
        with open(config_file, "r") as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

    def get_ignore_regex(self) -> List[str]:
        return self.config.get("ignore_regex", [])

    def is_match_ignore_path(self, path) -> bool:
        """匹配忽略目录"""
        for reg in self.get_ignore_regex():
            if re.match(reg, format_path(path)):
                return True
        return False

    @classmethod
    def create_fis_config_template(cls, config_file) -> "FisConfig":
        config = {
            "ignore_regex": [
                f"/?{DEFAULT_FIS_CONFIG_FILE}",
                r"\.git/",
                r"\.svn/",
                r"\.idea/",
                r"\.vscode/",
                r"\.DS_Store",
                r"__pycache__/",
                r"\.pyc$",
                r"\.pyo$",
                r"\.lock$",
                r"/?node_modules/",
                r"/?build/",
                r"/?dist/",
                r"/?output/",
                r"/?temp/",
            ]
        }

        with open(config_file, "w") as f:
            yaml.dump(config, f)

        return cls(config_file)
