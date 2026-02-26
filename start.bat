@echo off
chcp 65001 >nul
REM AI解题助手 - 一键启动脚本

echo ========================================
echo    AI解题助手 - 启动器
echo ========================================
echo.

REM 检查Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到 Python，请先安装 Python 3.7+
    pause
    exit /b 1
)

REM 检查配置文件
if not exist "backend\.env" (
    if exist "backend\.env.example" (
        echo 首次运行，创建配置文件...
        copy "backend\.env.example" "backend\.env"
        echo.
        echo 注意: 请编辑 backend\.env 文件，填写你的 API 密钥
        echo.
        start notepad "backend\.env"
        pause
    ) else (
        echo 错误: 找不到配置文件模板
        pause
        exit /b 1
    )
)

REM 检查依赖
python -c "import flask, openai" >nul 2>&1
if %errorlevel% neq 0 (
    echo 安装后端依赖...
    pip install -r backend\requirements.txt
    if %errorlevel% neq 0 (
        echo 依赖安装失败
        pause
        exit /b 1
    )
)

echo.
echo 启动方式:
echo   [1] 同时启动前后端 (推荐)
echo   [2] 仅启动后端
echo   [3] 仅启动前端
echo   [4] 退出
echo.

set /p choice="请选择 (1-4): "

if "%choice%"=="1" (
    echo.
    echo 正在启动 AI解题助手...
    echo.
    
    REM 启动后端
    start "AI Solver 后端" cmd /k "cd backend && python app.py"
    
    REM 等待后端启动
    timeout /t 2 /nobreak >nul
    
    REM 启动前端
    start "AI Solver 前端" cmd /k "python run_frontend.py"
    
    echo 启动完成!
    echo   前端: http://localhost:8000
    echo   后端: http://localhost:5000
    echo.
    timeout /t 3 >nul
    
) else if "%choice%"=="2" (
    echo.
    echo 启动后端服务...
    cd backend
    python app.py
    
) else if "%choice%"=="3" (
    echo.
    echo 启动前端服务...
    python run_frontend.py
    
) else if "%choice%"=="4" (
    exit /b 0
    
) else (
    echo 无效选项
    pause
)
