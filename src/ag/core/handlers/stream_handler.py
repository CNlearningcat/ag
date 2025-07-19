import signal
from colorama import Fore, Style, init
init()
from typing import Dict
from openai.types.chat import ChatCompletionChunk
from openai import Stream

class StreamHandler:
    
    def __init__(self):
        """
        专用于流式输出的Ctrl+C中断处理器

        Args:
            cleanup: 中断时需要执行的资源释放函数
        """
        self._interrupted = False
        signal.signal(signal.SIGINT, self._handle_signal)

    def _handle_signal(self, signum, frame):
        """信号处理逻辑"""
        print(f"\n{Fore.RED}用户中断{Style.RESET_ALL}")
        self._interrupted = True
    
    def handle_stream(
        self, 
        stream: Stream[ChatCompletionChunk],
    ) -> Dict[str, str] :
        """
        流式输出stream流的每一个元素ChatCompletionChunk的content, 并将所有的content
        都收集起来做出字典返回

        Args:
            stream: 一个ChatCompletionChunk为单位的输出流

        Reterns:
            推理和回答构成的字典
            {"reasoning": reasoning_content, "answer": answer_content}
        """
        reasoning_content = ""
        answer_content = ""
        is_thinking = False
        is_answering = False
        for chunk in stream:
            # 检查中断
            if self._interrupted:
                stream.close()
                self.reset()
                break

            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta

            # reasoning_content 和 content 是互斥的

            if hasattr(delta, "reasoning_content") and delta.reasoning_content:
                reasoning_content += delta.reasoning_content

                if not is_thinking:
                    print(f"{Fore.CYAN}=========思考过程========={Style.RESET_ALL}", flush=True)
                    is_thinking = True

                print(f"{Fore.YELLOW}{delta.reasoning_content}{Style.RESET_ALL}", end='', flush=True)
                    

            if hasattr(delta, "content") and delta.content:
                answer_content += delta.content

                if not is_answering:
                    print(f"\n{Fore.LIGHTGREEN_EX}=========回答========={Style.RESET_ALL}", flush=True)
                    is_answering = True

                print(delta.content, end='', flush=True)
        

        return {"reasoning": reasoning_content, "answer": answer_content}


    def reset(self):
        self._interrupted = False

    
    def __enter__(self):
        return self

    def __exit__(self, *args):
        signal.signal(signal.SIGINT, signal.SIG_DFL)  # 恢复默认处理