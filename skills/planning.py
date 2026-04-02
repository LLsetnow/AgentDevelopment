"""规划技能"""
from typing import Dict, Any, List


class PlanningSkill(BaseSkill):
    """规划技能：制定任务执行计划"""
    
    def __init__(self, agent=None):
        super().__init__(agent)
    
    def execute(self, goal: str, constraints: str = "", timeframe: str = "") -> Dict[str, Any]:
        """
        执行规划
        
        Args:
            goal: 目标描述
            constraints: 约束条件
            timeframe: 时间范围
            
        Returns:
            规划结果
        """
        try:
            # 构建规划提示
            prompt_parts = [f"目标：{goal}"]
            
            if constraints:
                prompt_parts.append(f"约束条件：{constraints}")
            if timeframe:
                prompt_parts.append(f"时间范围：{timeframe}")
            
            prompt_parts.append("\n请为该目标制定详细的执行计划。")
            
            prompt = "\n".join(prompt_parts)
            
            # 使用 Agent 进行规划
            if self.agent:
                result = self.agent.chat(prompt, save_to_history=False)
            else:
                # 简单模拟规划
                result = self._simulate_planning(goal, constraints, timeframe)
            
            return {
                "success": True,
                "result": result,
                "message": "规划完成",
                "data": {
                    "goal": goal,
                    "constraints": constraints,
                    "timeframe": timeframe
                }
            }
        except Exception as e:
            return {
                "success": False,
                "result": None,
                "message": f"规划失败: {str(e)}",
                "data": {}
            }
    
    def _simulate_planning(self, goal: str, constraints: str, timeframe: str) -> str:
        """模拟规划（当不可用 Agent 时）"""
        plan = f"目标：{goal}\n\n"
        
        if constraints:
            plan += f"约束条件：{constraints}\n"
        
        if timeframe:
            plan += f"时间范围：{timeframe}\n"
        
        plan += "\n执行计划：\n"
        plan += "1. 分析目标和约束\n"
        plan += "2. 拆解任务为子任务\n"
        plan += "3. 确定优先级和依赖关系\n"
        plan += "4. 分配资源和时间\n"
        plan += "5. 制定执行步骤\n"
        plan += "6. 设定里程碑和检查点\n"
        plan += "7. 制定风险管理方案\n\n"
        plan += "这是一个模拟规划结果。连接真实 Agent 后可以获得更详细的计划。"
        
        return plan
    
    def get_description(self) -> str:
        return "规划技能：为给定目标制定详细的执行计划"
    
    def get_examples(self) -> List[str]:
        return [
            'skill.execute(goal="学习 Python 编程", timeframe="3个月")',
            'skill.execute(goal="开发一个 Web 应用", constraints="预算5000元，团队3人", timeframe="2个月")'
        ]


# 导入基类
from .reasoning import BaseSkill
