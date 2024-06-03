"""
===== 中文格式轉換器 =====
此模組用以將簡體中文轉換為繁體中文。
1. convert(text)：接受一個字符串，返回轉換結果。
2. parse_array(array)：接受一個陣列，並對陣列中的每個元素進行轉換。
3. global_translate(content)：接受一個字典，並對字典中的每個值進行轉換。
=========================
"""

import re
import opencc
import logging

logger = logging.getLogger(__name__)

# 定義簡繁轉換器
cc = opencc.OpenCC('s2t')

# 接受一個字符串，返回轉換結果
def convert(text):
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
    # 執行轉換
    try:
        result = cc.convert(text)
        logger.info(f'轉換成功：{result.text}')
        return result.text
    except Exception as e:
        logger.error(f'轉換失敗：{e}')
        return None