'''
Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
Date: 2024-03-23 20:58:47
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2024-03-23 21:36:15
FilePath: \ai_translator\api\book\page.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from .content import Content

class Page:
    """
    Page类用于创建和管理页面内容。
    """

    def __init__(self):
        """
        初始化Page对象，创建一个空的内容列表。
        """
        self.contents = []  # 存储页面内容的列表

    def add_content(self, content: Content):
        """
        向页面中添加内容。

        参数:
        content (Content): 需要添加到页面的内容对象。
        
        返回值:
        无
        """
        self.contents.append(content)  # 将新内容添加到内容列表中