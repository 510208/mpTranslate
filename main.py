import os
import sys
from googletrans import Translator
import argparse
import json
import yaml
import logging
import tqdm
from opencc import OpenCC
import re

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

# 逐行書出ASCII LOGO
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
# 參數二選一：
# --json [路徑] 或 --yaml [路徑]
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--json', help='輸入文件為 JSON 格式')
group.add_argument('--yaml', help='輸入文件為 YAML 格式')
# 參數二選一，預設為--en2zt：
# --en2zt 或 --zs2zt
group2 = parser.add_mutually_exclusive_group(required=True)
group2.add_argument('--en2zt', help='由英文翻譯為繁體中文', action='store_true')
group2.add_argument('--zs2zt', help='由簡體中文翻譯為繁體中文', action='store_true')
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

# 輸入文件路徑
input_file_path = args.json if args.json else args.yaml

# 輸出文件路徑：默認為 output/ 資料夾下的輸入文件名稱，如果有指定 --output 參數，則使用指定的路徑
output_file_path = args.output if args.output else f'output/{input_file_path.split("/")[-1]}'

# Log檔案路徑：如果有指定 --log 參數，則使用指定的路徑，否則直接顯示到終端
# 初始化日誌
if args.log:
    logging.info(f'設定輸出檔案，並不再繼續顯示：\n{args.log}')
    log_file_path = args.log if args.log else f'log/{input_file_path.split("/")[-1]}.log'
    logging.basicConfig(filename=log_file_path)


# -----------
# 讀取文件
# -----------
logging.info(f'讀取文件：{input_file_path}')
with open(input_file_path, 'r', encoding='utf-8') as f:
    if args.json:
        data = json.load(f)
    elif args.yaml:
        data = yaml.safe_load(f)

# -----------
# 翻譯
# -----------
# 初始化翻譯器，使其偵測原始語言並只翻譯成繁體中文
translator = Translator()
translator.raise_Exception = True
translator.detect_language = True
translator.from_lang = 'auto'
translator.to_lang = 'zh-tw'

# 初始化OpenCC
cc = OpenCC('s2t')

# 開始翻譯
logging.info('開始翻譯...')
def translate(item):
    if isinstance(item, dict):
        return {k: translate(v) for k, v in item.items()}
    elif isinstance(item, list):
        return [translate(element) for element in item]
    elif isinstance(item, str):
        if item.strip():  # 檢查 item 是否為空
            # 使用正則表達式找到 placeholder，並將其暫時替換為特殊標記
            placeholders = re.findall(r'%\w+%', item)
            placeholder_map = {ph: ph for ph in placeholders}  # 使用原始名稱作為 map 的值
            item_temp = item
            for ph, ph_temp in placeholder_map.items():
                item_temp = item_temp.replace(ph, ph_temp)
            # 進行翻譯
            try:
                translated_text = translator.translate(item_temp, dest='zh-tw').text
            except Exception as e:
                logging.error(f"Error translating text: {e}")
                translated_text = item
            # 將翻譯的文本中的 placeholder 還原回來
            for ph, ph_temp in placeholder_map.items():
                translated_text = translated_text.replace(ph_temp, ph)
            return translated_text
        else:
            return item
    else:
        return item

for key, value in tqdm.tqdm(data.items()):
    # 翻譯
    try:
        if args.en2zt:
            data[key] = translate(value)
        elif args.zs2zt:
            data[key] = cc.convert(value)
    except Exception as e:
        logging.error(f'翻譯失敗：{key} - {value}')
        logging.error(e)

# -----------
# 寫入文件
# -----------
# 先檢查目標檔案是否存在，否的話就建立該檔案，是的話就繼續

# 寫入文件
logging.info(f'寫入文件：{output_file_path}')
with open(output_file_path, 'w', encoding='utf-8') as f:
    if args.json:
        json.dump(data, f, ensure_ascii=False, indent=4)
    elif args.yaml:
        # 寫入時要保留原本的註解
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

logging.info('翻譯完成！')
sys.exit(0)