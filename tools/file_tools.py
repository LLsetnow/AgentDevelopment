"""文件操作工具"""
import os
from typing import List, Optional


def read_file(filepath: str, encoding: str = "utf-8") -> str:
    """
    读取文件内容
    
    Args:
        filepath: 文件路径
        encoding: 文件编码
        
    Returns:
        文件内容
    """
    try:
        with open(filepath, 'r', encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        return f"错误: 文件不存在 - {filepath}"
    except PermissionError:
        return f"错误: 无权限读取文件 - {filepath}"
    except Exception as e:
        return f"读取文件失败: {str(e)}"


def write_file(filepath: str, content: str, mode: str = "w", encoding: str = "utf-8") -> str:
    """
    写入文件
    
    Args:
        filepath: 文件路径
        content: 文件内容
        mode: 写入模式（'w' 覆盖, 'a' 追加）
        encoding: 文件编码
        
    Returns:
        操作结果
    """
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, mode, encoding=encoding) as f:
            f.write(content)
        
        return f"文件写入成功: {filepath}"
    except PermissionError:
        return f"错误: 无权限写入文件 - {filepath}"
    except Exception as e:
        return f"写入文件失败: {str(e)}"


def list_files(directory: str, pattern: str = "*") -> List[str]:
    """
    列出目录中的文件
    
    Args:
        directory: 目录路径
        pattern: 文件匹配模式
        
    Returns:
        文件列表
    """
    try:
        import glob
        search_pattern = os.path.join(directory, pattern)
        files = glob.glob(search_pattern, recursive=False)
        return [os.path.basename(f) for f in files]
    except Exception as e:
        return [f"列出文件失败: {str(e)}"]


def delete_file(filepath: str) -> str:
    """
    删除文件
    
    Args:
        filepath: 文件路径
        
    Returns:
        操作结果
    """
    try:
        if not os.path.exists(filepath):
            return f"错误: 文件不存在 - {filepath}"
        
        os.remove(filepath)
        return f"文件删除成功: {filepath}"
    except PermissionError:
        return f"错误: 无权限删除文件 - {filepath}"
    except Exception as e:
        return f"删除文件失败: {str(e)}"


def file_exists(filepath: str) -> str:
    """
    检查文件是否存在
    
    Args:
        filepath: 文件路径
        
    Returns:
        "exists" 或 "not_exists"
    """
    return "exists" if os.path.exists(filepath) else "not_exists"
