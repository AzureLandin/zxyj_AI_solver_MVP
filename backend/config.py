import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # AI API配置
    AI_API_KEY = os.getenv('AI_API_KEY', '')
    AI_API_BASE = os.getenv('AI_API_BASE')
    AI_MODEL = os.getenv('AI_MODEL', 'gpt-3.5-turbo')
    
    # 允许的前端域名（CORS）
    FRONTEND_ORIGIN = os.getenv('FRONTEND_ORIGIN', 'http://localhost:8000')
