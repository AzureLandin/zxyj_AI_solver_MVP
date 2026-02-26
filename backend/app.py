from flask import Flask, request, jsonify  # type: ignore[reportMissingImports]
from flask_cors import CORS  # type: ignore[reportMissingModuleSource]
from config import Config  # type: ignore[reportImplicitRelativeImport]
from services.ai_service import AIService, AI_list  # type: ignore[reportImplicitRelativeImport]
import base64
import imghdr

app = Flask(__name__)
app.config.from_object(Config)

# 配置CORS，允许前端跨域请求
CORS(app, resources={
    r"/api/*": {
        "origins": app.config['FRONTEND_ORIGIN'],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# 初始化AI服务 - 文字模型（用于文字搜题）
text_ai_service = AIService(
    api_key=app.config['AI_API_KEY'],
    api_base=app.config['AI_API_BASE'],
    model=app.config['AI_MODEL']
)

# 初始化AI服务 - 视觉模型（用于拍照搜题）
vision_ai_service = AIService(
    api_key=app.config['AI_VISION_API_KEY'],
    api_base=app.config['AI_VISION_API_BASE'],
    model=app.config['AI_VISION_MODEL']
)

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'ok',
        'message': 'AI Solver API is running'
    })

@app.route('/api/routing', methods=['GET'])
def get_routing_info():
    """
    获取模型路由配置信息
    展示当前使用的模型路由规则
    """
    return jsonify({
        'success': True,
        'data': {
            'routing_rules': {
                'text_search': {
                    'description': '文字搜题',
                    'endpoint': '/api/solve',
                    'method': 'POST',
                    'model_type': 'text',
                    'model': app.config['AI_MODEL'],
                    'api_base': app.config['AI_API_BASE']
                },
                'image_search': {
                    'description': '拍照搜题',
                    'endpoint': '/api/solve-image',
                    'method': 'POST',
                    'model_type': 'vision',
                    'model': app.config['AI_VISION_MODEL'],
                    'api_base': app.config['AI_VISION_API_BASE']
                }
            },
            'note': '系统会根据不同的搜题方式自动路由到对应的AI模型'
        }
    })

@app.route('/api/solve', methods=['POST'])
def solve_problem():
    """
    解题API接口
    接收题目，调用AI模型返回答案
    """
    try:
        data = request.get_json()
        
        if not data or 'problem' not in data:
            return jsonify({
                'success': False,
                'error': '缺少题目内容'
            }), 400
        
        problem = data['problem'].strip()
        
        if not problem:
            return jsonify({
                'success': False,
                'error': '题目内容不能为空'
            }), 400
        
        # 调用AI服务解题 - 使用文字模型
        solution = text_ai_service.solve_problem(problem)
        
        if solution:
            return jsonify({
                'success': True,
                'data': {
                    'problem': problem,
                    'solution': solution,
                    'model': app.config['AI_MODEL'],
                    'model_type': 'text'
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': '无法获取解答，请检查API配置'
            }), 500
    
    except Exception as e:
        app.logger.error(f"解题错误: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }), 500

@app.route('/api/solve-image', methods=['POST'])
def solve_image():
    """
    图片解题API接口
    接收图片，调用AI模型识别并解答
    """
    try:
        # 检查是否有文件上传
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': '缺少图片文件'
            }), 400

        file = request.files['image']

        if file.filename == '':
            return jsonify({
                'success': False,
                'error': '未选择图片文件'
            }), 400

        # 验证文件类型
        allowed_types = ['jpg', 'jpeg', 'png']
        file_type = imghdr.what(file)

        if file_type not in allowed_types:
            return jsonify({
                'success': False,
                'error': '不支持的图片格式，请上传 JPG 或 PNG 格式'
            }), 400

        # 读取图片并转换为Base64
        image_data = file.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')

        # 调用AI服务解题 - 使用视觉模型
        solution = vision_ai_service.solve_problem_with_image(image_base64)

        if solution:
            return jsonify({
                'success': True,
                'data': {
                    'problem': '图片题目（已识别）',
                    'solution': solution,
                    'model': app.config['AI_VISION_MODEL'],
                    'model_type': 'vision'
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': '无法获取解答，请检查API配置'
            }), 500

    except Exception as e:
        app.logger.error(f"图片解题错误: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }), 500

@app.route('/api/models', methods=['GET'])
def get_models():
    """获取可用的AI模型列表"""
    try:
        # 初始化AI_list实例
        ai_list = AI_list(
            api_key=app.config['AI_API_KEY'],
            api_base=app.config['AI_API_BASE'],
            model=app.config['AI_MODEL']
        )

        # 调用get_list方法获取模型列表
        models_response = ai_list.get_list()

        # 处理获取的模型列表
        available_models = models_response if models_response else [
            'gpt-3.5-turbo',
            'gpt-4',
            'gpt-4-turbo'
        ]

        # 如果获取失败，使用默认模型列表
        if not available_models:
            available_models = [
                'gpt-3.5-turbo',
                'gpt-4',
                'gpt-4-turbo'
            ]

        return jsonify({
            'success': True,
            'data': {
                'text_model': {
                    'current': app.config['AI_MODEL'],
                    'api_base': app.config['AI_API_BASE']
                },
                'vision_model': {
                    'current': app.config['AI_VISION_MODEL'],
                    'api_base': app.config['AI_VISION_API_BASE']
                },
                'available_models': available_models
            }
        })

    except Exception as e:
        app.logger.error(f"获取模型列表错误: {str(e)}")
        # 出错时返回默认模型列表
        return jsonify({
            'success': True,
            'data': {
                'text_model': {
                    'current': app.config['AI_MODEL'],
                    'api_base': app.config['AI_API_BASE']
                },
                'vision_model': {
                    'current': app.config['AI_VISION_MODEL'],
                    'api_base': app.config['AI_VISION_API_BASE']
                },
                'available_models': [
                    'gpt-3.5-turbo',
                    'gpt-4',
                    'gpt-4-turbo'
                ]
            }
        })

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
