import pdfplumber
from typing import Optional
from book import Book, Page, Content, ContentType, TableContent
from translator.exceptions import PageOutOfRangeException
from utils import LOG


class PDFParser:
    """
    PDF解析器类，用于解析PDF文件并提取文本和表格内容。
    """

    def __init__(self):
        """
        初始化PDF解析器。
        """
        pass

    def parse_pdf(self, pdf_file_path: str, pages: Optional[int] = None) -> Book:
        """
        解析PDF文件，提取每页的文本和表格内容。

        参数:
        - pdf_file_path: str，PDF文件的路径。
        - pages: Optional[int]，要解析的页码范围。None表示解析所有页，否则解析从第一页到指定页。

        返回:
        - Book，包含解析得到的文本和表格内容的书对象。
        """
        book = Book(pdf_file_path)

        with pdfplumber.open(pdf_file_path) as pdf:
            # 检查指定页码范围是否超出PDF实际页数
            if pages is not None and pages > len(pdf.pages):
                raise PageOutOfRangeException(len(pdf.pages), pages)

            # 根据是否指定了页码范围，确定要解析的页码列表
            if pages is None:
                pages_to_parse = pdf.pages
            else:
                pages_to_parse = pdf.pages[:pages]

            for pdf_page in pages_to_parse:
                page = Page()

                # 提取原始文本内容和表格内容
                raw_text = pdf_page.extract_text()
                tables = pdf_page.extract_tables()

                # 从原始文本中移除表格内容
                for table_data in tables:
                    for row in table_data:
                        for cell in row:
                            raw_text = raw_text.replace(cell, "", 1)

                # 处理文本内容
                if raw_text:
                    # 清理文本，移除空行和首尾空白字符
                    raw_text_lines = raw_text.splitlines()
                    cleaned_raw_text_lines = [line.strip() for line in raw_text_lines if line.strip()]
                    cleaned_raw_text = "\n".join(cleaned_raw_text_lines)

                    text_content = Content(content_type=ContentType.TEXT, original=cleaned_raw_text)
                    page.add_content(text_content)
                    LOG.debug(f"[raw_text]\n {cleaned_raw_text}")

                # 处理表格内容
                if tables:
                    table = TableContent(tables)
                    page.add_content(table)
                    LOG.debug(f"[table]\n{table}")

                book.add_page(page)

        return book