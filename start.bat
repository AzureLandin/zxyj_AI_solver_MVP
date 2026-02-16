@echo off
REM AI解题助手 - 快速启动脚本

echo ========================================
echo    AI解题助手 - 快速启动
echo ========================================
echo.

REM 检查Python版本
echo 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

REM 创建.env文件（如果不存在）
if not exist "backend\.env" (
    echo 创建后端配置文件...
    copy "backend\.env.example" "backend\.env"
    echo.
    echo 注意: 请编辑 backend\.env 文件，填写你的AI API密钥
    echo.
)

echo.
echo ========================================
echo 请选择启动方式：
echo 1. 同时启动前后端（需要两个终端）
echo 2. 仅启动后端
echo 3. 仅启动前端
echo 4. 安装后端依赖
echo 5. 退出
echo ========================================
echo.

set /p choice="请输入选项 (1-5): "

if "%choice%"=="1" (
    echo.
    echo 正在启动后端服务...
    start "AI Solver Backend" cmd /k "cd backend && python app.py"
    timeout /t 3 /nobreak >nul
    
    echo 正在启动前端服务...
    start "AI Solver Frontend" cmd /k "python run_frontend.py"
    
    echo.
    echo ========================================
    echo 启动完成！
    echo 前端: http://localhost:8000
    echo 后端: http://localhost:5000
    echo ========================================
) else if "%choice%"=="2" (
    echo 启动后端服务...
    cd backend
    python app.py
) else if "%choice%"=="3" (
    echo 启动前端服务...
    python run_frontend.py
) else if "%choice%"=="4" (
    echo 安装后端依赖...
    cd backend
    pip install -r requirements.txt
    echo.
    echo 依赖安装完成！
    pause
) else if "%choice%"=="5" (
    exit /b 0
) else (
    echo 无效的选项！
    pause
)
