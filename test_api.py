#!/usr/bin/env python3
"""
AI解题助手 - API测试脚本
用于验证后端API是否正常工作
"""

import requests
import json
import sys
import time

def test_health():
    """测试健康检查接口"""
    print("\n【测试1】健康检查接口...")
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            print("  ✓ API正常运行")
            print(f"  响应: {response.json()}")
            return True
        else:
            print(f"  ✗ 响应异常: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("  ✗ 无法连接到后端服务")
        print("  请确保后端服务已启动: python backend/app.py")
        return False
    except Exception as e:
        print(f"  ✗ 错误: {e}")
        return False

def test_models():
    """测试模型信息接口"""
    print("\n【测试2】模型信息接口...")
    try:
        response = requests.get('http://localhost:5000/api/models', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"  ✓ 当前模型: {data['data']['current_model']}")
                print(f"  可用模型: {len(data['data']['available_models'])} 个")
                return True
        print(f"  ✗ 响应异常: {response.text}")
        return False
    except Exception as e:
        print(f"  ✗ 错误: {e}")
        return False

def test_solve():
    """测试解题接口"""
    print("\n【测试3】解题接口...")
    
    # 检查API密钥
    try:
        from backend.config import Config
        if not Config.AI_API_KEY or Config.AI_API_KEY == '':
            print("  ⚠ 警告: API密钥未配置")
            print("  请在 backend\.env 文件中配置 AI_API_KEY")
            print("\n  是否继续测试？(按回车继续，Ctrl+C退出)")
            input()
    except:
        pass
    
    # 测试题目
    test_problems = [
        "计算 2 + 2 * 3",
        "解方程 x + 5 = 10",
        "苹果原价5元，现在打8折，现价多少？"
    ]
    
    problem = test_problems[0]  # 使用第一个测试题
    
    print(f"\n  测试题目: {problem}")
    print("  正在调用AI解题...")
    
    try:
        response = requests.post(
            'http://localhost:5000/api/solve',
            json={'problem': problem},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("  ✓ 解题成功")
                print("\n  【题目】:")
                print(f"    {data['data']['problem']}")
                print("\n  【解答】:")
                solution = data['data']['solution']
                # 显示前500字符
                preview = solution[:500] + ("..." if len(solution) > 500 else "")
                for line in preview.split('\n'):
                    print(f"    {line}")
                print(f"\n  （共 {len(solution)} 字符）")
                return True
            else:
                print(f"  ✗ 解题失败: {data.get('error', '未知错误')}")
                return False
        else:
            print(f"  ✗ 响应异常: {response.status_code}")
            print(f"  响应: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("  ✗ 请求超时")
        print("  可能原因: AI API响应慢或网络问题")
        return False
    except Exception as e:
        print(f"  ✗ 错误: {e}")
        return False

def test_cors():
    """测试CORS配置"""
    print("\n【测试4】CORS跨域配置...")
    try:
        response = requests.get(
            'http://localhost:5000/api/health',
            headers={'Origin': 'http://localhost:8000'},
            timeout=5
        )
        if 'Access-Control-Allow-Origin' in response.headers:
            print(f"  ✓ CORS已配置: {response.headers['Access-Control-Allow-Origin']}")
            return True
        else:
            print("  ⚠ 警告: CORS头未找到")
            print("  前端可能无法正常访问API")
            return False
    except Exception as e:
        print(f"  ✗ 错误: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("AI解题助手 - API测试工具")
    print("=" * 60)
    print("\n开始测试API接口...")
    print("请确保后端服务已启动: python backend/app.py")
    print("\n" + "-" * 60)
    
    time.sleep(1)
    
    results = []
    
    # 运行测试
    results.append(("健康检查", test_health()))
    results.append(("模型信息", test_models()))
    results.append(("CORS配置", test_cors()))
    results.append(("解题接口", test_solve()))
    
    # 总结
    print("\n" + "=" * 60)
    print("测试结果总结:")
    print("=" * 60)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {name}: {status}")
    
    passed = sum(results)
    total = len(results)
    
    print("\n" + "-" * 60)
    print(f"总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！应用可以正常使用。")
        print("\n请访问: http://localhost:8000")
    else:
        print("\n⚠ 部分测试失败，请检查:")
        print("  1. 后端服务是否已启动")
        print("  2. API密钥是否正确配置")
        print("  3. 网络连接是否正常")
        print("  4. 查看上面的错误信息")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    try:
        main()
        input("\n按回车键退出...")
    except KeyboardInterrupt:
        print("\n\n测试已取消")
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")
