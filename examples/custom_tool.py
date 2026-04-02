"""自定义工具使用示例"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simple import DeepSeekAgent, load_config
from tools.system_tools import get_current_time
from tools.file_tools import read_file, write_file
from tools.web_tools import search_web


def main():
    # 加载配置
    config = load_config()
    api_key = config.get("api_key", "")
    
    if not api_key:
        print("错误: 请在 config.yaml 中配置 api_key")
        return
    
    # 创建 Agent
    agent = DeepSeekAgent(api_key=api_key)
    
    # 添加自定义工具到 Agent
    agent.add_tool("get_time", "获取当前时间", get_current_time)
    agent.add_tool("read_file", "读取文件内容", read_file)
    agent.add_tool("write_file", "写入文件内容", write_file)
    agent.add_tool("search_web", "网络搜索", search_web)
    
    print("=" * 60)
    print("自定义工具使用示例")
    print("=" * 60)
    
    # 示例 1: 获取当前时间
    print("\n[示例 1: 获取当前时间]")
    current_time = agent.execute_tool("get_time")
    print(f"当前时间: {current_time}\n")
    
    # 示例 2: 读取文件
    print("[示例 2: 读取文件]")
    # 先创建一个示例文件
    test_file = "data/example.txt"
    write_file(test_file, "这是一个示例文件内容。\n用于演示文件操作工具。")
    
    file_content = agent.execute_tool("read_file", filepath=test_file)
    print(f"文件内容: {file_content}\n")
    
    # 示例 3: 写入文件
    print("[示例 3: 写入文件]")
    write_result = agent.execute_tool("write_file", filepath="data/output.txt", content="这是通过工具写入的内容。")
    print(f"写入结果: {write_result}\n")
    
    # 示例 4: 网络搜索
    print("[示例 4: 网络搜索]")
    search_result = agent.execute_tool("search_web", query="Python 编程", num_results=3)
    print(f"搜索结果: {search_result}\n")
    
    # 示例 5: 组合使用工具
    print("[示例 5: 组合使用工具]")
    # 获取时间 -> 记录到文件 -> 读取验证
    timestamp = agent.execute_tool("get_time")
    log_content = f"日志记录于: {timestamp}\n任务: 演示工具组合使用"
    
    agent.execute_tool("write_file", filepath="data/log.txt", content=log_content)
    log_content = agent.execute_tool("read_file", filepath="data/log.txt")
    
    print(f"组合操作结果:\n{log_content}\n")
    
    # 示例 6: 列出 Agent 的所有工具
    print("[示例 6: 列出所有工具]")
    if hasattr(agent, 'tools'):
        print(f"可用工具: {len(agent.tools)} 个")
        for tool in agent.tools:
            print(f"  - {tool['name']}: {tool['description']}")
    print()

if __name__ == "__main__":
    main()
