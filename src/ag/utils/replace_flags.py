import re
import os
import subprocess
from typing import Dict, Callable


def replace_tags(text: str, context: dict = None) -> str:
    """
    替换文本中所有支持的 @xxx(...) 标签为对应的内容。
    
    支持：
        - @file(path)
        - @dir(path)
        - @shell(command)
        
    示例：
        input: "查看这个文件 @file(test.txt)"
        output: "查看这个文件 <文件内容>"
    """

    # 默认上下文为空字典
    if context is None:
        context = {}

    # 注册支持的标签及其处理函数
    # 解耦, 主函数 `replace_tags()` 不需要知道每个标签具体怎么处理，它只负责调用对应的名字即可
    tag_handlers: Dict[str, Callable[[str, dict], str]] = {
        "file": handle_file_tag,
        "dir": handle_dir_tag,
        "shell": handle_shell_tag,
    }

    # 正则匹配 @tag(...)
    pattern = r"@(\w+)\(([^)]*)\)"
    def replace_match(match):
        tag_name = match.group(1).lower()
        content = match.group(2)

        handler = tag_handlers.get(tag_name)
        if handler:
            try:
                return handler(content.strip(), context)
            except Exception as e:
                return f"[Error in @{tag_name}({content}): {e}]"
        else:
            return match.group(0)  # 未知标签保留不变

    return re.sub(pattern, replace_match, text)


## ✅ 各个标签的实现

### 1. `@file(path)`
def handle_file_tag(path: str, context: dict) -> str:
    """处理 @file(path) 指令，返回文件内容。"""
    # 使用上下文中的base_dir（如果存在）
    if context and "base_dir" in context:
        full_path = os.path.join(context["base_dir"], path)
    else:
        full_path = os.path.expanduser(path)
    
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        return f"\n{content}"
    except Exception as e:
        raise RuntimeError(f"无法读取文件: {e}")


### 2. `@dir(path)`
def handle_dir_tag(path: str, context: dict) -> str:
    """
    处理 @dir(path) 指令，返回目录结构树状图。
    """
    # 使用上下文中的base_dir（如果存在）
    if context and "base_dir" in context:
        full_path = os.path.join(context["base_dir"], path)
    else:
        full_path = os.path.expanduser(path)
    
    if not os.path.isdir(full_path):
        raise ValueError(f"{full_path} 不是一个目录")

    tree_lines = []

    def walk_directory(root, prefix=""):
        items = sorted(os.listdir(root))
        for i, item in enumerate(items):
            full_item = os.path.join(root, item)
            is_last = (i == len(items) - 1)
            new_prefix = prefix + ("└── " if is_last else "├── ")

            if os.path.isdir(full_item):
                tree_lines.append(prefix + item + "/")
                walk_directory(full_item, prefix + ("    " if is_last else "│   "))
            else:
                tree_lines.append(new_prefix + item)

    walk_directory(full_path)
    return "\n".join(tree_lines)


### 3. `@shell(cmd)`
def handle_shell_tag(cmd: str, context: dict) -> str:
    """处理 @shell(cmd) 指令，执行命令并返回输出。"""
    # 替换命令中的上下文变量
    if context:
        for key, value in context.items():
            cmd = cmd.replace(f"${key}", str(value))
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=True
        )
        return f"\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"<internal: shell output of `{cmd}`>\n{e.stdout}\n[Exit Code: {e.returncode}]"


## ✅ 使用示例

if __name__ == "__main__":
    sample_text = """
    这是一个测试：
    - 查看文件：@file(test.py)
    - 查看目录：@dir(.)
    - 运行命令：@shell(ls)
    """

    replaced = replace_tags(sample_text)
    print(replaced)


## ✅ 可扩展性设计说明
'''
通过注册机制，你可以很方便地添加新的标签处理器。例如：

```python
def handle_code_tag(lang: str, context: dict) -> str:
    ...
    
# 添加新支持的标签
tag_handlers["code"] = handle_code_tag
```

或者从外部传入自定义上下文或配置：

```python
context = {
    "base_dir": "/some/path",
    "username": "alice"
}
replaced = replace_tags(text, context=context)
```

---

## ✅ 总结

✅ 当前支持的功能：

| 指令 | 功能 |
|------|------|
| `@file(path)` | 插入指定文件内容 |
| `@dir(path)` | 插入目录结构树 |
| `@shell(cmd)` | 执行 shell 命令并插入输出 |

✅ 可扩展性：

- 新增一个标签只需添加一个处理函数和注册；
- 支持传递上下文参数；
- 支持错误捕获与提示；
- 避免破坏原始文本格式。

'''
