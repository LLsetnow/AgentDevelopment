"""基础使用示例"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simple import DeepSeekAgent, load_config

def main():
    # 加载配置
    config = load_config()
    api_key = config.get("api_key", "")
    
    if not api_key:
        print("错误: 请在 config.yaml 中配置 api_key")
        return
    
    # 创建 Agent
    agent = DeepSeekAgent(api_key=api_key)
    
    # 设置系统提示
    agent.set_system_prompt("你是一个智能助手，可以帮助用户完成各种任务。")
    
    print("=" * 60)
    print("DeepSeek Agent 基础使用示例")
    print("=" * 60)
    
    # 示例 1: 简单对话
    print("\n[示例 1: 简单对话]")
    response = agent.chat("你好，请介绍一下你自己")
    print(f"用户: 你好，请介绍一下你自己")
    print(f"助手: {response}\n")
    
    # 示例 2: 多轮对话
    print("[示例 2: 多轮对话]")
    response1 = agent.chat("什么是人工智能？")
    print(f"用户: 什么是人工智能？")
    print(f"助手: {response1}\n")
    
    response2 = agent.chat("它的应用领域有哪些？")
    print(f"用户: 它的应用领域有哪些？")
    print(f"助手: {response2}\n")
    
    # 示例 3: 思考任务
    print("[示例 3: 思考任务]")
    thought = agent.think("如何提高工作效率？")
    print(f"任务: 如何提高工作效率？")
    print(f"思考结果: {thought}\n")
    
    # 示例 4: 制定计划
    print("[示例 4: 制定计划]")
    plan = agent.plan("学习 Python 编程")
    print(f"目标: 学习 Python 编程")
    print(f"计划: {plan}\n")
    
    # 示例 5: 清空对话历史
    print("[示例 5: 清空对话历史]")
    print(f"清空前对话数: {len(agent.messages)}")
    agent.clear_messages()
    print(f"清空后对话数: {len(agent.messages)}\n")

if __name__ == "__main__":
    main()
