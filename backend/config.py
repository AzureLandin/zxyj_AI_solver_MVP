import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # AI API配置 - 文字模型（普通对话）
    AI_API_KEY = os.getenv('AI_API_KEY', '')
    AI_API_BASE = os.getenv('AI_API_BASE')
    AI_MODEL = os.getenv('AI_MODEL', 'gpt-3.5-turbo')
    
    # AI API配置 - 视觉模型（图片识别）
    AI_VISION_API_KEY = os.getenv('AI_VISION_API_KEY', os.getenv('AI_API_KEY', ''))
    AI_VISION_API_BASE = os.getenv('AI_VISION_API_BASE', os.getenv('AI_API_BASE', ''))
    AI_VISION_MODEL = os.getenv('AI_VISION_MODEL', 'gpt-4o')
    
    # 允许的前端域名（CORS）
    FRONTEND_ORIGIN = os.getenv('FRONTEND_ORIGIN', 'http://localhost:8000')
