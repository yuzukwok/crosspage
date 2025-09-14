import os
import random
import string
from dotenv import load_dotenv
from crossword_generator import generate_crossword
from llm_definition import batch_generate_definitions
from crossword_html import generate_crossword_html
from upload_oss import upload_to_oss

def read_words_from_txt(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]
    return words

def random_filename(ext='html', length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length)) + '.' + ext

def main(txt_path):
    # 1. 读取单词
    words = read_words_from_txt(txt_path)
    if not words:
        print('单词列表为空')
        return
    # 2. 生成填字游戏结构
    grid, layout = generate_crossword(words)
    # 3. LLM生成英文解释
    clues = batch_generate_definitions(words)
    # 4. 生成随机文件名
    html_name = random_filename()
    # 5. 生成HTML
    generate_crossword_html(grid, layout, clues, output_file=html_name)
    # 6. 上传到OSS
    url = upload_to_oss(html_name)
    print('最终访问地址:', url)
    return url

if __name__ == '__main__':
    # 假设单词列表文件为 words.txt
    main('words.txt')
