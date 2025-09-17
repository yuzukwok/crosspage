#!/usr/bin/env python3
"""
简单的HTTP服务器用于提供配置界面
"""
import http.server
import socketserver
import os
import json
from urllib.parse import urlparse, parse_qs
import threading
import webbrowser

PORT = 3000

class ConfigHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 处理根路径，返回配置界面
        if self.path == '/' or self.path == '/config':
            self.path = '/config.html'
        
        # 调用父类的GET处理方法
        return super().do_GET()
    
    def do_POST(self):
        # 处理配置相关的POST请求
        if self.path == '/api/generate-html':
            self.handle_generate_html()
        else:
            self.send_error(404, "Not Found")
    
    def handle_generate_html(self):
        """处理HTML生成请求"""
        try:
            # 读取请求数据
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # 导入必要的模块
            from crossword_html import generate_crossword_html
            import tempfile
            
            # 提取参数
            grid = data.get('grid')
            layout = data.get('layout')
            clues = data.get('clues')
            style = data.get('style', 'classic')
            
            if not all([grid, layout, clues]):
                self.send_error(400, "Missing required data")
                return
            
            # 生成HTML文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                generate_crossword_html(grid, layout, clues, f.name, style)
                html_file = f.name
            
            # 读取生成的HTML内容
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # 清理临时文件
            os.unlink(html_file)
            
            # 返回HTML内容
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Content-Disposition', f'attachment; filename="crossword-{style}.html"')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")
    
    def end_headers(self):
        # 添加CORS头部
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def run_server():
    """运行配置服务器"""
    with socketserver.TCPServer(("", PORT), ConfigHandler) as httpd:
        print(f"配置界面服务器运行在 http://localhost:{PORT}")
        print("按 Ctrl+C 停止服务器")
        
        # 自动打开浏览器
        def open_browser():
            webbrowser.open(f'http://localhost:{PORT}')
        
        timer = threading.Timer(1.0, open_browser)
        timer.start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")

if __name__ == "__main__":
    run_server()