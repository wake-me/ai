import requests
import simplejson

from model import Model

class GLMModel(Model):
    """
    GLMModel类，继承自Model类，用于通过HTTP请求与特定的模型服务进行交互。
    
    参数:
    - model_url: str，模型服务的URL地址。
    - timeout: int，请求超时时间（秒）。
    """
    def __init__(self, model_url: str, timeout: int):
        self.model_url = model_url  # 模型服务的URL
        self.timeout = timeout  # 请求超时时间

    def make_request(self, prompt):
        """
        向模型服务发送请求，并获取响应。
        
        参数:
        - prompt: str，发送给模型的服务端的输入文本。
        
        返回:
        - translation: str，模型服务返回的文本响应。
        - True: bool，表示请求成功。
        """
        try:
            # 准备请求的负载数据
            payload = {
                "prompt": prompt,
                "history": []
            }
            # 向模型服务发送POST请求
            response = requests.post(self.model_url, json=payload, timeout=self.timeout)
            # 检查响应状态
            response.raise_for_status()
            # 解析JSON响应
            response_dict = response.json()
            translation = response_dict["response"]  # 提取响应文本
            return translation, True
        except requests.exceptions.RequestException as e:
            # 处理请求异常
            raise Exception(f"请求异常：{e}")
        except requests.exceptions.Timeout as e:
            # 处理请求超时
            raise Exception(f"请求超时：{e}")
        except simplejson.errors.JSONDecodeError as e:
            # 处理JSON解析错误
            raise Exception("Error: response is not valid JSON format.")
        except Exception as e:
            # 处理其他未知异常
            raise Exception(f"发生了未知错误：{e}")
        return "", False  # 请求失败时的返回值