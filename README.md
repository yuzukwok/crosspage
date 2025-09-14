# Crossword Generator

一个自动生成填字游戏的工具，支持 HTML 输出和微信小程序集成。

## 功能特性

- 自动生成填字游戏网格和布局
- 支持横向和纵向单词
- 生成 HTML 版本，支持打印适配 A4 纸
- 集成微信小程序前端
- 使用 LLM 生成单词定义和提示
- 支持批量单词处理

## 安装

1. 克隆项目：
   ```bash
   git clone https://github.com/username/crosspage.git
   cd crosspage
   ```

2. 安装 Python 依赖：
   ```bash
   pip install -r requirements.txt
   ```

   如果没有 `requirements.txt`，请手动安装所需库：
   ```bash
   pip install requests openai  # 示例依赖，请根据代码实际导入的库安装
   ```

3. 配置环境变量：
   - 复制 `.env.example` 到 `.env`
   - 填写必要的 API 密钥等信息

## 使用

### 生成填字游戏

运行主管道：
```bash
python crossword_pipeline.py
```

这将生成 HTML 文件和小程序所需的数据。

### 单独生成 HTML

```python
from crossword_generator import generate_crossword
from crossword_html import generate_crossword_html
from llm_definition import batch_generate_definitions

words = ['apple', 'banana', 'orange']
grid, layout = generate_crossword(words)
clues = batch_generate_definitions(words)
generate_crossword_html(grid, layout, clues, 'output.html')
```

### 微信小程序

进入 `miniprogram/` 目录，使用微信开发者工具打开项目。

## 项目结构

```
crosspage/
├── api_server.py          # API 服务器
├── crossword_generator.py  # 填字游戏生成器
├── crossword_html.py       # HTML 生成器
├── crossword_pipeline.py   # 主处理管道
├── llm_definition.py       # LLM 定义生成
├── upload_oss.py           # OSS 上传工具
├── words.txt               # 单词列表
├── project.config.json     # 项目配置
├── .env                    # 环境变量
├── .gitignore              # Git 忽略文件
├── miniprogram/            # 微信小程序
│   ├── app.js
│   ├── app.json
│   ├── project.config.json
│   ├── project.private.config.json
│   └── pages/
│       └── index/
│           ├── index.js
│           ├── index.wxml
│           └── index.wxss
└── __pycache__/            # Python 缓存
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License