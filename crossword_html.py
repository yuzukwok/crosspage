from typing import List, Dict
import json

def generate_crossword_html(grid: List[List[str]], layout: List[Dict], clues: Dict[str, str], 
                           output_file: str = 'crossword.html', style: str = 'classic'):
    """
    生成填字游戏HTML文件
    
    Args:
        grid: 填字游戏网格
        layout: 单词布局信息
        clues: 单词提示信息
        output_file: 输出文件名
        style: HTML样式 ('classic', 'modern', 'minimal', 'newspaper')
    """
    size = len(grid)
    
    # 生成HTML内容
    html_content = generate_html_template(grid, layout, clues, size, style)
    
    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"填字游戏HTML已生成: {output_file}")

def generate_html_template(grid: List[List[str]], layout: List[Dict], 
                          clues: Dict[str, str], size: int, style: str = 'classic'):
    """生成HTML模板"""
    
    # 计算题目编号
    numbered_layout = []
    num_counter = 1
    for entry in layout:
        entry_copy = entry.copy()
        entry_copy['number'] = num_counter
        numbered_layout.append(entry_copy)
        num_counter += 1
    
    # 分离横向和纵向题目
    across_clues = []
    down_clues = []
    for entry in numbered_layout:
        clue_text = clues.get(entry['word'].lower(), entry['word'])
        clue_info = {
            'number': entry['number'],
            'word': entry['word'],
            'clue': clue_text,
            'row': entry['row'],
            'col': entry['col']
        }
        
        if entry['direction'] == 'across':
            across_clues.append(clue_info)
        else:
            down_clues.append(clue_info)
    
    # 选择样式
    css_styles = get_css_styles(style)
    
    # 生成网格HTML
    grid_html = generate_grid_html(grid, numbered_layout, size)
    
    # 生成题目列表HTML
    clues_html = generate_clues_html(across_clues, down_clues)
    
    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>填字游戏</title>
    <style>
        {css_styles}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>填字游戏</h1>
            <div class="controls">
                <button onclick="checkAnswers()" class="btn btn-primary">检查答案</button>
                <button onclick="clearAll()" class="btn btn-secondary">清空</button>
                <button onclick="showAnswers()" class="btn btn-info">显示答案</button>
            </div>
        </header>
        
        <div class="game-area">
            <div class="grid-container">
                {grid_html}
            </div>
            
            <div class="clues-container">
                {clues_html}
            </div>
        </div>
    </div>
    
    <script>
        {generate_javascript(grid, numbered_layout)}
    </script>
</body>
</html>"""
    
    return html_template

def generate_grid_html(grid: List[List[str]], layout: List[Dict], size: int):
    """生成网格HTML"""
    # 创建编号映射
    number_map = {}
    for entry in layout:
        key = f"{entry['row']}-{entry['col']}"
        if key not in number_map:
            number_map[key] = entry['number']
    
    grid_html = f'<div class="crossword-grid" style="grid-template-columns: repeat({size}, 1fr);">'
    
    for r in range(size):
        for c in range(size):
            cell_value = grid[r][c]
            cell_key = f"{r}-{c}"
            
            if cell_value:  # 有字母的格子
                number = number_map.get(cell_key, '')
                number_html = f'<span class="cell-number">{number}</span>' if number else ''
                
                grid_html += f'''
                <div class="cell" data-row="{r}" data-col="{c}" data-answer="{cell_value}">
                    {number_html}
                    <input type="text" maxlength="1" class="cell-input" 
                           oninput="handleInput(this)" onkeydown="handleKeydown(event, this)">
                </div>'''
            else:  # 黑色格子
                grid_html += '<div class="cell cell-black"></div>'
    
    grid_html += '</div>'
    return grid_html

def generate_clues_html(across_clues: List[Dict], down_clues: List[Dict]):
    """生成题目列表HTML"""
    clues_html = '<div class="clues-section">'
    
    # 横向题目
    clues_html += '<div class="clues-group"><h3>横向</h3><ul class="clues-list">'
    for clue in across_clues:
        clues_html += f'<li><span class="clue-number">{clue["number"]}.</span> {clue["clue"]}</li>'
    clues_html += '</ul></div>'
    
    # 纵向题目
    clues_html += '<div class="clues-group"><h3>纵向</h3><ul class="clues-list">'
    for clue in down_clues:
        clues_html += f'<li><span class="clue-number">{clue["number"]}.</span> {clue["clue"]}</li>'
    clues_html += '</ul></div>'
    
    clues_html += '</div>'
    return clues_html

def generate_javascript(grid: List[List[str]], layout: List[Dict]):
    """生成JavaScript代码"""
    grid_json = json.dumps(grid)
    layout_json = json.dumps(layout)
    
    return f"""
        const GRID = {grid_json};
        const LAYOUT = {layout_json};
        
        function handleInput(input) {{
            input.value = input.value.toUpperCase();
            if (input.value) {{
                moveToNext(input);
            }}
        }}
        
        function handleKeydown(event, input) {{
            if (event.key === 'Backspace' && !input.value) {{
                moveToPrevious(input);
            }} else if (event.key === 'ArrowRight') {{
                event.preventDefault();
                moveToNext(input);
            }} else if (event.key === 'ArrowLeft') {{
                event.preventDefault();
                moveToPrevious(input);
            }}
        }}
        
        function moveToNext(currentInput) {{
            const cells = Array.from(document.querySelectorAll('.cell-input'));
            const currentIndex = cells.indexOf(currentInput);
            if (currentIndex < cells.length - 1) {{
                cells[currentIndex + 1].focus();
            }}
        }}
        
        function moveToPrevious(currentInput) {{
            const cells = Array.from(document.querySelectorAll('.cell-input'));
            const currentIndex = cells.indexOf(currentInput);
            if (currentIndex > 0) {{
                cells[currentIndex - 1].focus();
            }}
        }}
        
        function checkAnswers() {{
            let correct = 0;
            let total = 0;
            
            document.querySelectorAll('.cell').forEach(cell => {{
                const input = cell.querySelector('.cell-input');
                if (input) {{
                    total++;
                    const answer = cell.dataset.answer;
                    const userInput = input.value.toUpperCase();
                    
                    cell.classList.remove('correct', 'incorrect');
                    
                    if (userInput === answer) {{
                        correct++;
                        cell.classList.add('correct');
                    }} else if (userInput) {{
                        cell.classList.add('incorrect');
                    }}
                }}
            }});
            
            alert(`正确: ${{correct}}/${{total}}`);
        }}
        
        function clearAll() {{
            document.querySelectorAll('.cell-input').forEach(input => {{
                input.value = '';
                input.parentElement.classList.remove('correct', 'incorrect');
            }});
        }}
        
        function showAnswers() {{
            document.querySelectorAll('.cell').forEach(cell => {{
                const input = cell.querySelector('.cell-input');
                if (input) {{
                    input.value = cell.dataset.answer;
                    cell.classList.add('correct');
                    cell.classList.remove('incorrect');
                }}
            }});
        }}
    """

def get_css_styles(style: str = 'classic'):
    """获取CSS样式"""
    base_styles = """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            background: #f5f5f5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
        }
        
        .controls {
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .btn-primary {
            background: #007bff;
            color: white;
        }
        
        .btn-primary:hover {
            background: #0056b3;
        }
        
        .btn-secondary {
            background: #6c757d;
            color: white;
        }
        
        .btn-secondary:hover {
            background: #545b62;
        }
        
        .btn-info {
            background: #17a2b8;
            color: white;
        }
        
        .btn-info:hover {
            background: #138496;
        }
        
        .game-area {
            display: grid;
            grid-template-columns: 1fr 300px;
            gap: 30px;
            align-items: start;
        }
        
        @media (max-width: 768px) {
            .game-area {
                grid-template-columns: 1fr;
            }
        }
        
        .crossword-grid {
            display: grid;
            gap: 2px;
            background: #333;
            border: 2px solid #333;
            justify-content: center;
            max-width: 600px;
            margin: 0 auto;
        }
        
        .cell {
            width: 40px;
            height: 40px;
            position: relative;
            background: white;
        }
        
        .cell-black {
            background: #333;
        }
        
        .cell-number {
            position: absolute;
            top: 2px;
            left: 2px;
            font-size: 10px;
            font-weight: bold;
            line-height: 1;
            z-index: 1;
        }
        
        .cell-input {
            width: 100%;
            height: 100%;
            border: none;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            text-transform: uppercase;
            background: transparent;
        }
        
        .cell-input:focus {
            outline: 2px solid #007bff;
            background: #e3f2fd;
        }
        
        .cell.correct {
            background: #d4edda;
        }
        
        .cell.incorrect {
            background: #f8d7da;
        }
        
        .clues-container {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .clues-group h3 {
            margin-bottom: 15px;
            color: #333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 5px;
        }
        
        .clues-list {
            list-style: none;
            margin-bottom: 25px;
        }
        
        .clues-list li {
            margin-bottom: 8px;
            padding: 8px;
            border-radius: 4px;
            transition: background 0.2s ease;
        }
        
        .clues-list li:hover {
            background: #f8f9fa;
        }
        
        .clue-number {
            font-weight: bold;
            color: #007bff;
            margin-right: 5px;
        }
    """
    
    # 根据不同样式添加特定CSS
    if style == 'modern':
        base_styles += """
        .header h1 {
            background: linear-gradient(45deg, #007bff, #17a2b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .crossword-grid {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .cell {
            border-radius: 3px;
        }
        """
    elif style == 'minimal':
        base_styles += """
        body {
            background: white;
        }
        
        .header h1 {
            color: #333;
            font-weight: 300;
        }
        
        .crossword-grid {
            border: 1px solid #ddd;
            background: #ddd;
        }
        
        .clues-container {
            box-shadow: none;
            border: 1px solid #ddd;
        }
        """
    elif style == 'newspaper':
        base_styles += """
        body {
            font-family: 'Times New Roman', serif;
            background: #fefefe;
        }
        
        .header h1 {
            font-family: 'Times New Roman', serif;
            color: #333;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .crossword-grid {
            border: 3px solid #000;
            background: #000;
        }
        
        .cell {
            border: 1px solid #000;
        }
        
        .clues-container {
            background: #fefefe;
            border: 2px solid #333;
        }
        
        .clues-group h3 {
            font-family: 'Times New Roman', serif;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        """
    
    return base_styles

if __name__ == "__main__":
    # 测试示例
    from crossword_generator import generate_crossword
    from llm_definition import batch_generate_definitions
    
    words = ['apple', 'banana', 'orange']
    grid, layout = generate_crossword(words)
    clues = {'apple': 'A red or green fruit', 'banana': 'A yellow curved fruit', 'orange': 'A citrus fruit'}
    
    generate_crossword_html(grid, layout, clues, 'test_crossword.html', 'classic')