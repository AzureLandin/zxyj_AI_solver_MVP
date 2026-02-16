# AI解题助手 - 项目设计文档

## 文档信息

| 项目 | AI解题助手 MVP |
|------|---------------|
| 版本 | v1.0.0 |
| 创建日期 | 2026-02-16 |
| 最后更新 | 2026-02-16 |
| 作者 | AI Solver Team |

---

## 目录

1. [项目概述](#项目概述)
2. [技术架构](#技术架构)
3. [系统设计](#系统设计)
4. [接口设计](#接口设计)
5. [数据模型](#数据模型)
6. [安全设计](#安全设计)
7. [性能设计](#性能设计)
8. [部署方案](#部署方案)
9. [扩展性设计](#扩展性设计)
10. [测试方案](#测试方案)

---

## 项目概述

### 1.1 项目背景

AI解题助手是一个基于大语言模型的智能解题应用，旨在帮助学生和学习者快速获得各类题目的详细解答。系统采用前后端完全分离的架构，通过RESTful API进行通信。

### 1.2 核心功能

- **智能解题**：支持数学、物理、化学、生物等多学科题目
- **详细步骤**：提供问题分析、解题思路、详细步骤和最终答案
- **实时响应**：通过API实时调用大模型生成解答
- **用户友好**：简洁直观的Web界面
- **灵活配置**：支持多种AI模型和自定义API地址

### 1.3 技术选型

#### 后端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.7+ | 开发语言 |
| Flask | 3.0.0 | Web框架 |
| Flask-CORS | 4.0.0 | 跨域请求处理 |
| OpenAI SDK | >=1.12.0 | 大模型API调用 |
| python-dotenv | 1.0.0 | 环境变量管理 |
| httpx | >=0.25.0 | HTTP客户端 |

#### 前端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| HTML5 | - | 页面结构 |
| CSS3 | - | 样式设计 |
| JavaScript | ES6+ | 交互逻辑 |
| Bootstrap | 3.4.1 | UI框架 |
| jQuery | 3.6.0 | DOM操作 |
| Font Awesome | 4.7.0 | 图标库 |

---

## 技术架构

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        用户浏览器                           │
│                   (Frontend - localhost:8000)               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  index.html  │  │  style.css    │  │   app.js     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────────┬────────────────────────────┘
                             │
                    AJAX/RESTful API
                             │
┌────────────────────────────┴────────────────────────────┐
│                    后端服务器                             │
│                  (Backend - localhost:5000)              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   app.py     │  │  config.py   │  │  ai_service  │     │
│  │  (Flask)     │  │  (配置)      │  │  (AI服务)    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────────┬────────────────────────────┘
                             │
                    OpenAI API / 兼容API
                             │
                    ┌────────┴────────┐
                    │  大语言模型     │
                    │  (GPT/Claude)  │
                    └─────────────────┘
```

### 2.2 分层架构

```
┌─────────────────────────────────────┐
│        表现层 (Frontend)            │
│   HTML + CSS + JavaScript (jQuery) │
└─────────────────────────────────────┘
              ↕ API/JSON
┌─────────────────────────────────────┐
│        接口层 (API)                 │
│   Flask RESTful API Endpoints       │
└─────────────────────────────────────┘
              ↕
┌─────────────────────────────────────┐
│        业务层 (Service)             │
│   AIService - 题目处理逻辑          │
└─────────────────────────────────────┘
              ↕
┌─────────────────────────────────────┐
│        外部服务层                    │
│   OpenAI API / 第三方API            │
└─────────────────────────────────────┘
```

### 2.3 部署架构

```
开发环境:
┌───────────────────────────────────────┐
│  本地开发机                           │
│  ├─ Flask (localhost:5000)           │
│  └─ Python HTTP Server (localhost:8000)│
└───────────────────────────────────────┘

生产环境:
┌───────────────┐         ┌───────────────┐
│  静态文件服务器 │         │   API服务器   │
│  (Nginx/CDN)   │         │   (Gunicorn)  │
└───────────────┘         └───────────────┘
        │                        │
        └────────┬───────────────┘
                 │
           ┌──────┴──────┐
           │   负载均衡  │
           └──────┬──────┘
                  │
           ┌──────┴──────┐
           │  大模型API  │
           └─────────────┘
```

---

## 系统设计

### 3.1 后端设计

#### 3.1.1 模块结构

```
backend/
├── app.py                    # Flask应用主入口
├── config.py                 # 配置管理
├── requirements.txt          # Python依赖
├── services/                # 服务层
│   ├── __init__.py
│   └── ai_service.py        # AI解题服务
└── pyrightconfig.json       # 类型检查配置
```

#### 3.1.2 核心类设计

##### AIService 类

```python
class AIService:
    """AI解题服务类"""
    
    属性:
        - api_key: str        # API密钥
        - api_base: str       # API基础地址
        - model: str          # 模型名称
        - client: OpenAI      # OpenAI客户端实例
    
    方法:
        - __init__(api_key, api_base, model)
        - solve_problem(problem) -> Optional[str]
        - test_connection() -> bool
```

##### Config 类

```python
class Config:
    """配置类"""
    
    属性:
        - SECRET_KEY: str           # Flask密钥
        - AI_API_KEY: str           # AI API密钥
        - AI_API_BASE: str          # AI API地址
        - AI_MODEL: str             # 当前模型
        - FRONTEND_ORIGIN: str      # 前端地址(CORS)
```

#### 3.1.3 异常处理

自定义异常层次结构：

```
AIServiceError (基础异常)
├── AIServiceInitError (初始化异常)
├── AIServiceAPIError (API调用异常)
└── AIServiceConnectionError (连接异常)
```

异常处理流程：

```
┌─────────────┐
│  调用AI服务  │
└──────┬──────┘
       │
       ↓ 发生异常
┌─────────────┐
│ 捕获异常     │
└──────┬──────┘
       │
       ├─→ AIServiceInitError
       │      ↓
       │  记录日志 + 返回错误响应
       │
       ├─→ AIServiceAPIError
       │      ↓
       │  记录日志 + 返回错误响应
       │
       └─→ AIServiceConnectionError
              ↓
         记录日志 + 返回错误响应
```

### 3.2 前端设计

#### 3.2.1 页面结构

```
index.html
├── <head>
│   ├── Bootstrap CSS
│   ├── Font Awesome
│   └── 自定义样式
├── <body>
│   ├── 导航栏
│   ├── 主容器
│   │   ├── 左侧面板 - 题目输入区
│   │   │   ├── 表单
│   │   │   └── 示例题目
│   │   └── 右侧面板 - 答案展示区
│   │       ├── 初始状态
│   │       ├── 加载状态
│   │       ├── 答案内容
│   │       └── 错误状态
│   ├── 关于模态框
│   └── 页脚
└── JavaScript
    ├── jQuery
    ├── Bootstrap JS
    └── app.js (自定义逻辑)
```

#### 3.2.2 状态管理

前端状态流转：

```
┌──────────┐     提交题目     ┌──────────┐
│ 初始状态  │ ──────────────→ │ 加载状态  │
└──────────┘                  └─────┬────┘
                                   │
                                   │ API响应
                                   ↓
                              ┌──────────┐
                              │ 成功状态  │ ←───┐
                              └──────────┘     │
                                   ↑           │
                              ┌──────────┐     │
                              │ 失败状态  │ ────┘
                              └──────────┘
```

#### 3.2.3 交互流程

```
用户输入题目
    ↓
点击"AI解题"按钮
    ↓
验证输入 (非空检查)
    ↓
显示加载状态
    ↓
AJAX POST /api/solve
    ↓
┌─────────┐
│等待响应  │
└────┬────┘
     │
     ├─→ 成功 (200 OK)
     │      ↓
     │   显示答案
     │
     └─→ 失败 (4xx/5xx)
            ↓
         显示错误信息
```

---

## 接口设计

### 4.1 API列表

| 端点 | 方法 | 描述 | 认证 |
|------|------|------|------|
| `/api/health` | GET | 健康检查 | 否 |
| `/api/solve` | POST | 解题接口 | 否 |
| `/api/models` | GET | 获取模型列表 | 否 |

### 4.2 接口详情

#### 4.2.1 健康检查接口

**请求：**
```http
GET /api/health
```

**响应：**
```json
{
  "status": "ok",
  "message": "AI Solver API is running"
}
```

**状态码：**
- `200 OK`: 服务正常运行

---

#### 4.2.2 解题接口

**请求：**
```http
POST /api/solve
Content-Type: application/json

{
  "problem": "题目内容"
}
```

**请求参数：**

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| problem | string | 是 | 题目内容，不能为空 |

**成功响应：**
```json
{
  "success": true,
  "data": {
    "problem": "题目内容",
    "solution": "**问题分析**：\n...\n\n**最终答案**：\n...",
    "model": "gpt-3.5-turbo"
  }
}
```

**错误响应：**
```json
{
  "success": false,
  "error": "错误描述信息"
}
```

**状态码：**
- `200 OK`: 成功获取解答
- `400 Bad Request`: 请求参数错误
- `500 Internal Server Error`: 服务器内部错误

**错误类型：**
| 错误信息 | 场景 |
|----------|------|
| 缺少题目内容 | 未提供problem参数 |
| 题目内容不能为空 | problem参数为空字符串 |
| 无法获取解答，请检查API配置 | AI服务调用失败 |
| 服务器错误: {具体错误} | 其他异常情况 |

---

#### 4.2.3 获取模型列表接口

**请求：**
```http
GET /api/models
```

**响应：**
```json
{
  "success": true,
  "data": {
    "current_model": "gpt-3.5-turbo",
    "available_models": [
      "gpt-3.5-turbo",
      "gpt-4",
      "gpt-4-turbo",
      "claude-3-sonnet-20240229",
      "claude-3-opus-20240229"
    ]
  }
}
```

**状态码：**
- `200 OK`: 成功获取模型列表

---

### 4.3 CORS配置

**允许的源：**
```python
FRONTEND_ORIGIN = "http://localhost:8000"
```

**允许的方法：**
- GET
- POST
- OPTIONS

**允许的请求头：**
- Content-Type
- Authorization

---

## 数据模型

### 5.1 请求数据模型

#### 5.1.1 解题请求模型

```typescript
interface SolveRequest {
  problem: string;  // 题目内容
}
```

### 5.2 响应数据模型

#### 5.2.1 通用响应模型

```typescript
interface BaseResponse {
  success: boolean;  // 是否成功
  error?: string;    // 错误信息（失败时）
}
```

#### 5.2.2 健康检查响应

```typescript
interface HealthResponse extends BaseResponse {
  status: string;     // 状态
  message: string;    // 消息
}
```

#### 5.2.3 解题响应

```typescript
interface SolveResponse extends BaseResponse {
  data?: {
    problem: string;   // 题目内容
    solution: string;  // 解答内容（Markdown格式）
    model: string;     // 使用的模型
  };
}
```

#### 5.2.4 模型列表响应

```typescript
interface ModelsResponse extends BaseResponse {
  data?: {
    current_model: string;     // 当前模型
    available_models: string[]; // 可用模型列表
  };
}
```

### 5.3 内部数据模型

#### 5.3.1 配置模型

```python
class Config:
    SECRET_KEY: str
    AI_API_KEY: str
    AI_API_BASE: str
    AI_MODEL: str
    FRONTEND_ORIGIN: str
```

#### 5.3.2 AI服务模型

```python
class AIService:
    api_key: str
    api_base: str
    model: str
    client: OpenAI
```

---

## 安全设计

### 6.1 API密钥安全

#### 6.1.1 密钥存储

- 使用环境变量存储敏感信息
- 通过 `.env` 文件管理（不提交到版本控制）
- 提供 `.env.example` 作为模板

**`.env` 文件示例：**
```env
SECRET_KEY=your-secret-key-here
AI_API_KEY=your-openai-api-key
AI_API_BASE=https://api.openai.com/v1
AI_MODEL=gpt-3.5-turbo
FRONTEND_ORIGIN=http://localhost:8000
```

#### 6.1.2 密钥验证

在初始化时验证API密钥的有效性：

```python
if not api_key or not api_key.strip():
    raise AIServiceInitError("API密钥不能为空")
```

### 6.2 输入验证

#### 6.2.1 前端验证

- 必填字段检查
- 内容非空检查

```javascript
const problem = $('#problemInput').val().trim();
if (!problem) {
    showError('请输入题目内容');
    return;
}
```

#### 6.2.2 后端验证

- 参数存在性检查
- 内容非空检查

```python
if not data or 'problem' not in data:
    return jsonify({'success': False, 'error': '缺少题目内容'}), 400

problem = data['problem'].strip()
if not problem:
    return jsonify({'success': False, 'error': '题目内容不能为空'}), 400
```

### 6.3 跨域安全

- 配置CORS只允许指定源访问
- 限制允许的HTTP方法
- 限制允许的请求头

```python
CORS(app, resources={
    r"/api/*": {
        "origins": app.config['FRONTEND_ORIGIN'],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

### 6.4 错误处理

#### 6.4.1 异常分类

```python
class AIServiceError(Exception): pass
class AIServiceInitError(AIServiceError): pass
class AIServiceAPIError(AIServiceError): pass
class AIServiceConnectionError(AIServiceError): pass
```

#### 6.4.2 错误响应格式

统一使用JSON格式返回错误信息：

```json
{
  "success": false,
  "error": "错误描述"
}
```

#### 6.4.3 日志记录

```python
app.logger.error(f"解题错误: {str(e)}")
```

### 6.5 超时设置

- 客户端初始化超时：30秒
- API请求超时：60秒

```python
client = openai.OpenAI(
    api_key=api_key,
    base_url=api_base,
    timeout=30.0
)

response = self.client.chat.completions.create(
    ...
    timeout=60.0
)
```

---

## 性能设计

### 7.1 响应时间优化

#### 7.1.1 前端优化

- 使用CDN加载静态资源
- 减少HTTP请求（合并CSS/JS）
- 添加加载状态反馈

#### 7.1.2 后端优化

- 设置合理的超时时间
- 异常处理避免阻塞
- 简化提示词减少token消耗

### 7.2 资源使用优化

#### 7.2.1 Token控制

- 限制最大输出token数：4000
- 调整温度参数：0.7（平衡速度和质量）

```python
max_tokens=4000,
temperature=0.7,
top_p=0.9
```

#### 7.2.2 连接管理

- 使用连接池（httpx默认支持）
- 设置合理的超时时间
- 连接测试确保可用性

### 7.3 并发处理

当前版本为MVP，主要设计为单实例运行。未来可扩展：

```
┌─────────────┐
│  负载均衡器  │
└──────┬──────┘
       │
  ┌────┴────┐
  │         │
┌─┴─┐     ┌─┴─┐
│实例1│    │实例2│
└───┘     └───┘
```

### 7.4 缓存设计（未来扩展）

#### 7.4.1 缓存策略

```python
# Redis缓存示例
def solve_problem(self, problem: str) -> Optional[str]:
    cache_key = f"solution:{hashlib.md5(problem.encode()).hexdigest()}"
    
    # 尝试从缓存获取
    cached = redis_client.get(cache_key)
    if cached:
        return cached
    
    # 调用AI服务
    solution = self._call_ai(problem)
    
    # 缓存结果（1小时）
    if solution:
        redis_client.setex(cache_key, 3600, solution)
    
    return solution
```

---

## 部署方案

### 8.1 开发环境部署

#### 8.1.1 环境要求

- Python 3.7+
- pip
- 现代浏览器

#### 8.1.2 部署步骤

```bash
# 1. 克隆项目
git clone <repository-url>
cd AI_solver_MVP

# 2. 安装后端依赖
cd backend
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填写API密钥

# 4. 启动后端
python app.py

# 5. 启动前端（新终端）
python ../run_frontend.py
```

#### 8.1.3 访问地址

- 前端：http://localhost:8000
- 后端API：http://localhost:5000

### 8.2 生产环境部署

#### 8.2.1 后端部署

**使用Gunicorn：**

```bash
cd backend
pip install gunicorn

# 启动服务
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**使用Systemd管理服务：**

```ini
# /etc/systemd/system/ai-solver.service
[Unit]
Description=AI Solver Backend Service
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/AI_solver_MVP/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

**启动服务：**
```bash
sudo systemctl start ai-solver
sudo systemctl enable ai-solver
```

#### 8.2.2 前端部署

**使用Nginx：**

```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/frontend;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # API反向代理
    location /api/ {
        proxy_pass http://localhost:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**部署到CDN：**

```bash
# 上传前端文件到CDN
aws s3 sync frontend/ s3://your-bucket/ --delete
```

#### 8.2.3 Docker部署（推荐）

**Dockerfile（后端）：**

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

**Dockerfile（前端）：**

```dockerfile
FROM nginx:alpine

COPY frontend/ /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**docker-compose.yml：**

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "5000:5000"
    environment:
      - AI_API_KEY=${AI_API_KEY}
      - AI_API_BASE=${AI_API_BASE}
      - AI_MODEL=${AI_MODEL}
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
```

**启动：**
```bash
docker-compose up -d
```

### 8.3 监控与日志

#### 8.3.1 日志配置

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
```

#### 8.3.2 健康检查

```bash
# 定期检查API健康状态
curl http://localhost:5000/api/health
```

---

## 扩展性设计

### 9.1 功能扩展

#### 9.1.1 用户系统

```python
# 数据库模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    api_quota = db.Column(db.Integer, default=100)
```

#### 9.1.2 历史记录

```python
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    problem = db.Column(db.Text)
    solution = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

#### 9.1.3 题目分类

```python
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
```

### 9.2 技术扩展

#### 9.2.1 支持多种AI服务

```python
class AIServiceFactory:
    @staticmethod
    def create_service(provider: str, config: dict):
        if provider == 'openai':
            return OpenAIService(config)
        elif provider == 'anthropic':
            return AnthropicService(config)
        elif provider == 'azure':
            return AzureOpenAIService(config)
```

#### 9.2.2 异步处理

```python
import asyncio
from openai import AsyncOpenAI

class AsyncAIService:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
    
    async def solve_problem_async(self, problem: str):
        response = await self.client.chat.completions.create(...)
        return response.choices[0].message.content
```

#### 9.2.3 消息队列

```python
# 使用Celery处理异步任务
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def solve_problem_task(problem: str):
    ai_service = AIService(...)
    return ai_service.solve_problem(problem)
```

### 9.3 数据库扩展

```python
# 使用SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    # ...
```

### 9.4 缓存扩展

```python
# 使用Redis
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'RedisCache'})

@app.route('/api/solve', methods=['POST'])
@cache.cached(timeout=3600, key_prefix=lambda: request.json['problem'])
def solve_problem():
    # ...
```

---

## 测试方案

### 10.1 单元测试

#### 10.1.1 后端单元测试

```python
# tests/test_ai_service.py
import pytest
from services.ai_service import AIService

def test_solve_problem_success():
    service = AIService(api_key="test-key")
    result = service.solve_problem("1+1=?")
    assert result is not None
    assert "2" in result

def test_solve_problem_empty_input():
    service = AIService(api_key="test-key")
    result = service.solve_problem("")
    assert result is None

def test_api_key_validation():
    with pytest.raises(AIServiceInitError):
        service = AIService(api_key="")
```

#### 10.1.2 前端单元测试

```javascript
// tests/app.test.js
describe('AI Solver App', () => {
    test('should show error when problem is empty', () => {
        $('#problemInput').val('');
        $('#problemForm').submit();
        expect($('#errorState').is(':visible')).toBe(true);
    });

    test('should call API on form submit', (done) => {
        $('#problemInput').val('test problem');
        $('#problemForm').submit();
        // 验证API调用...
    });
});
```

### 10.2 集成测试

#### 10.2.1 API集成测试

```python
# tests/test_api.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert b'ok' in response.data

def test_solve_problem(client):
    response = client.post('/api/solve',
                           json={'problem': '1+1=?'},
                           content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
```

### 10.3 端到端测试

#### 10.3.1 E2E测试脚本

```python
# tests/test_e2e.py
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_full_workflow():
    driver = webdriver.Chrome()
    
    try:
        # 打开前端页面
        driver.get('http://localhost:8000')
        
        # 输入题目
        problem_input = driver.find_element(By.ID, 'problemInput')
        problem_input.send_keys('1+1=?')
        
        # 点击解题按钮
        solve_btn = driver.find_element(By.ID, 'solveBtn')
        solve_btn.click()
        
        # 等待结果
        time.sleep(5)
        
        # 验证结果显示
        answer_content = driver.find_element(By.ID, 'answerContent')
        assert answer_content.is_displayed()
        
    finally:
        driver.quit()
```

### 10.4 性能测试

#### 10.4.1 负载测试

```python
# tests/load_test.py
import locust
from locust import HttpUser, task, between

class AISolverUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        self.client.get("/api/health")
    
    @task
    def solve_problem(self):
        self.client.post("/api/solve",
                        json={"problem": "1+1=?"})
```

### 10.5 测试覆盖率

```bash
# 安装pytest-cov
pip install pytest-cov

# 运行测试并生成覆盖率报告
pytest --cov=backend --cov-report=html
```

---

## 附录

### A. 环境变量说明

| 变量名 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| SECRET_KEY | Flask密钥 | dev-secret-key | 否 |
| AI_API_KEY | OpenAI API密钥 | - | 是 |
| AI_API_BASE | API基础地址 | https://api.openai.com/v1 | 否 |
| AI_MODEL | 模型名称 | gpt-3.5-turbo | 否 |
| FRONTEND_ORIGIN | 前端地址 | http://localhost:8000 | 否 |

### B. 支持的AI模型

| 模型 | 描述 | 适用场景 |
|------|------|----------|
| gpt-3.5-turbo | 快速、低成本 | 一般题目 |
| gpt-4 | 能力强 | 复杂题目 |
| gpt-4-turbo | 性能平衡 | 推荐使用 |
| claude-3-sonnet | Anthropic模型 | 长文本 |
| claude-3-opus | 高级模型 | 最复杂题目 |

### C. 常见问题

#### C.1 如何切换模型？

修改 `.env` 文件中的 `AI_MODEL` 变量，然后重启后端服务。

#### C.2 如何添加新的AI服务提供商？

1. 在 `services/` 目录下创建新的服务类
2. 实现 `solve_problem` 和 `test_connection` 方法
3. 在 `app.py` 中初始化新服务

#### C.3 如何部署到生产环境？

参考"8.2 生产环境部署"章节，推荐使用Docker部署。

### D. 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0.0 | 2026-02-16 | 初始版本发布 |

### E. 联系方式

- 项目地址：[GitHub Repository]
- 问题反馈：[Issue Tracker]
- 邮件：support@example.com

---

**文档结束**
