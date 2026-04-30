'''
 * @Author       : MatthewZhang
 * @Date         : 2026-04-29 13:42:38
 * @Description  : 
'''

import os
import logging
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
logger = logging.getLogger(__name__)
load_dotenv()

# 目的: 读取examples下的所有py文件, 统一交给LLM处理
# 1.读取examples里的bad_async文件, 返回dict->{"文件名": 代码内容}
def read_file(file_path: str ="examples/bad_async.py"):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

#  # 2.写一串prompt用于让LLM检查代码是否出现异步问题
def build_review_prompt(code: str) -> str:
    PROMPT = f"""
    你是一个 Python asyncio 代码审查助手。

    请审查下面代码中是否存在 asyncio 反模式，重点关注：
    1. async 函数中是否混入同步阻塞调用
    2. 是否忘记 await
    3. 是否错误使用 asyncio.run
    4. 是否 create_task 后未保存引用
    5. 是否存在共享状态 race condition

    请按以下格式输出：
    【问题】
    【原因】
    【建议修改】
    【置信度】

    代码如下：

    ```python
    {code}
    ```
    """
    return PROMPT

# 3.调用LLM进行分析
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise RuntimeError("Missing required environment variable: DEEPSEEK_API_KEY")

# 获取云端DeepSeek模型
code = read_file()  # content: {"examples/bad_async.py": code(str类型)}
prompt = build_review_prompt(code)
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
resp = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[{"role": "user", "content": prompt}],
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}}
)

# 4.获取LLM输出结果
print(resp.choices[0].message.content)
