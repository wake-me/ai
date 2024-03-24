from typing import Optional
from model import Model
from translator.pdf_parser import PDFParser
from translator.writer import Writer
from utils import LOG

class PDFTranslator:
    """
    PDF翻译器类，用于将PDF文件中的文本内容翻译成指定语言，并将翻译结果保存到新的PDF文件中。
    
    参数:
    - model: Model类型的实例，用于执行翻译任务。
    """
    def __init__(self, model: Model):
        """
        初始化PDF翻译器实例。
        
        参数:
        - model: Model类型的实例，用于执行翻译任务。
        """
        self.model = model
        self.pdf_parser = PDFParser()  # PDF解析器实例
        self.writer = Writer()  # 文本写入器实例

    def translate_pdf(self, pdf_file_path: str, file_format: str = 'PDF', target_language: str = '中文', output_file_path: str = None, pages: Optional[int] = None):
        """
        翻译PDF文件，并将翻译结果保存到指定路径。
        
        参数:
        - pdf_file_path: 要翻译的PDF文件路径。
        - file_format: 输出文件格式，默认为'PDF'。
        - target_language: 目标语言，默认为'中文'。
        - output_file_path: 保存翻译结果的文件路径，如果未指定，则不保存。
        - pages: 要翻译的PDF页面范围，可选参数，如果未指定，则翻译所有页面。
        
        返回值:
        无
        """
        # 解析PDF文件
        self.book = self.pdf_parser.parse_pdf(pdf_file_path, pages)

        # 遍历并翻译每一页的内容
        for page_idx, page in enumerate(self.book.pages):
            for content_idx, content in enumerate(page.contents):
                # 为当前内容生成翻译提示，并进行翻译
                prompt = self.model.translate_prompt(content, target_language)
                LOG.debug(prompt)
                translation, status = self.model.make_request(prompt)
                LOG.info(translation)
                
                # 直接更新页面内容的翻译
                self.book.pages[page_idx].contents[content_idx].set_translation(translation, status)

        # 保存翻译后的书籍
        self.writer.save_translated_book(self.book, output_file_path, file_format)