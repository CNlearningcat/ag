from typing import Iterable, Optional, Union
from openai import OpenAI, Stream
from openai.types.chat import ChatCompletionChunk, ChatCompletion
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam

from ag.config import AppConfig 

class OpenAIClient:
    """封装所有OpenAI API交互操作"""
    
    def __init__(self, config: Optional[AppConfig] = None):
        """
        Args:
            config: 配置对象，包含API密钥和基础URL
                   None时会自动加载默认配置
        """
        self.config = config or AppConfig()
        self._sync_client = OpenAI(
            api_key=self.config.api_key,
            base_url=self.config.api_base,
            timeout=self.config.timeout
        )

    def chat_completion(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        model: str,
        stream: bool = True,
        **kwargs
    ) -> (ChatCompletion | Stream[ChatCompletionChunk]):
        """执行聊天补全操作
        
        Args:
            messages: 消息历史列表
            model: 使用的模型ID
            stream: 是否使用流式响应
            **kwargs: 其他API参数(temperature等)
            
        Returns:
            流式模式返回生成器，非流式返回完整响应文本
        """
        params = {
            "model": model,
            "messages": messages,
            "stream": stream,
            **kwargs
        }
        return self._sync_client.chat.completions.create(**params)
    

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """清理客户端资源"""
        self._sync_client.close()
        # 异步客户端使用context manager自动管理

if __name__ == '__main__':
    client = OpenAIClient()
    print(client.list_models())