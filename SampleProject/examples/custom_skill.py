"""自定义技能示例"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simple import DeepSeekAgent, load_config
from skills.reasoning import BaseSkill
from typing import Dict, Any, List


class AnalysisSkill(BaseSkill):
    """分析技能：自定义分析示例"""
    
    def execute(self, task: str, data: str = "") -> Dict[str, Any]:
        """
        执行分析任务
        
        Args:
            task: 分析任务描述
            data: 待分析的数据
            
        Returns:
            分析结果
        """
        try:
            # 构建分析提示
            if data:
                prompt = f"数据：{data}\n\n任务：{task}\n\n请进行分析。"
            else:
                prompt = f"任务：{task}\n\n请进行分析。"
            
            # 使用 Agent 进行分析
            if self.agent:
                result = self.agent.chat(prompt, save_to_history=False)
            else:
                result = f"模拟分析结果：针对任务 '{task}' 的分析\n这是一个示例，连接真实 Agent 后可以获得智能分析。"
            
            return {
                "success": True,
                "result": result,
                "message": "分析完成",
                "data": {
                    "task": task,
                    "data": data
                }
            }
        except Exception as e:
            return {
                "success": False,
                "result": None,
                "message": f"分析失败: {str(e)}",
                "data": {}
            }
    
    def get_description(self) -> str:
        return "分析技能：对数据和任务进行分析"
    
    def get_examples(self) -> List[str]:
        return [
            'skill.execute(task="分析销售趋势", data="本月销售额100万，上月80万")',
            'skill.execute(task="分析用户反馈")'
        ]


def main():
    # 加载配置
    config = load_config()
    api_key = config.get("api_key", "")
    
    if not api_key:
        print("错误: 请在 config.yaml 中配置 api_key")
        return
    
    # 创建 Agent
    agent = DeepSeekAgent(api_key=api_key)
    
    # 注册自定义技能
    analysis_skill = AnalysisSkill(agent)
    agent.add_tool("analysis", "分析技能，用于分析数据和任务", lambda task, data="": analysis_skill.execute(task, data))
    
    print("=" * 60)
    print("自定义技能使用示例")
    print("=" * 60)
    
    # 示例 1: 直接使用技能
    print("\n[示例 1: 直接使用自定义技能]")
    result = analysis_skill.execute(task="分析产品改进建议")
    print(f"任务: 分析产品改进建议")
    print(f"结果: {result['result']}\n")
    
    # 示例 2: 通过 Agent 使用技能
    print("[示例 2: 通过 Agent 使用技能]")
    tool_result = agent.execute_tool("analysis", task="分析市场机会")
    print(f"任务: 分析市场机会")
    print(f"结果: {tool_result}\n")
    
    # 示例 3: 带数据的分析
    print("[示例 3: 带数据的分析]")
    sales_data = """
    第一季度: 50万
    第二季度: 70万
    第三季度: 65万
    第四季度: 90万
    """
    result = analysis_skill.execute(task="分析销售趋势", data=sales_data)
    print(f"任务: 分析销售趋势")
    print(f"数据: {sales_data.strip()}")
    print(f"结果: {result['result']}\n")

if __name__ == "__main__":
    main()
