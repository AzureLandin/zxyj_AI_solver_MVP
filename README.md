# AI解题助手 - 快速使用指南

## 🎉 项目已完成！

这是一个完整的AI解题Web应用MVP，实现了前后端完全分离的架构。

## 📁 项目结构

```
AI_solver_MVP/
├── backend/                    # 后端API服务
│   ├── app.py                 # Flask应用入口
│   ├── config.py              # 配置文件
│   ├── requirements.txt       # Python依赖
│   ├── .env.example           # 环境变量示例
│   └── services/
│       └── ai_service.py      # AI服务（调用大模型API）
├── frontend/                  # 前端静态页面
│   ├── index.html            # 主页面
│   ├── css/style.css         # 自定义样式
│   └── js/app.js             # 前端交互逻辑
├── run_frontend.py           # 前端服务器启动脚本
├── quick_start.py            # 快速启动脚本（推荐）
├── start.bat                 # Windows快速启动批处理
├── test_api.py               # API测试工具
└── README.md                 # 完整文档
```

## 🚀 快速启动（推荐）

### 方法1：使用快速启动脚本（推荐）

双击运行 `quick_start.py`：

```bash
python quick_start.py
```

或双击 `start.bat`（Windows）

按照提示操作即可！

### 方法2：手动启动

**步骤1：配置API密钥**

```bash
cd backend
copy .env.example .env
```

编辑 `.env` 文件，填写你的API密钥：

```env
AI_API_KEY=your-api-key-here
AI_API_BASE=https://api.openai.com/v1
AI_MODEL=gpt-3.5-turbo
```

**步骤2：安装依赖**

```bash
cd backend
pip install -r requirements.txt
```

**步骤3：启动后端**

```bash
cd backend
python app.py
```

**步骤4：启动前端**

在新终端中：

```bash
python run_frontend.py
```

浏览器会自动打开 http://localhost:8000

## 🧪 测试API

运行测试脚本验证API是否正常：

```bash
python test_api.py
```

## 🎯 功能特点

- ✅ 前后端完全分离（Flask + Bootstrap3）
- ✅ 调用大模型API解题（支持OpenAI、Azure、Claude等）
- ✅ 美观的响应式界面
- ✅ 详细的解题步骤展示
- ✅ 示例题目快速测试
- ✅ 复制答案功能
- ✅ CORS跨域支持
- ✅ 完整的错误处理

## 🔧 配置说明

编辑 `backend/.env` 文件：

```env
# API密钥（必填）
AI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx

# API地址（可选）
AI_API_BASE=https://api.openai.com/v1

# AI模型（可选）
AI_MODEL=gpt-3.5-turbo

# 前端域名（CORS）
FRONTEND_ORIGIN=http://localhost:8000
```

**支持的模型：**
- `gpt-3.5-turbo`（默认，推荐）
- `gpt-4`（更强，但费用更高）
- `claude-3-sonnet-20240229`
- 其他兼容OpenAI API的模型

## 🌐 API接口

### 健康检查
```bash
GET http://localhost:5000/api/health
```

### 解题接口
```bash
POST http://localhost:5000/api/solve
Content-Type: application/json

{
    "problem": "题目内容"
}
```

### 获取模型信息
```bash
GET http://localhost:5000/api/models
```

## 💡 使用示例

1. **输入题目**：在左侧输入框输入题目
   ```
   计算 (2x + 3)^2 的展开式
   ```

2. **点击解题**：点击"AI解题"按钮

3. **查看解答**：右侧显示详细解题步骤

4. **复制答案**：点击"复制答案"按钮

## 📝 示例题目

- 数学：`计算 2^10 + 3^5`
- 代数：`解方程 x^2 - 5x + 6 = 0`
- 物理：`汽车以10m/s行驶，刹车距离是多少？`
- 化学：`解释什么是氧化还原反应`
- 生物：`什么是光合作用？`

## 🐛 常见问题

**问题：无法连接后端**
- 检查后端是否已启动：`python backend/app.py`
- 检查端口是否被占用：5000

**问题：API密钥无效**
- 检查 `backend/.env` 文件是否正确配置
- 检查API密钥是否有效
- 检查API余额是否充足

**问题：跨域错误**
- 检查 `backend/.env` 中的 `FRONTEND_ORIGIN` 配置
- 确保前端地址与配置一致

## 📚 完整文档

查看 `README.md` 获取更详细的文档，包括：
- 项目架构说明
- 部署指南
- API文档
- 开发指南
- 故障排除

## 🎊 开始使用

1. 配置API密钥（必须）
2. 运行 `python quick_start.py`
3. 开始使用AI解题助手！

---

**提示**：使用本应用需要消耗大模型API的调用额度，请注意控制使用成本。

**祝您使用愉快！** 🎉
