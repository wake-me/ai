'''
Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
Date: 2024-03-23 21:45:20
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2024-03-23 23:16:37
FilePath: \ai_translator\api\app.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import argparse
from flask import Flask




def parse_args():

    parser = argparse.ArgumentParser(description="这是一个 AI 翻译助手")
    parser.add_argument('--port', type=int, default=5000, help='运行应用的端口号，默认为5000')
    parser.add_argument('--env', choices=['development', 'production'], default='development', help='应用运行环境，默认为development')


    return parser.parse_args()

# 创建 Flask 应用实例
app = Flask(__name__)

# 假设这是你的路由和其他配置
@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    args = parse_args()
    
    # 根据命令行参数配置应用
    app.run(host='0.0.0.0', port=args.port, debug=args.env == 'development')