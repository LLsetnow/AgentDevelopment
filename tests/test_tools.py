"""工具测试"""
import unittest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.system_tools import get_current_time, get_system_info
from tools.file_tools import read_file, write_file, file_exists, list_files


class TestSystemTools(unittest.TestCase):
    """系统工具测试"""
    
    def test_get_current_time(self):
        """测试获取当前时间"""
        time_str = get_current_time()
        self.assertIsNotNone(time_str)
        self.assertIn("-", time_str)  # 检查格式包含日期分隔符
    
    def test_get_system_info(self):
        """测试获取系统信息"""
        info = get_system_info()
        self.assertIn("os", info)
        self.assertIn("python_version", info)
        self.assertIn("architecture", info)


class TestFileTools(unittest.TestCase):
    """文件工具测试"""
    
    def setUp(self):
        """测试前准备"""
        self.test_file = "data/test_file.txt"
        self.test_content = "这是测试内容\n第二行"
    
    def tearDown(self):
        """测试后清理"""
        import os
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_write_and_read_file(self):
        """测试文件写入和读取"""
        # 写入文件
        write_result = write_file(self.test_file, self.test_content)
        self.assertIn("成功", write_result)
        
        # 读取文件
        read_result = read_file(self.test_file)
        self.assertEqual(read_result, self.test_content)
    
    def test_file_exists(self):
        """测试检查文件是否存在"""
        # 文件不存在
        self.assertEqual(file_exists(self.test_file), "not_exists")
        
        # 创建文件
        write_file(self.test_file, "test")
        
        # 文件存在
        self.assertEqual(file_exists(self.test_file), "exists")
    
    def test_list_files(self):
        """测试列出文件"""
        # 在 data 目录创建测试文件
        write_file("data/test1.txt", "test1")
        write_file("data/test2.txt", "test2")
        
        # 列出文件
        files = list_files("data", "test*.txt")
        
        # 检查结果
        self.assertGreater(len(files), 0)


if __name__ == '__main__':
    unittest.main()
