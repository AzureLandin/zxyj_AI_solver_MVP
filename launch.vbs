Set WshShell = CreateObject("WScript.Shell")

' 启动后端服务
WshShell.Run "cmd /k ""cd /d c:\Users\lendi\CodeBuddy\AI_solver_MVP\backend && python app.py""", 1, false

' 等待3秒让后端启动
WScript.Sleep 3000

' 启动前端服务
WshShell.Run "cmd /k ""cd /d c:\Users\lendi\CodeBuddy\AI_solver_MVP && python run_frontend.py""", 1, false

' 提示用户
WScript.Echo "AI解题助手已启动！" & vbCrLf & "前端: http://localhost:8000" & vbCrLf & "后端: http://localhost:5000" & vbCrLf & vbCrLf & "提示：请编辑 backend\.env 文件配置API密钥后，刷新页面即可使用AI解题功能。"
