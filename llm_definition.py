import os
import requests
from typing import List, Dict
from dotenv import load_dotenv


# 加载.env文件
load_dotenv()


DASHSCOPE_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
DASHSCOPE_MODEL = os.getenv("DASHSCOPE_MODEL", "qwen-turbo")
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
    "Content-Type": "application/json"
}

def get_simple_english_definition(word: str) -> str:
    prompt = f"Explain the word '{word}' in simple English for elementary school students. Only return the explanation, do not repeat the word."
    data = {
        "model": DASHSCOPE_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful English teacher for children."},
            {"role": "user", "content": prompt}
        ]
    }
    resp = requests.post(DASHSCOPE_API_URL, headers=HEADERS, json=data, timeout=20)
    resp.raise_for_status()
    result = resp.json()
    # 兼容通义千问 OpenAI 兼容接口格式
    try:
        return result["choices"][0]["message"]["content"].strip()
    except Exception:
        return str(result)

def batch_generate_definitions(words: List[str]) -> Dict[str, str]:
    definitions = {}
    for word in words:
        try:
            definitions[word] = get_simple_english_definition(word)
        except Exception as e:
            definitions[word] = f"[Error: {e}]"
    return definitions

if __name__ == "__main__":
    words = ['apple', 'banana', 'orange', 'grape', 'pear', 'peach']
    defs = batch_generate_definitions(words)
    for w, d in defs.items():
        print(f"{w}: {d}")
