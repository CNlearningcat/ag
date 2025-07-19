from typing import Optional
from prompt_toolkit import prompt as ptk_prompt
from prompt_toolkit.key_binding import KeyBindings


class InputHandler:
    """用户多轮输入的处理"""

    def __init__(self):
        self.kb = KeyBindings()
        self._register_key_bindings()

    def _register_key_bindings(self):
        """注册所有快捷键"""
        @self.kb.add('c-s')
        def _(event):
            " Ctrl+s 提交 "
            event.current_buffer.validate_and_handle()

        @self.kb.add('c-x')
        def _(event):
            """Ctrl+X 退出处理"""
            event.app.exit(exception=SystemExit, style="class:aborting")

        @self.kb.add("c-z")
        def _(event):
            """Ctrl+Z 撤销"""
            event.app.current_buffer.undo()

        @self.kb.add("c-c")
        def _(event):
            """Ctrl-C 复制"""
            buff = event.app.current_buffer
            clipboard_text = buff.copy_selection() or buff.document.current_line
            event.app.clipboard.set_data(clipboard_text)

        @self.kb.add("c-v")
        def _(event):
            """Ctrl-V 粘贴"""
            clipboard_data = event.app.clipboard.get_data()
            if clipboard_data:
                event.app.current_buffer.insert_text(clipboard_data)

    def get_input(self) -> Optional[str]:
        """
        获取用户在终端中的输入并返回, 支持多行输入. 
        支持的快捷键:
        ctrl-s: 提交文本
        ctrl-c: 复制文本
        ctrl-v: 粘贴文本
        ctrl-x: 退出

        Returns:
            返回用户的输出

        Raises:
            SystemExit
        """
        try:
            return ptk_prompt(multiline=True, key_bindings=self.kb)
        except SystemExit:
            raise
        