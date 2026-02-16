#!/usr/bin/env python3
"""
AI解题助手 - 快速启动脚本
适用于Windows双击运行
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def print_header():
    print("=" * 60)
    print("   AI解题助手 - 快速启动")
    print("=" * 60)
    print()

def check_python():
    """检查Python环境"""
    print("检查Python环境...")
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        print(f"  {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"错误: 未找到Python - {e}")
        print("请先安装Python 3.7+")
        input("按回车键退出...")
        return False

def setup_env():
    """创建.env配置文件"""
    env_file = Path("backend/.env")
    example_file = Path("backend/.env.example")
    
    if not env_file.exists():
        print("创建后端配置文件...")
        if example_file.exists():
            import shutil
            shutil.copy(example_file, env_file)
            print(f"  已创建 {env_file}")
            print("\n  注意: 请编辑 backend\.env 文件，填写你的AI API密钥")
            print("  否则无法使用AI解题功能")
            return False
        else:
            print(f"  错误: 找不到 {example_file}")
            return False
    else:
        print(f"  配置文件已存在: {env_file}")
        return True

def check_backend_dependency():
    """检查后端的依赖"""
    print("\n检查后端依赖...")
    try:
        import flask
        import openai
        print("  ✓ Flask 已安装")
        print("  ✓ OpenAI SDK 已安装")
        return True
    except ImportError as e:
        print(f"  ✗ 缺少依赖: {e}")
        print("\n  请先在终端运行: pip install -r backend/requirements.txt")
        return False

def show_menu():
    """显示菜单"""
    print("\n" + "=" * 60)
    print("请选择启动方式：")
    print("  1. 同时启动前后端（推荐）")
    print("  2. 仅启动后端")
    print("  3. 仅启动前端")
    print("  4. 安装后端依赖")
    print("  5. 退出")
    print("=" * 60)
    print()
    
    try:
        choice = input("请输入选项 (1-5): ").strip()
        return choice
    except KeyboardInterrupt:
        print("\n\n退出程序")
        sys.exit(0)

def start_backend():
    """启动后端"""
    print("\n启动后端服务...")
    print("  命令: python backend/app.py")
    print("  地址: http://localhost:5000")
    print("\n" + "-" * 60 + "\n")
    
    os.chdir("backend")
    subprocess.run([sys.executable, "app.py"])

def start_frontend():
    """启动前端"""
    print("\n启动前端服务...")
    print("  命令: python run_frontend.py")
    print("  地址: http://localhost:8000")
    print("\n" + "-" * 60 + "\n")
    
    subprocess.run([sys.executable, "run_frontend.py"])

def start_both():
    """同时启动前后端"""
    print("\n启动方案：")
    print("  - 后端将在新窗口中启动")
    print("  - 前端将在新窗口中启动")
    print("  - 浏览器将自动打开")
    print("\n" + "=" * 60 + "\n")
    
    # 启动后端
    print("正在启动后端服务...")
    if sys.platform == "win32":
        # Windows
        subprocess.Popen(
            ["start", "cmd", "/k", f"cd backend && {sys.executable} app.py"],
            shell=True
        )
    else:
        # Linux/Mac
        subprocess.Popen([
            "gnome-terminal", "--", "bash", "-c", 
            f"cd backend && {sys.executable} app.py; exec bash"
        ])
    
    time.sleep(3)  # 等待后端启动
    
    # 启动前端
    print("正在启动前端服务...")
    if sys.platform == "win32":
        # Windows
        subprocess.Popen(
            ["start", "cmd", "/k", f"{sys.executable} run_frontend.py"],
            shell=True
        )
    else:
        # Linux/Mac
        subprocess.Popen([
            "gnome-terminal", "--", "bash", "-c",
            f"{sys.executable} run_frontend.py; exec bash"
        ])
    
    print("\n" + "=" * 60)
    print("启动完成！")
    print("  前端: http://localhost:8000")
    print("  后端: http://localhost:5000")
    print("=" * 60)
    
    # 自动打开浏览器
    time.sleep(2)
    webbrowser.open('http://localhost:8000')

def install_dependencies():
    """安装后端依赖"""
    print("\n安装后端依赖...")
    print("  命令: pip install -r backend/requirements.txt")
    print()
    
    result = subprocess.run([
        sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"
    ])
    
    if result.returncode == 0:
        print("\n✓ 依赖安装完成！")
        input("\n按回车键返回菜单...")
    else:
        print("\n✗ 依赖安装失败，请检查错误信息")
        input("\n按回车键返回菜单...")

def main():
    """主函数"""
    print_header()
    
    if not check_python():
        return
    
    has_config = setup_env()
    has_dependencies = check_backend_dependency()
    
    if not has_config:
        print("\n请先配置 API 密钥，然后重新运行此脚本")
        input("按回车键退出...")
        return
    
    if not has_dependencies:
        print("\n请先安装依赖，然后重新运行此脚本")
        input("按回车键退出...")
        return
    
    while True:
        choice = show_menu()
        
        if choice == "1":
            start_both()
            return
        elif choice == "2":
            start_backend()
            return
        elif choice == "3":
            start_frontend()
            return
        elif choice == "4":
            install_dependencies()
        elif choice == "5":
            print("\n退出程序")
            return
        else:
            print("\n无效的选项，请重新选择\n")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")
