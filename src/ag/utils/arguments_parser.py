import argparse

def arguments_parser():
    parser = argparse.ArgumentParser(
        description="(LLM) AGent for everything",
        usage="ag [-h] [-c] [-q QUERY] [-r] [-m MODEL] "
    )
    parser.add_argument("-n", "--no-stream", action="store_true", help="Unable stream output")
    parser.add_argument("-c", "--cot", action="store_true", help="Enable chain-of-thought reasoning")
    parser.add_argument("-q", "--query", type=str, default=None, help="One query one response")
    parser.add_argument("-r", "--revise", action="store_true", help="Revise the content; produce diff form.")
    parser.add_argument("-m", "--model", type=str, default=None, help="before use this, you should set the optional-model table in config file")
    return parser