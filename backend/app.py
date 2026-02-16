from flask import Flask, request, jsonify  # type: ignore[reportMissingImports]
from flask_cors import CORS  # type: ignore[reportMissingModuleSource]
from config import Config  # type: ignore[reportImplicitRelativeImport]
from services.ai_service import AIService, AI_list  # type: ignore[reportImplicitRelativeImport]

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

# 初始化AI服务
ai_service = AIService(
    api_key=app.config['AI_API_KEY'],
    api_base=app.config['AI_API_BASE'],
    model=app.config['AI_MODEL']
)

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'ok',
        'message': 'AI Solver API is running'
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
        
        # 调用AI服务解题
        solution = ai_service.solve_problem(problem)
        
        if solution:
            return jsonify({
                'success': True,
                'data': {
                    'problem': problem,
                    'solution': solution,
                    'model': app.config['AI_MODEL']
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
                'current_model': app.config['AI_MODEL'],
                'available_models': available_models
            }
        })

    except Exception as e:
        app.logger.error(f"获取模型列表错误: {str(e)}")
        # 出错时返回默认模型列表
        return jsonify({
            'success': True,
            'data': {
                'current_model': app.config['AI_MODEL'],
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
