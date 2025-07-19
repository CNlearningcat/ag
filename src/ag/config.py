# src/ag/config.py
from pathlib import Path
from typing import Optional, Dict
import toml
from pydantic import BaseModel, field_validator

class AppConfig(BaseModel):
    """
    纯文件配置模型（仅 TOML 文件）
    配置字段说明：
    - api_key:   API 访问密钥（必填）
    - api_base:  API 基础地址（默认: OpenAI 官方）
    - timeout:   请求超时时间（秒，默认: 30）
    - model:     模型名称（默认: gpt-4）
    """
    api_key: str = ""
    api_base: str = "https://api.openai.com/v1"
    timeout: int = 10
    model: str = "gpt-4"
    optional_models: Dict[str, str] = {} 

    @field_validator("api_key")
    def validate_api_key(cls, v: str) -> str:
        if not v:
            raise ValueError("API_KEY 不能为空！")
        return v

    @field_validator("timeout")
    def validate_timeout(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("超时时间必须大于 0")
        return v

def load_config(config_path: Optional[str] = None) -> AppConfig:
    """
    从 TOML 文件加载配置
    :param config_path: 可选的配置文件路径（默认: ~/.ag/config.toml）
    :raises: FileNotFoundError 如果配置文件不存在或格式错误
    """
    # 1. 确定配置文件路径
    default_path = Path("~/.config/ag/config.toml").expanduser() # 
    toml_path = Path(config_path) if config_path else default_path

    # 2. 读取并解析 TOML
    if not toml_path.exists():
        raise FileNotFoundError(f"配置文件不存在: {toml_path}")

    with open(toml_path, "r", encoding="utf-8") as f:
        config_data = toml.load(f)
    
    # 3. 提取 [ag] 段落并验证
    return AppConfig(**config_data.get("ag", {}))


if __name__ == "__main__":
    # 测试配置加载
    try:
        config = load_config()
        print("配置加载成功:", config)
        print("模型:", config.model)
    except Exception as e:
        print(f"配置加载失败: {e}")