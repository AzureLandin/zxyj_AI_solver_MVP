"""
AI服务模块
负责调用大模型API解题
"""

import openai
import requests
import json
import os
from typing import Optional, Dict, Any


class AIServiceError(Exception):
    """AI服务基础异常"""
    pass


class AIServiceInitError(AIServiceError):
    """AI服务初始化异常"""
    pass


class AIServiceAPIError(AIServiceError):
    """AI服务API调用异常"""
    pass


class AIServiceConnectionError(AIServiceError):
    """AI服务连接异常"""
    pass


class AIService:
    """AI解题服务类"""
    
    def __init__(self, api_key: str, api_base: str, model: str):
        """
        初始化AI服务

        Args:
            api_key: API密钥
            api_base: API基础地址
            model: 模型名称

        Raises:
            AIServiceInitError: 当初始化失败时抛出
        """
        self.api_key = api_key
        self.api_base = api_base or 'https://api.openai.com/v1'
        self.model = model

        # 验证API密钥
        if not api_key or not api_key.strip():
            error_msg = "API密钥不能为空"
            print(f"OpenAI客户端初始化失败: {error_msg}")
            raise AIServiceInitError(error_msg)

        # 配置OpenAI客户端
        try:
            if api_base and api_base != 'https://api.openai.com/v1':
                # 使用自定义的API地址
                self.client = openai.OpenAI(
                    api_key=api_key,
                    base_url=api_base,
                    timeout=30.0  # 添加超时设置
                )
            else:
                # 使用默认的OpenAI地址
                self.client = openai.OpenAI(
                    api_key=api_key,
                    timeout=30.0
                )

            # 测试连接是否成功
            try:
                self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=1
                )
            except Exception as test_error:
                print(f"OpenAI客户端连接测试失败: {str(test_error)}")
                raise AIServiceInitError(f"API连接测试失败: {str(test_error)}")

        except AIServiceInitError:
            # 重新抛出初始化异常
            raise
        except Exception as e:
            error_msg = f"OpenAI客户端初始化失败: {str(e)}"
            print(error_msg)
            raise AIServiceInitError(error_msg)
    
    def solve_problem(self, problem: str) -> Optional[str]:
        """
        使用AI模型解决问题

        Args:
            problem: 问题描述

        Returns:
            解决方案文本，如果失败返回None

        Raises:
            AIServiceAPIError: 当API调用失败时抛出
            AIServiceConnectionError: 当网络连接失败时抛出
        """
        # 验证输入
        if not problem or not problem.strip():
            print("问题描述不能为空")
            return None

        try:
            # 构建提示词
            system_prompt = """你是一个专业的AI解题助手。请按照以下要求解答问题：

                1. 仔细阅读并理解题目
                2. 提供详细的解题步骤和思路
                3. 如果涉及计算，展示完整的计算过程
                4. 最后给出明确的答案
                5. 使用清晰、易懂的语言
                6. 对于数学问题，可以使用LaTeX格式表示公式
                7. 如果问题不完整或不清楚，请指出并请求澄清

                请按照以下格式回答：

                **问题分析**：
                [分析题目要求和已知条件]

                **解题思路**：
                [描述解题的整体思路和方法]

                **详细步骤**：
                [展示详细的解题步骤]

                **最终答案**：
                [给出明确的最终答案]

                现在开始解题："""

            user_prompt = f"题目：{problem}\n\n请详细解答这个问题。"

            # 调用API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=4000,
                top_p=0.9,
                frequency_penalty=0,
                presence_penalty=0,
                timeout=60.0  # 添加请求超时
            )

            # 提取回答
            if response.choices and len(response.choices) > 0:
                solution = response.choices[0].message.content
                if solution and solution.strip():
                    return solution
                else:
                    print("AI返回的答案为空")
                    return None
            else:
                print("AI未返回有效的选择")
                return None

        except openai.APITimeoutError as e:
            error_msg = f"API请求超时: {str(e)}"
            print(error_msg)
            raise AIServiceConnectionError(error_msg)
        except openai.APIConnectionError as e:
            error_msg = f"API连接错误: {str(e)}"
            print(error_msg)
            raise AIServiceConnectionError(error_msg)
        except openai.RateLimitError as e:
            error_msg = f"API调用频率超限: {str(e)}"
            print(error_msg)
            raise AIServiceAPIError(error_msg)
        except openai.APIStatusError as e:
            error_msg = f"API状态错误 (状态码: {e.status_code}): {str(e)}"
            print(error_msg)
            raise AIServiceAPIError(error_msg)
        except openai.APIError as e:
            error_msg = f"API调用错误: {str(e)}"
            print(error_msg)
            raise AIServiceAPIError(error_msg)
        except Exception as e:
            error_msg = f"未知错误: {str(e)}"
            print(error_msg)
            raise AIServiceAPIError(error_msg)
    
    def test_connection(self) -> bool:
        """
        测试API连接是否正常

        Returns:
            连接是否成功
        """
        try:
            # 发送一个简单的请求测试连接
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5,
                timeout=30.0
            )
            print("API连接测试成功")
            return True
        except openai.APITimeoutError as e:
            print(f"API连接测试超时: {str(e)}")
            return False
        except openai.APIConnectionError as e:
            print(f"API连接测试失败: {str(e)}")
            return False
        except openai.APIError as e:
            print(f"API连接测试失败: {str(e)}")
            return False
        except Exception as e:
            print(f"API连接测试失败: {str(e)}")
            return False

class AI_list(AIService):
    def __init__(self, api_key, api_base, model):
        super().__init__(api_key, api_base, model)
        self.api_base = api_base + "/models"
        self.api_key = api_key
        self.model = model
        
    def get_list(self):
        url = self.api_base + "/models"
        header = self.api_key
        try:

            response = requests.get(self.api_base, headers={"Authorization": f"Bearer {self.api_key}"})


            if response.status_code == 200:

                return response.json()

            else:

                print(f"获取列表失败，状态码: {response.status_code}")

                return []

        except Exception as e:

            print(f"获取列表时发生错误: {str(e)}")

            return []