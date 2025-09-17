# Crossword Generator

一个自动生成填字游戏的工具，支持 HTML 输出和微信小程序集成。

## 功能特性

- 🎮 自动生成填字游戏网格和布局
- 📱 支持横向和纵向单词交叉放置
- 🌐 生成 HTML 版本，支持打印适配 A4 纸
- 📝 **全新Web配置界面** - 易用美观的可视化管理工具
- 📱 集成微信小程序前端
- 🤖 使用 LLM 生成单词定义和提示
- 📊 支持批量单词处理
- 🎨 **多种HTML样式** - 经典、现代、简约、报纸四种风格

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

### 🎯 Web配置界面（推荐）

我们提供了一个易用美观的Web配置界面，让您可以轻松创建和自定义填字游戏：

1. **启动服务**：
   ```bash
   # 安装依赖
   pip install -r requirements.txt
   
   # 启动API服务器
   python api_server.py
   
   # 在另一个终端启动配置界面服务器
   python -m http.server 3000
   ```

2. **使用配置界面**：
   - 访问 `http://localhost:3000/config.html`
   - 导入词表文件或手动输入单词
   - 选择HTML样式（经典、现代、简约、报纸）
   - 预览生成的填字游戏
   - 编辑题目描述
   - 一键导出HTML文件

**主要特性**：
- 📝 支持文件拖拽导入词表
- 🎨 四种预定义HTML样式
- 👀 实时预览填字游戏
- ✏️ 在线编辑题目描述
- 📥 一键导出完整HTML文件
- 🔧 灵活的配置选项

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
generate_crossword_html(grid, layout, clues, 'output.html', 'modern')
```

### 微信小程序

进入 `miniprogram/` 目录，使用微信开发者工具打开项目。

## 项目结构

```
crosspage/
├── api_server.py          # API 服务器
├── crossword_generator.py  # 填字游戏生成器
├── crossword_html.py       # HTML 生成器（新增）
├── crossword_pipeline.py   # 主处理管道
├── config.html            # Web配置界面（新增）
├── llm_definition.py       # LLM 定义生成
├── upload_oss.py           # OSS 上传工具
├── requirements.txt        # Python依赖（新增）
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