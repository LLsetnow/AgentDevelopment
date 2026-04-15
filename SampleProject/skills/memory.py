"""记忆技能"""
import json
import os
from typing import Dict, Any, List
from datetime import datetime


class MemorySkill(BaseSkill):
    """记忆技能：管理和存储长期记忆"""
    
    def __init__(self, agent=None, storage_path: str = "data/memory"):
        super().__init__(agent)
        self.storage_path = storage_path
        self.memory_file = os.path.join(storage_path, "memory.json")
        self._ensure_storage()
    
    def _ensure_storage(self):
        """确保存储目录存在"""
        os.makedirs(self.storage_path, exist_ok=True)
        
        # 如果记忆文件不存在，创建空文件
        if not os.path.exists(self.memory_file):
            self._save_memory({})
    
    def _load_memory(self) -> Dict[str, Any]:
        """加载记忆"""
        try:
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    
    def _save_memory(self, memory: Dict[str, Any]):
        """保存记忆"""
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(memory, f, ensure_ascii=False, indent=2)
    
    def execute(self, action: str, key: str = "", value: Any = None) -> Dict[str, Any]:
        """
        执行记忆操作
        
        Args:
            action: 操作类型（store, retrieve, delete, list, clear）
            key: 记忆键
            value: 记忆值（store 操作时使用）
            
        Returns:
            操作结果
        """
        try:
            memory = self._load_memory()
            
            if action == "store":
                result = self._store(memory, key, value)
            elif action == "retrieve":
                result = self._retrieve(memory, key)
            elif action == "delete":
                result = self._delete(memory, key)
            elif action == "list":
                result = self._list(memory)
            elif action == "clear":
                result = self._clear()
            else:
                return {
                    "success": False,
                    "result": None,
                    "message": f"未知操作: {action}",
                    "data": {}
                }
            
            return result
        except Exception as e:
            return {
                "success": False,
                "result": None,
                "message": f"记忆操作失败: {str(e)}",
                "data": {}
            }
    
    def _store(self, memory: Dict[str, Any], key: str, value: Any) -> Dict[str, Any]:
        """存储记忆"""
        memory[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        self._save_memory(memory)
        
        return {
            "success": True,
            "result": f"已存储记忆: {key}",
            "message": "存储成功",
            "data": {"key": key}
        }
    
    def _retrieve(self, memory: Dict[str, Any], key: str) -> Dict[str, Any]:
        """检索记忆"""
        if key in memory:
            return {
                "success": True,
                "result": memory[key]["value"],
                "message": "检索成功",
                "data": {
                    "key": key,
                    "timestamp": memory[key]["timestamp"]
                }
            }
        else:
            return {
                "success": False,
                "result": None,
                "message": f"记忆不存在: {key}",
                "data": {}
            }
    
    def _delete(self, memory: Dict[str, Any], key: str) -> Dict[str, Any]:
        """删除记忆"""
        if key in memory:
            del memory[key]
            self._save_memory(memory)
            
            return {
                "success": True,
                "result": f"已删除记忆: {key}",
                "message": "删除成功",
                "data": {"key": key}
            }
        else:
            return {
                "success": False,
                "result": None,
                "message": f"记忆不存在: {key}",
                "data": {}
            }
    
    def _list(self, memory: Dict[str, Any]) -> Dict[str, Any]:
        """列出所有记忆"""
        keys = list(memory.keys())
        
        return {
            "success": True,
            "result": keys,
            "message": f"共 {len(keys)} 条记忆",
            "data": {"count": len(keys)}
        }
    
    def _clear(self) -> Dict[str, Any]:
        """清空所有记忆"""
        self._save_memory({})
        
        return {
            "success": True,
            "result": "已清空所有记忆",
            "message": "清空成功",
            "data": {}
        }
    
    def get_description(self) -> str:
        return "记忆技能：存储、检索和管理长期记忆"
    
    def get_examples(self) -> List[str]:
        return [
            'skill.execute(action="store", key="用户偏好", value="喜欢简洁的回答")',
            'skill.execute(action="retrieve", key="用户偏好")',
            'skill.execute(action="list")',
            'skill.execute(action="delete", key="用户偏好")',
            'skill.execute(action="clear")'
        ]


# 导入基类
from .reasoning import BaseSkill
