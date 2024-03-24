import pandas as pd
from enum import Enum, auto
from PIL import Image as PILImage
from utils import LOG
import io

# 定义内容类型枚举，包括文本、表格和图片
class ContentType(Enum):
    TEXT = auto()
    TABLE = auto()
    IMAGE = auto()

# 定义内容类，包含原始内容、翻译内容及其类型和状态
class Content:
    def __init__(self, content_type, original, translation=None):
        """
        初始化内容对象。
        
        :param content_type: 内容类型（文本、表格、图片）。
        :param original: 原始内容。
        :param translation: 翻译内容（默认为None）。
        """
        self.content_type = content_type
        self.original = original
        self.translation = translation
        self.status = False

    def set_translation(self, translation, status):
        """
        设置翻译内容并更新状态。
        
        :param translation: 翻译后的内容。
        :param status: 翻译的状态（True表示成功）。
        :raises ValueError: 当翻译类型与期望类型不匹配时抛出。
        """
        if not self.check_translation_type(translation):
            raise ValueError(f"Invalid translation type. Expected {self.content_type}, but got {type(translation)}")
        self.translation = translation
        self.status = status

    def check_translation_type(self, translation):
        """
        检查翻译内容的类型是否匹配。
        
        :param translation: 待检查的翻译内容。
        :return: 布尔值，类型匹配返回True，否则返回False。
        """
        if self.content_type == ContentType.TEXT and isinstance(translation, str):
            return True
        elif self.content_type == ContentType.TABLE and isinstance(translation, list):
            return True
        elif self.content_type == ContentType.IMAGE and isinstance(translation, PILImage.Image):
            return True
        return False


# 表格内容类，继承自内容类，提供针对表格内容的特定操作
class TableContent(Content):
    def __init__(self, data, translation=None):
        """
        初始化表格内容对象。
        
        :param data: 表格数据，二维列表形式。
        :param translation: 翻译后的表格数据（默认为None）。
        :raises ValueError: 当给定数据与创建的DataFrame对象的行和列数不匹配时抛出。
        """
        df = pd.DataFrame(data)

        # 验证数据中的行和列数是否与DataFrame对象匹配
        if len(data) != len(df) or len(data[0]) != len(df.columns):
            raise ValueError("The number of rows and columns in the extracted table data and DataFrame object do not match.")
        
        super().__init__(ContentType.TABLE, df)

    def set_translation(self, translation, status):
        """
        设置翻译后的表格内容并更新状态。
        
        :param translation: 翻译后的表格内容，字符串形式。
        :param status: 翻译的状态（True表示成功）。
        :raises ValueError: 当翻译类型不为字符串时抛出。
        """
        try:
            if not isinstance(translation, str):
                raise ValueError(f"Invalid translation type. Expected str, but got {type(translation)}")

            LOG.debug(translation)
            # 将字符串转换为列表的列表形式
            # table_data = [row.strip().split(',') for row in translation.strip().split('\n')]
            # LOG.debug(translation)
            # 从table_data创建read_csv
            # translated_df = pd.DataFrame(translation)
            csv_file_like = io.StringIO(translation)
            LOG.debug(csv_file_like)
            
            translated_df = pd.read_csv(csv_file_like)

            LOG.debug(translated_df)
            self.translation = translated_df
            self.status = status
        except Exception as e:
            LOG.error(f"An error occurred during table translation: {e}")
            self.translation = None
            self.status = False

    def __str__(self):
        """
        返回原始表格内容的字符串表示。
        
        :return: 表格的字符串表示。
        """
        return self.original.to_string(header=False, index=False)

    def iter_items(self, translated=False):
        """
        遍历表格内容项。
        
        :param translated: 是否遍历翻译后的表格内容（默认为False，即遍历原始内容）。
        :return: 表格内容项的迭代器。
        """
        target_df = self.translation if translated else self.original
        for row_idx, row in target_df.iterrows():
            for col_idx, item in enumerate(row):
                yield (row_idx, col_idx, item)

    def update_item(self, row_idx, col_idx, new_value, translated=False):
        """
        更新表格中的内容项。
        
        :param row_idx: 行索引。
        :param col_idx: 列索引。
        :param new_value: 新值。
        :param translated: 是否更新翻译后的表格内容（默认为False，即更新原始内容）。
        """
        target_df = self.translation if translated else self.original
        target_df.at[row_idx, col_idx] = new_value

    def get_original_as_str(self):
        """
        返回原始表格内容的字符串表示。
        
        :return: 原始表格的字符串表示。
        """
        return self.original.to_string(header=False, index=False)