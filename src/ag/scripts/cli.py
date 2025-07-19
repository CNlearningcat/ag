import sys
from colorama import Fore, Style, init
init()

from ag.core.agent import Agent
from ag.utils.arguments_parser import arguments_parser
from ag.utils.replace_flags import replace_tags
from ag.config import load_config

def main():
    # 解析命令行参数
    parser = arguments_parser()
    args = parser.parse_args()

    # 加载配置文件 
    config = load_config()
    # 初始化 Agent
    agent = Agent(config)
    
    # 单次查询模式
    if args.query != None:
        try:
            conversation = agent.get_conversation()
            conversation.add_user(f'{replace_tags(args.query)}')

            print(f"\n{Fore.MAGENTA}{agent.model()}{Style.RESET_ALL}:")
            response = agent.query(
                messages=conversation.get_history(),
                cot=args.cot,
                stream=not args.no_stream
            )
            if type(response) == str:
                print(response, flush=True)
            
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        print()
        sys.exit(0)
    
    else:
        # 交互式聊天模式
        print(f"\n{Fore.GREEN}进入交互对话模式 (ctrl-s:提交输入, ctrl-x:退出, ctrl-c: 中断输出){Style.RESET_ALL}\n")
        agent.chat(on_input=replace_tags, cot=args.cot, stream=not args.no_stream)
        sys.exit(0)


if __name__ == '__main__':
    main()