# 使用 Google Gemini API 來翻譯Minecraft插件的語系檔
# 使用方法: python main.py <語系檔路徑> <目標語言>

import sys
import os
import google.generativeai as genai
from ruamel.yaml import YAML
import argparse
import logging
# 匯入檔案路徑函式庫
from pathlib import Path
import prompt
import tqdm

# 讀取配置檔案
with open('config.yaml', 'r', encoding='utf-8') as f:
    cfgReader = YAML()
    cfgReader.indent(mapping=2, sequence=4, offset=2)
    cfgReader.preserve_quotes = True
    config = cfgReader.load(f)

API_KEY = config['genai_api_key']

# 配置日誌
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s %(levelname)s][%(name)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M')

logging.getLogger('google.auth.transport.requests').setLevel(logging.INFO)
logging.getLogger('google.auth.transport.requests').propagate = False

# 取得當前路徑
logging.info("取得當前路徑")
current_path = Path(__file__).parent
logging.info(f'當前路徑: {current_path}')

# 解析命令行參數
logging.info("解析命令行引數")

parser = argparse.ArgumentParser(
    description='mptranslate：使用 Google Gemini API 來翻譯Minecraft插件的語系檔'
)

parser.add_argument('--input', '-i', type=str, help='語系檔路徑', required=True)
# 輸出預設為當前路徑下的output資料夾
parser.add_argument('--output', '-o', type=str, help='輸出語系檔路徑', required=False, default=current_path / 'output')
parser.add_argument('--target', '-t', type=str, help='目標語言', required=False, default='zh-TW')
args = parser.parse_args()

# 定義常數
INPUT_PATH = Path(args.input)
OUTPUT_PATH = Path(args.output)
TARGET_LANGUAGE = args.target

logging.info("解析命令行引數完成")
logging.info(f'輸入語系檔路徑: {INPUT_PATH}')
logging.info(f'輸出語系檔路徑: {OUTPUT_PATH}')
logging.info(f'目標語言: {TARGET_LANGUAGE}')

# 檢查輸入語系檔是否為yaml格式的檔案
if INPUT_PATH.suffix != '.yaml':
    logging.error(f'輸入語系檔不是yaml格式的檔案: {INPUT_PATH}')
    sys.exit(1)
elif not INPUT_PATH.exists():
    # 檢查輸入語系檔是否存在
    logging.error(f'輸入語系檔不存在: {INPUT_PATH}')
    sys.exit(1)

# 讀取輸入語系檔
logging.info("讀取輸入語系檔")
yaml = YAML()
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.preserve_quotes = True

with open(INPUT_PATH, 'r', encoding='utf-8') as f:
    data = yaml.load(f)

logging.info("讀取輸入語系檔完成")

# 開始執行翻譯

# 初始化prompt
logging.info("初始化prompt")
p = prompt.prompt(TARGET_LANGUAGE)
logging.info(f"初始化prompt完成，prompt如下：{p.short_prompts}")

# 初始化Google Gemini API
logging.info("初始化Google Gemini API")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(name='gemini-1.5-flash')

# 初始化進度條
logging.info("初始化tqdm進度條")

def translate(inputitem: str):
    # 翻譯單個字串
    response = model.generate_content(p.short_prompts + "\n" + inputitem)
    # 取得翻譯結果
    result = response.text.split('\n')
    # 回傳翻譯結果
    return result[1]

# 開始翻譯
logging.info("開始翻譯")
while True:
    # 先製作20個字串，再一次翻譯
    # 定義累積字串
    accum = ""
    # 定義翻譯結果
    result = {}
    # 取得前20個字串加入accum，如果選到的不是字串，就先轉成字串並加入accum
    for i in range(20):
        key = list(data.keys())[i]
        if type(data[key]) != str:
            accum += str(data[key]) + '\n'
        else:
            accum += data[key] + '\n'
        result[key] = data[key]
    
    # 叫用translate翻譯
    logging.info(f"叫用translate翻譯，內容：\n{accum}")
    response = translate(accum)

    # 分割翻譯結果
    response = response.split('\n')

    # 將翻譯結果放入data
    for i in range(len(response)):
        key = list(result.keys())[i]
        data[key] = response[i]
    
    # 如果data為空，就break
    if len(data) == 0:
        break