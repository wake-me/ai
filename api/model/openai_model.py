
import requests
import simplejson
import time
import os
import openai

from model import Model
from utils import LOG
from openai import OpenAI

class OpenAIModel(Model):
    """
    一个封装了OpenAI API的模型类，用于与OpenAI进行交互。

    参数:
    - model: 字符串，指定使用的OpenAI模型名称。
    - api_key: 字符串，OpenAI的API密钥。
    """

    def __init__(self, model: str, api_key: str):
        """
        初始化OpenAIModel实例。

        参数:
        - model: 字符串，指定使用的OpenAI模型名称。
        - api_key: 字符串，OpenAI的API密钥。
        """
        self.model = model
        # 使用环境变量中的API密钥初始化OpenAI客户端
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def make_request(self, prompt):
        """
        向OpenAI发送请求，获取模型生成的响应。

        参数:
        - prompt: 字符串，给模型的输入提示。

        返回:
        - 一个元组，包含模型生成的文本和一个布尔值，表示请求是否成功。
        """
        attempts = 0  # 初始化重试次数
        while attempts < 3:  # 最多重试3次
            try:
                # 根据模型类型发送不同的请求
                if self.model == "gpt-3.5-turbo":
                    # 对话模型的请求
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[  # 构造对话消息
                            {"role": "user", "content": prompt}
                        ]
                    )
                    translation = response.choices[0].message.content.strip()  # 提取响应内容
                else:
                    # 通用模型的请求
                    response = self.client.completions.create(
                        model=self.model,
                        prompt=prompt,
                        max_tokens=150,  # 最大生成令牌数
                        temperature=0  # 温度设置为0，得到最确定的结果
                    )
                    translation = response.choices[0].text.strip()  # 提取响应内容

                return translation, True  # 成功返回响应和标志
            except openai.RateLimitError as e:  # 处理速率限制错误
                attempts += 1
                if attempts < 3:
                    LOG.warning("Rate limit reached. Waiting for 60 seconds before retrying.")
                    time.sleep(60)  # 等待60秒后重试
                else:
                    raise Exception("Rate limit reached. Maximum attempts exceeded.")  # 超过最大重试次数，抛出异常
            except openai.APIConnectionError as e:  # 处理API连接错误
                print("The server could not be reached")
                print(e.__cause__)  # 打印底层异常，可能是httpx库抛出的
            except requests.exceptions.Timeout as e:  # 处理请求超时错误
                # 这里省略了对该错误的处理代码
                pass
            except openai.APIStatusError as e:  # 处理其他API状态错误
                print("Another non-200-range status code was received")
                print(e.status_code)
                print(e.response)
            except Exception as e:  # 处理其他未知错误
                raise Exception(f"发生了未知错误：{e}")
        return "", False  # 如果所有尝试都失败，返回空字符串和False