import os
import sys
from googletrans import Translator
import argparse
import yaml
import logging
import tqdm
from opencc import OpenCC
import re
import translater
import simpcc

VERSION = '0.1'
ASCII_LOGO = r"""

               _______                  _       _       
              |__   __|                | |     | |      
  _ __ ___  _ __ | |_ __ __ _ _ __  ___| | __ _| |_ ___ 
 | '_ ` _ \| '_ \| | '__/ _` | '_ \/ __| |/ _` | __/ _ \
 | | | | | | |_) | | | | (_| | | | \__ \ | (_| | ||  __/
 |_| |_| |_| .__/|_|_|  \__,_|_| |_|___/_|\__,_|\__\___|
           | |                                          
           |_|                                          

"""

# 初始化日志
logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(name)s][%(levelname)s] %(message)s')

# 逐行輸出ASCII LOGO
for line in ASCII_LOGO.split('\n'):
    logging.info(line)
logging.info('Minecraft 模組語言文件翻譯工具')
logging.info('作者：SamHacker')
logging.info(f'版本：{VERSION}')

# 初始化argparse
# 讓argparse的help信息更加友好且顯示繁體中文
class ChineseHelpFormatter(argparse.HelpFormatter):
    def __init__(self, prog):
        super(ChineseHelpFormatter, self).__init__(prog, max_help_position=27, width=120)

    def _split_lines(self, text, width):
        if text.startswith('輸入文件'):
            return text.splitlines()
        return super(ChineseHelpFormatter, self)._split_lines(text, width)

# class ChineseArgumentParser(argparse.ArgumentParser):
#     def __init__(self, *args, **kwargs):
#         super(ChineseArgumentParser, self).__init__(*args, **kwargs)
#         self.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='顯示此幫助訊息並退出')
#         self.add_argument('--ver', action='version', version='%(prog)s 0.1', help='顯示程式的版本號並退出')

# parser = ChineseArgumentParser(description='翻譯 Minecraft 模組的語言文件；由 SamHacker 基於 Python 實現', formatter_class=ChineseHelpFormatter)
    
parser = argparse.ArgumentParser(description='翻譯 Minecraft 模組的語言文件；由 SamHacker 基於 Python 實現', formatter_class=ChineseHelpFormatter)
# parser = argparse.ArgumentParser(description='翻譯 Minecraft 模組的語言文件；由 SamHacker 基於 Python 實現')
# 定義關於，顯示作者資訊
parser.add_argument('--about', help='顯示作者資訊', action='store_true')
# 定義版本，顯示版本資訊
parser.add_argument('--ver', action='version', version='%(prog)s 0.1')
# 強制性參數： --yaml [路徑]
parser.add_argument('--yaml', help='輸入文件的路徑', required=True)
# 選擇性參數： --output [路徑]
parser.add_argument('--output', help='輸出文件的路徑，默認為 output/ 資料夾下的輸入文件名稱')
# 選擇性參數： Log檔案路徑
# --log [路徑]
parser.add_argument('--log', help='Log檔案的路徑，默認為 log/ 資料夾下的輸入文件名稱.log')

# 檢查是否有 --about 參數，如果有，則顯示作者資訊
if '--about' in sys.argv:
    logging.info(ASCII_LOGO)
    logging.info('Minecraft 模組語言文件翻譯工具')
    logging.info('作者：SamHacker')
    logging.info(f'版本：{VERSION}')
    sys.exit(0)

# 檢查如果沒有任何參數，則顯示幫助信息
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

# 解析參數
args = parser.parse_args()

# -----------
# 處理參數
# -----------

# 處理輸入參數
impath = args.yaml
# 處理輸出參數
if args.output is None:
    opath = os.path.join('output', os.path.basename(impath))
else:
    opath = args.output

# 處理Log參數
if args.log is None:
    logpath = os.path.join('log', os.path.basename(impath) + '.log')
else:
    logpath = args.log

# 輸出參數信息
logging.info(f'輸入文件：{impath}')
logging.info(f'輸出文件：{opath}')
logging.info(f'Log文件：{logpath}')

# -----------
# 開始翻譯
# -----------

# 讀取yaml文件
with open(impath, 'r', encoding='utf-8') as f:
    content = yaml.load(f, Loader=yaml.FullLoader)

# simpcc.convert用以轉換繁簡中文
# translater.translate用以翻譯英文

# 遍覽content，對每個value進行翻譯
for key, value in content.items():
    # 檢查value是否是字典
    if isinstance(value, dict):
        # 對字典中的每個值進行翻譯
        for k, v in value.items():
            # 檢查v的類型
            if isinstance(v, str):
                # 如果v是字符串，就檢查她是簡體中文還是英文
                # 如果是簡體中文，就轉換為繁體中文
                # 如果包含簡體中文，就視為簡體中文
                if re.search(r'[\u4e00-\u9fa5]', v):
                    logging.info(f'鍵{key}的值{v}是簡體中文')
                    content[key][k] = simpcc.convert(v)
                else:
                    logging.info(f'鍵{key}的值{v}是英文')
                    content[key][k] = translater.translate(v)
            elif isinstance(v, list):
                # 如果v是陣列，就調用parse_array
                content[key][k] = translater.parse_array(v)
            elif v is None:
                # 如果v是None，就直接返回None
                content[key][k] = None
            else:
                # 如果v不是字符串，也不是陣列，就直接傳回v
                content[key][k] = v
    elif isinstance(value, list):
        # 如果value是陣列，就調用parse_array
        content[key] = translater.parse_array(value)
    elif value is None:
        # 如果value是None，就直接返回None
        content[key] = None
    else:
        # 如果value不是字典，也不是陣列，就直接傳回value
        content[key] = value

# 寫入yaml文件
# 保留原yaml文件的排列、斷行、縮進與註解
with open(opath, 'w', encoding='utf-8') as f:
    yaml.dump(content, f, allow_unicode=True)