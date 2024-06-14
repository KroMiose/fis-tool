import inquirer


class ChoicesBase:
    """选项组基类"""

    _prompt_message = "请选择"

    @classmethod
    def choices(cls):
        """生成子选项列表"""
        try:
            return cls.expose_choices()
        except NotImplementedError:
            _group = []
            for attr in dir(cls):
                value = getattr(cls, attr)
                if attr.startswith("_") or callable(getattr(cls, attr)):
                    continue
                if not isinstance(value, (str, int, float, bool)):
                    continue
                _group.append((value, attr))

            return _group

    @classmethod
    def prompt(cls):
        """生成选项提示"""
        return cls._prompt_message

    @classmethod
    def checkbox(cls, **kwargs):
        """进行多选动作"""
        return inquirer.checkbox(
            message=cls._prompt_message, choices=cls.choices(), **kwargs
        )

    @classmethod
    def action(cls, **kwargs):
        """进行单选动作"""
        return inquirer.prompt(  # type: ignore
            [
                inquirer.List(
                    "action",
                    message=cls._prompt_message,
                    choices=cls.choices(),
                )
            ],
            **kwargs
        )["action"]

    @classmethod
    def expose_choices(cls):
        """暴露选项列表"""
        raise NotImplementedError


class DynamicChoicesBase:
    """选项组基类"""

    _prompt_message = "请选择"

    def choices(self):
        """生成子选项列表"""
        raise NotImplementedError

    def prompt(self):
        """生成选项提示"""
        return self._prompt_message

    def checkbox(self, **kwargs):
        """进行多选动作"""
        return inquirer.checkbox(
            message=self._prompt_message, choices=self.choices(), **kwargs
        )

    def action(self, **kwargs):
        """进行单选动作"""
        return inquirer.prompt(  # type: ignore
            [
                inquirer.List(
                    "action",
                    message=self._prompt_message,
                    choices=self.choices(),
                )
            ],
            **kwargs
        )["action"]

    def expose_choices(self):
        """暴露选项列表"""
        raise NotImplementedError
