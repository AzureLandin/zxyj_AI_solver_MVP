# AI解题助手 - API接口文档

## 基本信息

- **基础URL**: `http://localhost:5000`
- **API版本**: v1.0
- **支持格式**: JSON
- **字符编码**: UTF-8

---

## 接口列表

### 1. 健康检查

检查API服务是否正常运行。

**请求**

- **方法**: `GET`
- **路径**: `/api/health`

**响应**

```json
{
  "status": "ok",
  "message": "AI Solver API is running"
}
```

---

### 2. 获取路由配置

获取当前模型路由配置信息，展示文字搜题和拍照搜题分别使用的模型。

**请求**

- **方法**: `GET`
- **路径**: `/api/routing`

**响应**

```json
{
  "success": true,
  "data": {
    "routing_rules": {
      "text_search": {
        "description": "文字搜题",
        "endpoint": "/api/solve",
        "method": "POST",
        "model_type": "text",
        "model": "glm-4-flash",
        "api_base": "https://open.bigmodel.cn/api/paas/v4"
      },
      "image_search": {
        "description": "拍照搜题",
        "endpoint": "/api/solve-image",
        "method": "POST",
        "model_type": "vision",
        "model": "glm-4v-flash",
        "api_base": "https://open.bigmodel.cn/api/paas/v4"
      }
    },
    "note": "系统会根据不同的搜题方式自动路由到对应的AI模型"
  }
}
```

---

### 3. 文字搜题

接收文字题目，调用**文字模型**返回详细解答。

**请求**

- **方法**: `POST`
- **路径**: `/api/solve`
- **Content-Type**: `application/json`

**请求体**

```json
{
  "problem": "求解方程：2x + 5 = 13"
}
```

| 参数      | 类型     | 必填  | 说明   |
| ------- | ------ | --- | ---- |
| problem | string | 是   | 题目内容 |

**成功响应**

```json
{
  "success": true,
  "data": {
    "problem": "求解方程：2x + 5 = 13",
    "solution": "**问题分析**：\n这是一个一元一次方程，需要求解x的值。\n\n**解题思路**：\n移项、合并同类项、求解。\n\n**详细步骤**：\n1. 将方程两边减去5：2x = 8\n2. 将方程两边除以2：x = 4\n\n**最终答案**：\nx = 4",
    "model": "glm-4-flash",
    "model_type": "text"
  }
}
```

| 字段         | 类型     | 说明                    |
| ---------- | ------ | --------------------- |
| problem    | string | 原始题目                  |
| solution   | string | AI生成的解答（支持Markdown格式） |
| model      | string | 使用的模型名称               |
| model_type | string | 模型类型（text/vision）     |

**错误响应**

```json
{
  "success": false,
  "error": "题目内容不能为空"
}
```

---

### 4. 拍照搜题

接收题目图片，调用**视觉模型**识别题目并返回解答。

**请求**

- **方法**: `POST`
- **路径**: `/api/solve-image`
- **Content-Type**: `multipart/form-data`

**请求体**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| image | file | 是 | 图片文件（支持JPG、PNG） |

**成功响应**

```json
{
  "success": true,
  "data": {
    "problem": "图片题目（已识别）",
    "solution": "**问题分析**：\n[AI识别的题目内容]\n\n**解题思路**：\n[解题方法]\n\n**详细步骤**：\n[步骤说明]\n\n**最终答案**：\n[最终答案]",
    "model": "glm-4v-flash",
    "model_type": "vision"
  }
}
```

**错误响应**

```json
{
  "success": false,
  "error": "不支持的图片格式，请上传 JPG 或 PNG 格式"
}
```

---

### 5. 获取模型列表

获取当前配置的AI模型信息和可用模型列表。

**请求**

- **方法**: `GET`
- **路径**: `/api/models`

**响应**

```json
{
  "success": true,
  "data": {
    "text_model": {
      "current": "glm-4-flash",
      "api_base": "https://open.bigmodel.cn/api/paas/v4"
    },
    "vision_model": {
      "current": "glm-4v-flash",
      "api_base": "https://open.bigmodel.cn/api/paas/v4"
    },
    "available_models": [
      "gpt-3.5-turbo",
      "gpt-4",
      "gpt-4-turbo"
    ]
  }
}
```

| 字段               | 类型     | 说明     |
| ---------------- | ------ | ------ |
| text_model       | object | 文字模型配置 |
| vision_model     | object | 视觉模型配置 |
| available_models | array  | 可用模型列表 |

---

## 错误码说明

| HTTP状态码 | 说明      |
| ------- | ------- |
| 200     | 请求成功    |
| 400     | 请求参数错误  |
| 500     | 服务器内部错误 |

---

## 路由规则说明

系统根据搜题方式自动路由到对应的AI模型：

| 搜题方式 | API端点              | 模型类型 | 环境变量              |
| ---- | ------------------ | ---- | ----------------- |
| 文字搜题 | `/api/solve`       | 文字模型 | `AI_MODEL`        |
| 拍照搜题 | `/api/solve-image` | 视觉模型 | `AI_VISION_MODEL` |

**注意**：视觉模型必须支持多模态（图片识别）功能。如果视觉模型配置为空，系统会使用文字模型作为后备。

---

## 配置说明

在 `backend/.env` 文件中配置AI模型：

```bash
# 文字模型（用于文字搜题）
AI_API_KEY=your_api_key
AI_API_BASE=https://open.bigmodel.cn/api/paas/v4
AI_MODEL=glm-4-flash

# 视觉模型（用于拍照搜题）
AI_VISION_API_KEY=your_api_key
AI_VISION_API_BASE=https://open.bigmodel.cn/api/paas/v4
AI_VISION_MODEL=glm-4v-flash
```

---

## 使用示例

### cURL示例

**文字搜题**

```bash
curl -X POST http://localhost:5000/api/solve \
  -H "Content-Type: application/json" \
  -d '{"problem":"求解方程：2x + 5 = 13"}'
```

**拍照搜题**

```bash
curl -X POST http://localhost:5000/api/solve-image \
  -F "image=@/path/to/question.jpg"
```

**获取路由配置**

```bash
curl http://localhost:5000/api/routing
```

---

## 注意事项

1. **图片大小限制**: 建议图片大小不超过10MB
2. **支持格式**: JPG、PNG
3. **请求超时**: API默认超时时间为60秒
4. **Markdown支持**: 解答内容支持Markdown格式渲染
5. **最终答案高亮**: AI会按格式输出最终答案，前端可自动高亮显示

---

## 更新日志

### v1.0 (2026-02-23)

- 初始版本发布
- 支持文字搜题功能
- 支持拍照搜题功能
- 实现双模型路由机制
- 添加路由配置查询接口
