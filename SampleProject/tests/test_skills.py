"""技能测试"""
import unittest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.reasoning import ReasoningSkill
from skills.planning import PlanningSkill
from skills.memory import MemorySkill


class TestReasoningSkill(unittest.TestCase):
    """推理技能测试"""
    
    def setUp(self):
        """测试前准备"""
        self.skill = ReasoningSkill()
    
    def test_execute(self):
        """测试执行推理"""
        result = self.skill.execute(problem="为什么物体下落时会加速？")
        
        self.assertIsNotNone(result)
        self.assertIn("success", result)
        self.assertTrue(result["success"])
        self.assertIn("result", result)
        self.assertIsNotNone(result["result"])
    
    def test_execute_with_context(self):
        """测试带上下文的推理"""
        result = self.skill.execute(
            problem="如何提高工作效率？",
            context="当前工作时间为9点到18点"
        )
        
        self.assertTrue(result["success"])
        self.assertIn("工作效率", result["result"])
    
    def test_get_description(self):
        """测试获取技能描述"""
        description = self.skill.get_description()
        self.assertIn("推理", description)
    
    def test_get_examples(self):
        """测试获取示例"""
        examples = self.skill.get_examples()
        self.assertIsInstance(examples, list)
        self.assertGreater(len(examples), 0)


class TestPlanningSkill(unittest.TestCase):
    """规划技能测试"""
    
    def setUp(self):
        """测试前准备"""
        self.skill = PlanningSkill()
    
    def test_execute(self):
        """测试执行规划"""
        result = self.skill.execute(goal="学习 Python 编程")
        
        self.assertIsNotNone(result)
        self.assertTrue(result["success"])
        self.assertIn("result", result)
        self.assertIsNotNone(result["result"])
    
    def test_execute_with_constraints(self):
        """测试带约束条件的规划"""
        result = self.skill.execute(
            goal="开发一个 Web 应用",
            constraints="预算5000元",
            timeframe="2个月"
        )
        
        self.assertTrue(result["success"])
        self.assertIn("计划", result["result"])
    
    def test_get_description(self):
        """测试获取技能描述"""
        description = self.skill.get_description()
        self.assertIn("规划", description)


class TestMemorySkill(unittest.TestCase):
    """记忆技能测试"""
    
    def setUp(self):
        """测试前准备"""
        self.skill = MemorySkill(storage_path="data/test_memory")
        self.skill._ensure_storage()
    
    def test_store_and_retrieve(self):
        """测试存储和检索记忆"""
        # 存储记忆
        store_result = self.skill.execute(
            action="store",
            key="test_key",
            value="test_value"
        )
        self.assertTrue(store_result["success"])
        
        # 检索记忆
        retrieve_result = self.skill.execute(
            action="retrieve",
            key="test_key"
        )
        self.assertTrue(retrieve_result["success"])
        self.assertEqual(retrieve_result["result"], "test_value")
    
    def test_list_memory(self):
        """测试列出记忆"""
        # 存储多条记忆
        self.skill.execute(action="store", key="key1", value="value1")
        self.skill.execute(action="store", key="key2", value="value2")
        
        # 列出记忆
        list_result = self.skill.execute(action="list")
        
        self.assertTrue(list_result["success"])
        self.assertGreaterEqual(list_result["data"]["count"], 2)
    
    def test_delete_memory(self):
        """测试删除记忆"""
        # 存储记忆
        self.skill.execute(action="store", key="delete_test", value="value")
        
        # 删除记忆
        delete_result = self.skill.execute(action="delete", key="delete_test")
        self.assertTrue(delete_result["success"])
        
        # 验证已删除
        retrieve_result = self.skill.execute(action="retrieve", key="delete_test")
        self.assertFalse(retrieve_result["success"])
    
    def test_clear_memory(self):
        """测试清空记忆"""
        # 存储一些记忆
        self.skill.execute(action="store", key="clear_test", value="value")
        
        # 清空所有记忆
        clear_result = self.skill.execute(action="clear")
        self.assertTrue(clear_result["success"])
        
        # 验证已清空
        list_result = self.skill.execute(action="list")
        self.assertEqual(list_result["data"]["count"], 0)


if __name__ == '__main__':
    unittest.main()
