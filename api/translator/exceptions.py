class PageOutOfRangeException(Exception):
    """
    自定义异常类，用于表示请求的页码超出了书籍的实际页码范围。

    :param book_pages: int, 书籍的实际页数
    :param requested_pages: int, 请求的页数
    """
    def __init__(self, book_pages, requested_pages):
        # 初始化异常实例，保存书籍页数和请求页数，并设置异常信息
        self.book_pages = book_pages
        self.requested_pages = requested_pages
        super().__init__(f"Page out of range: Book has {book_pages} pages, but {requested_pages} pages were requested.")