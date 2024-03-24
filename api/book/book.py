
from .page import Page


class Book:
    """
    书籍类，用于管理和组织PDF文件中的页面。

    参数:
    - pdf_file_path: str，PDF文件的路径。

    属性:
    - pdf_file_path: str，存储PDF文件的路径。
    - pages: list，存储Page对象的列表，每个Page对象代表PDF中的一页。
    """

    def __init__(self, pdf_file_path):
        """
        初始化书籍对象。

        参数:
        - pdf_file_path: str，PDF文件的路径。
        """
        self.pdf_file_path = pdf_file_path
        self.pages = []  # 初始化一个空列表，用于存储页面

    def add_page(self, page: Page):
        """
        向书籍中添加一个页面。

        参数:
        - page: Page，一个Page对象，代表PDF中的一页。
        """
        self.pages.append(page)  # 将提供的页面添加到页面列表中
