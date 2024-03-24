
# 从book模块导入ContentType枚举类
from book import ContentType

class Model:
    """
    提供与翻译请求相关的模型方法。
    """
    
    def make_text_prompt(self, text: str, target_language: str) -> str:
        """
        生成文本翻译提示。

        :param text: 需要翻译的文本字符串。
        :param target_language: 目标语言。
        :return: 返回一个字符串，包含翻译提示信息。
        """
        return f"翻译为{target_language}：{text}"

    def make_table_prompt(self, table: str, target_language: str) -> str:
        """
        生成表格翻译提示。

        :param table: 需要翻译的表格字符串。
        :param target_language: 目标语言。
        :return: 返回一个字符串，包含翻译提示信息，要求保持表格格式。
        """
        return f"将以下表格数据翻译成{target_language}，并确保翻译后的数据是cvs结构。请确保保持原始的数据结构，包括列名、行数据以及它们之间的对齐方式。例如：以逗号分隔的值列表（CSV），且不包含多余的空格或间隔字符。\n原表格数据：\n{table}"
        # return f"翻译为{target_language}，保持格式一致（间距,空格，分隔符），以表格形式返回：\n{table}"

    def translate_prompt(self, content, target_language: str) -> str:
        """
        根据内容类型生成对应的翻译提示。

        :param content: 包含原始内容和内容类型的对象。
        :param target_language: 目标语言。
        :return: 返回一个字符串，包含相应的翻译提示信息。
        """
        if content.content_type == ContentType.TEXT:
            # 如果内容类型为文本，则调用make_text_prompt生成文本翻译提示
            return self.make_text_prompt(content.original, target_language)
        elif content.content_type == ContentType.TABLE:
            # 如果内容类型为表格，则调用make_table_prompt生成表格翻译提示
            return self.make_table_prompt(content.get_original_as_str(), target_language)

    def make_request(self, prompt):
        """
        根据提示信息生成翻译请求。

        :param prompt: 包含翻译提示信息的字符串。
        :return: 需要子类实现，抛出NotImplementedError表示方法必须在子类中被重写。
        """
        raise NotImplementedError("子类必须实现 make_request 方法")