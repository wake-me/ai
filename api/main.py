
# 导入系统和操作系统模块
import sys
import os

# 将当前文件所在目录添加到系统路径中，以便能够找到自定义模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入自定义的工具模块和模型模块
from utils import ArgumentParser, ConfigLoader, LOG
from model import GLMModel, OpenAIModel
from translator import PDFTranslator

# 主程序入口
if __name__ == "__main__":

    # 解析命令行参数
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()

    # 加载配置文件
    config_loader = ConfigLoader(args.config)
    config = config_loader.load_config()

    # 根据命令行参数或配置文件加载OpenAI模型和API密钥
    model_name = args.openai_model if args.openai_model else config['OpenAIModel']['model']
    api_key = args.openai_api_key if args.openai_api_key else config['OpenAIModel']['api_key']
    model = OpenAIModel(model=model_name, api_key=api_key)

    # 根据命令行参数或配置文件设置PDF文件路径和文件格式
    pdf_file_path = args.book if args.book else config['common']['book']
    file_format = args.file_format if args.file_format else config['common']['file_format']

    # 创建PDF翻译器实例，并执行PDF翻译
    translator = PDFTranslator(model)
    translator.translate_pdf(pdf_file_path, file_format)