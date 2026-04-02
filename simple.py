import yaml
from dataclasses import dataclass
from typing import List, Optional, Callable, Any
import requests
from datetime import datetime

@dataclass
class Message:
    role: str
    content: str


def load_config(config_path: str = "config.yaml") -> dict:
    """
    从 YAML 文件加载配置
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        配置字典
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"配置文件 {config_path} 不存在，请先创建配置文件")
        return {}
    except Exception as e:
        print(f"加载配置文件失败: {str(e)}")
        return {}


class DeepSeekAgent:
    """简单的 Agent 框架，使用 DeepSeek API"""
    
    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        """
        初始化 Agent
        
        Args:
            api_key: DeepSeek API 密钥
            model: 使用的模型，默认为 deepseek-chat
        """
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.deepseek.com/chat/completions"
        self.messages: List[Message] = []
        self.tools: List[dict] = []
        self.system_prompt: Optional[str] = None
    
    def set_system_prompt(self, prompt: str):
        """设置系统提示词"""
        self.system_prompt = prompt
    
    def add_tool(self, tool_name: str, description: str, function: Callable):
        """
        添加工具
        
        Args:
            tool_name: 工具名称
            description: 工具描述
            function: 工具函数
        """
        self.tools.append({
            "name": tool_name,
            "description": description,
            "function": function
        })
    
    def clear_messages(self):
        """清空对话历史"""
        self.messages = []
    
    def _build_messages(self) -> List[dict]:
        """构建消息列表"""
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.extend([{"role": msg.role, "content": msg.content} for msg in self.messages])
        return messages
    
    def _call_api(self, messages: List[dict]) -> str:
        """调用 DeepSeek API"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            return f"API 调用失败: {str(e)}"
    
    def chat(self, user_message: str, save_to_history: bool = True) -> str:
        """
        与 Agent 对话
        
        Args:
            user_message: 用户消息
            save_to_history: 是否保存到对话历史
            
        Returns:
            Agent 的回复
        """
        # 添加用户消息
        if save_to_history:
            self.messages.append(Message(role="user", content=user_message))
        
        # 构建消息列表
        messages = self._build_messages()
        
        # 调用 API
        response = self._call_api(messages)
        
        # 保存助手回复
        if save_to_history:
            self.messages.append(Message(role="assistant", content=response))
        
        return response
    
    def think(self, task: str) -> str:
        """
        思考任务，返回详细的分析和解决方案
        
        Args:
            task: 任务描述
            
        Returns:
            思考结果
        """
        if not self.system_prompt:
            self.set_system_prompt("你是一个智能助手，擅长分析和解决问题。")
        
        prompt = f"请分析以下任务并提供详细的解决方案：\n\n任务：{task}"
        return self.chat(prompt)
    
    def plan(self, goal: str) -> str:
        """
        制定实现目标的计划
        
        Args:
            goal: 目标描述
            
        Returns:
            详细计划
        """
        if not self.system_prompt:
            self.set_system_prompt("你是一个规划专家，擅长制定详细的执行计划。")
        
        prompt = f"请为以下目标制定详细的执行计划：\n\n目标：{goal}"
        return self.chat(prompt)
    
    def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """
        执行指定工具
        
        Args:
            tool_name: 工具名称
            **kwargs: 工具参数
            
        Returns:
            工具执行结果
        """
        for tool in self.tools:
            if tool["name"] == tool_name:
                return tool["function"](**kwargs)
        return f"工具 '{tool_name}' 未找到"


def main():
    """示例用法"""
    # 从配置文件加载配置
    config = load_config()
    api_key = config.get("api_key", "")
    
    if not api_key:
        print("错误: 请在 config.yaml 中配置 api_key")
        return
    
    # 初始化 Agent
    agent = DeepSeekAgent(api_key=api_key)
    
    # 设置系统提示
    agent.set_system_prompt("你是一个智能助手，可以帮助用户完成各种任务。")
    
    # 添加一些示例工具
    def get_current_time():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def calculate_sum(a: float, b: float) -> float:
        return a + b
    
    agent.add_tool("get_time", "获取当前时间", get_current_time)
    agent.add_tool("calculate", "计算两个数的和", calculate_sum)
    
    print("=" * 50)
    print("DeepSeek Agent 框架")
    print("=" * 50)
    
    # 示例 1: 简单对话
    print("\n[示例 1: 简单对话]")
    response = agent.chat("你好，请介绍一下你自己")
    print(f"Assistant: {response}")
    
    # 示例 2: 思考任务
    print("\n[示例 2: 思考任务]")
    thought = agent.think("如何提高工作效率？")
    print(f"思考结果: {thought}")
    
    # 示例 3: 制定计划
    print("\n[示例 3: 制定计划]")
    plan = agent.plan("学习 Python 编程")
    print(f"计划: {plan}")
    
    # 示例 4: 使用工具
    print("\n[示例 4: 使用工具]")
    current_time = agent.execute_tool("get_time")
    result = agent.execute_tool("calculate", a=10, b=20)
    print(f"当前时间: {current_time}")
    print(f"计算结果: {result}")
    
    # 示例 5: 多轮对话
    print("\n[示例 5: 多轮对话]")
    response1 = agent.chat("什么是人工智能？")
    print(f"User: 什么是人工智能？")
    print(f"Assistant: {response1}")
    
    response2 = agent.chat("它的应用领域有哪些？")
    print(f"User: 它的应用领域有哪些？")
    print(f"Assistant: {response2}")


if __name__ == "__main__":
    main()
