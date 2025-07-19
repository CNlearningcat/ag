from colorama import Fore, Style, init
init()
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from typing import Iterable, Callable, Dict, Optional

# 项目内
from ag.config import AppConfig
from ag.utils.conversation import Conversation
from ag.core.handlers.stream_handler import StreamHandler
from ag.core.handlers.input_handler import InputHandler
from ag.core.client import OpenAIClient


class Agent:
    """一个命令行的ai agent 核心实现"""
    def __init__(self, config: AppConfig):
        # 配置
        self.app_config = config 
        # 服务端实例
        self.client = OpenAIClient(self.app_config)
        # 对话管理
        self.conversation = Conversation()
        # 流式
        self.stream_handler = StreamHandler()  
        # 多轮对话的输入管理
        self.input_handler = InputHandler()
    
    def query(self, messages:Iterable[ChatCompletionMessageParam], cot: bool = False, stream: bool = True) -> (str | dict[str, str]):
        """
        单轮查询

        Args:
            model: 要使用的模型的名称, 请查询你的API供应商提供哪些模型, 默认使用qwen-plus
            cot: 是否开启思维链
            stream: 是否开启流式输出

        Returns:
            dict: 返回{'reasoning': reasoning_content, 'answer': answer_content}字典, 代表模型的推理过程和回答
        """

        completion = self.client.chat_completion(
            messages=messages,
            model=self.app_config.model,
            stream=stream,
            extra_body={"enable_thinking": cot},
            )
        
        if not stream:
            return completion.choices[0].message.content
        
        else:
            return self.stream_handler.handle_stream(completion)
    
    def chat(self, on_input: Callable[[str, Optional[dict]], str] = None, cot: bool = False, stream: bool = True) -> None:
        """
        多轮对话模式

        Args:
            on_input: 对输入使用的解析函数, 比如替换文本的函数
            cot: 是否开启思维链
            stream: 是否开启流式输出
        """

        while True:
            try:
                print(f"\n{Fore.LIGHTBLUE_EX}输入>:")
                user_input = self.input_handler.get_input()
                
                if user_input:
                    if on_input is not  None:
                        self.conversation.add_user(on_input(user_input))
                    else:
                        self.conversation.add_user(user_input)
                    print(f"\n{Fore.MAGENTA}{self.app_config.model}{Style.RESET_ALL}:")
                    response = self.query(self.conversation.get_history(), cot, stream)
                    self.conversation.add_assistant(response['answer'])
            except SystemExit:
                print(f"{Fore.RED}退出多轮对话{Style.RESET_ALL}")
                break
                
    def model(self) -> str:
        """获取当前使用的模型名称"""
        return self.app_config.model    

    def get_conversation(self) -> Conversation:
        return self.conversation

if __name__ == '__main__':
    from ag.config import load_config

    config = load_config()

    ag = Agent(config)
    conversation = ag.get_conversation()
    conversation.add_user("你是谁?")
    result = ag.query(conversation.get_history(), cot=True) 
    print(result)
    # ag.chat()