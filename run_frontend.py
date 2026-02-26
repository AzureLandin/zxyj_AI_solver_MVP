#!/usr/bin/env python3
"""
简单HTTP服务器，用于运行前端页面
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

# 配置
PORT = 8000
FRONTEND_DIR: Path = Path(__file__).parent / "frontend"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)
    
    def end_headers(self):
        # 添加CORS头，允许跨域请求
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def run_server():
    """运行前端服务器"""
    os.chdir(FRONTEND_DIR)
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"\n{'='*60}")
        print(f"前端服务器已启动")
        print(f"访问地址: http://localhost:{PORT}")
        print(f"前端目录: {FRONTEND_DIR}")
        print(f"{'='*60}\n")
        print("提示：请确保后端Flask服务器也在运行")
        print("后端启动命令: python backend/app.py")
        print(f"{'='*60}\n")
        
        # 自动打开浏览器
        try:
            webbrowser.open(f'http://localhost:{PORT}')
        except Exception as e:
            print(f"无法自动打开浏览器: {e}")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")

if __name__ == '__main__':
    run_server()
