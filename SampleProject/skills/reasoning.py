"""推理技能"""
from typing import Dict, Any, List
from abc import ABC, abstractmethod


class BaseSkill(ABC):
    """技能基类"""
    
    def __init__(self, agent=None):
        self.agent = agent
        self.name = self.__class__.__name__
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """执行技能"""
        pass
    
    def get_description(self) -> str:
        """获取技能描述"""
        return f"技能: {self.name}"


class ReasoningSkill(BaseSkill):
    """推理技能：逻辑推理和分析问题"""
    
    def execute(self, problem: str, context: str = "") -> Dict[str, Any]:
        """
        执行推理
        
        Args:
            problem: 要解决的问题
            context: 背景信息
            
        Returns:
            推理结果
        """
        try:
            # 构建推理提示
            if context:
                prompt = f"背景：{context}\n\n问题：{problem}\n\n请进行逻辑推理并给出分析。"
            else:
                prompt = f"问题：{problem}\n\n请进行逻辑推理并给出分析。"
            
            # 使用 Agent 进行推理（如果可用）
            if self.agent:
                result = self.agent.chat(prompt, save_to_history=False)
            else:
                # 简单模拟推理
                result = self._simulate_reasoning(problem)
            
            return {
                "success": True,
                "result": result,
                "message": "推理完成",
                "data": {
                    "problem": problem,
                    "context": context
                }
            }
        except Exception as e:
            return {
                "success": False,
                "result": None,
                "message": f"推理失败: {str(e)}",
                "data": {}
            }
    
    def _simulate_reasoning(self, problem: str) -> str:
        """模拟推理（当不可用 Agent 时）"""
        reasoning_steps = [
            "1. 分析问题的关键点",
            "2. 识别相关因素",
            "3. 建立逻辑关系",
            "4. 进行推导和验证",
            "5. 得出结论"
        ]
        
        result = f"针对问题：{problem}\n\n推理过程：\n"
        result += "\n".join(reasoning_steps)
        result += "\n\n这是一个模拟推理结果。连接真实 Agent 后可以获得更智能的分析。"
        
        return result
    
    def get_description(self) -> str:
        return "推理技能：对问题进行逻辑推理和分析"
    
    def get_examples(self) -> List[str]:
        return [
            'skill.execute(problem="为什么物体下落时会加速？")',
            'skill.execute(problem="如何提高工作效率？", context="当前工作时间为9点到18点")'
        ]
