from ag.config import load_config

import pytest

# def test_config_file_not_exist():
#     with pytest.raises(FileNotFoundError) as e:
#         config = load_config()
    
#     exception_message = str(e.value)
#     assert "配置文件不存在" in exception_message

def test_load_config():
    config = load_config()

    assert config.api_key is not None
    assert config.api_base == "https://dashscope.aliyuncs.com/compatible-mode/v1"
    assert config.model == 'qwen-plus'
    assert config.optional_models == {
        'qwp' : "qwen-plus",
        'qwt' : "qwen-turbo",
        'qwpl' : "qwen-plus-latest",
        'qwtl' : "qwen-turbo-latest",
        'dsv' : "deepseek-v3",
        'dsr' : "deepseek-r1"
    }