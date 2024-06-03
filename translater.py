"""
===== 英文轉中文翻譯器 =====
這個模塊提供了一個簡單的翻譯器，可以將英文翻譯成中文。
這個模塊提供了三個函數：
1. translate(text, dest='zh-TW')：接受一個字符串，返回翻譯結果。
2. parse_array(array)：接受一個陣列，並對陣列中的每個元素進行翻譯。
3. global_translate(content)：接受一個字典，並對字典中的每個值進行翻譯。
=========================
"""

import re
from googletrans import Translator
import logging

logger = logging.getLogger(__name__)

translator = Translator()

# 接受一個字符串，返回翻譯結果
def translate(text:str, dest='zh-TW'):
    # 如果text不是字串型別，擲回一個自訂錯誤
    if not isinstance(text, str):
        logger.error('text必須是字符串')
        raise TypeError('text必須是字符串')
    # 如果text是空字符串，直接返回空字符串
    if text == '':
        logger.warning('text是空字符串')
        return ''
    # 如果text是None，直接返回None
    if text is None:
        logger.warning('text是None')
        return None
    # 執行翻譯
    try:
        result = translator.translate(text, dest=dest)
        logger.info(f'翻譯成功：{result.text}')
        return result.text
    except Exception as e:
        logger.error(f'翻譯失敗：{e}')
        return None

# 接受一個陣列，並對陣列中的每個元素進行翻譯
# 如果陣列中的元素也是陣列，就重複呼叫自己直到他是字符串
def parse_array(array):
    # 檢查array是否是陣列
    if not isinstance(array, list):
        logger.error('array必須是陣列')
        raise TypeError('array必須是陣列')
    # 如果array是空陣列，直接返回空陣列
    if array == []:
        logger.warning('array是空陣列')
        return []
    # 如果array是None，直接返回None
    if array is None:
        logger.warning('array是None')
        return None
    # 對array中的每個元素進行翻譯
    result = []
    for item in array:
        # 如果item是陣列，就遞迴呼叫自己
        if isinstance(item, list):
            result.append(parse_array(item))
        # 如果item是字符串，就翻譯
        elif isinstance(item, str):
            result.append(translate(item))
        # 如果item是None，就直接返回None
        elif item is None:
            result.append(None)
        # 如果item不是字符串，也不是陣列，就擲回一個自訂錯誤
        else:
            logger.error('array中的元素必須是字符串或陣列')
            raise TypeError('array中的元素必須是字符串或陣列')
    return result

# def global_translate(content: dict):
#     # 檢查content是否是字典
#     if not isinstance(content, dict):
#         logger.error('content必須是字典')
#         raise TypeError('content必須是字典')
#     # 如果content是空字典，直接返回空字典
#     if content == {}:
#         logger.warning('content是空字典')
#         return {}
#     # 如果content是None，直接返回None
#     if content is None:
#         logger.warning('content是None')
#         return None
#     # 對content中的每個值進行翻譯
#     result = {}
#     # 遍歷content中的每個鍵值對
#     for key, value in content.items():
#         # 如果value是字典，就遞迴呼叫自己
#         if isinstance(value, dict):
#             result[key] = global_translate(value)
#         # 如果value是陣列，就調用parse_array
#         elif isinstance(value, list):
#             result[key] = parse_array(value)
#         # 如果value是字符串，就翻譯
#         elif isinstance(value, str):
#             result[key] = translate(value)
#         # 如果value是None，就直接返回None
#         elif value is None:
#             result[key] = None
#         # 如果value不是字符串，也不是字典，也不是陣列，就擲回一個自訂錯誤
#         else:
#             logger.error('content中的值必須是字符串、字典或陣列')
#             raise TypeError('content中的值必須是字符串、字典或陣列')
#     return result