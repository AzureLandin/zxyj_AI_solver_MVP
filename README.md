# AI解题助手 - MVP版本

AI智能解题应用，支持拍照搜题和文字搜题。
=======

这是一个完整的AI解题Web应用MVP，实现了前后端完全分离的架构。

## 📁 项目结构

```
AI_solver_MVP/
├── backend/                  # 后端API服务
│   ├── app.py               # Flask应用入口
│   ├── config.py            # 配置文件
│   ├── requirements.txt     # Python依赖
│   ├── .env.example         # 环境变量示例
│   └── services/
│       └── ai_service.py    # AI服务
├── frontend/                # 前端页面
│   ├── index.html          # 主页面
│   ├── css/style.css       # 样式
│   └── js/app.js           # 交互逻辑
├── run_frontend.py         # 前端服务器
├── start.bat               # 一键启动脚本 ⭐
├── test_api.py             # API测试
└── API.md                  # API文档
```

## 🚀 快速启动

### Windows 用户

**双击 `start.bat`**，按提示选择启动方式：

- 选项 1：同时启动前后端（推荐）
- 选项 2：仅启动后端
- 选项 3：仅启动前端

### 手动启动

**1. 配置API密钥**

```bash
cd backend
copy .env.example .env
# 编辑 .env 文件，填写你的 API 密钥
```

**2. 安装依赖**

```bash
cd backend
pip install -r requirements.txt
```

**3. 启动服务**

```bash
# 终端1：启动后端
cd backend
python app.py

# 终端2：启动前端
python run_frontend.py
```

**4. 访问应用**

打开浏览器访问 http://localhost:8000

## ⚙️ 配置说明

编辑 `backend/.env`：

```env
# 文字模型配置
AI_API_KEY=your-api-key
AI_API_BASE=https://api.openai.com/v1
AI_MODEL=gpt-3.5-turbo

# 视觉模型配置（拍照搜题用）
AI_VISION_API_KEY=your-vision-api-key
AI_VISION_API_BASE=https://api.openai.com/v1
AI_VISION_MODEL=gpt-4-vision-preview
```

## 🌐 API接口

| 接口                 | 方法   | 说明     |
| ------------------ | ---- | ------ |
| `/api/health`      | GET  | 健康检查   |
| `/api/solve`       | POST | 文字解题   |
| `/api/solve-image` | POST | 图片解题   |
| `/api/models`      | GET  | 获取模型信息 |
| `/api/routing`     | GET  | 获取路由配置 |

详见 [API.md](API.md)

## 🎯 功能特点

- ✅ 拍照搜题（调用视觉模型）
- ✅ 文字搜题（调用对话模型）
- ✅ 搜题历史记录
- ✅ 详细解题步骤
- ✅ 响应式设计
- ✅ Markdown渲染
- ✅ 代码高亮

## 📝 使用说明

1. **文字搜题**：点击"文字搜题" → 输入题目 → 开始解题
2. **拍照搜题**：点击"拍照搜题" → 上传图片 → 开始解题
3. **查看历史**：点击右上角历史图标查看搜题记录

## 🐛 常见问题

**无法连接后端**

- 检查后端是否已启动（端口5000）
- 检查前端配置的后端地址

**API密钥无效**

- 检查 `.env` 文件配置
- 检查API密钥是否有效
- 检查API余额

## 💡 支持模型

- OpenAI: GPT-3.5, GPT-4, GPT-4V
- Claude: Claude 3 系列
- 智谱AI: GLM-4, GLM-4V
- 其他兼容 OpenAI API 的模型

---

**提示**：使用本应用需要消耗AI API调用额度，请注意控制成本。
