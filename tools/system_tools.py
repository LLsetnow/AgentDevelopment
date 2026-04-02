"""系统相关工具"""
import os
import platform
import subprocess
from datetime import datetime


def get_current_time(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    获取当前时间
    
    Args:
        format: 时间格式
        
    Returns:
        格式化的时间字符串
    """
    return datetime.now().strftime(format)


def get_system_info() -> dict:
    """
    获取系统信息
    
    Returns:
        系统信息字典
    """
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "hostname": platform.node()
    }


def get_disk_usage(path: str = ".") -> dict:
    """
    获取磁盘使用情况
    
    Args:
        path: 路径
        
    Returns:
        磁盘使用信息
    """
    try:
        import shutil
        usage = shutil.disk_usage(path)
        
        total_gb = usage.total / (1024**3)
        used_gb = usage.used / (1024**3)
        free_gb = usage.free / (1024**3)
        
        return {
            "total_gb": round(total_gb, 2),
            "used_gb": round(used_gb, 2),
            "free_gb": round(free_gb, 2),
            "usage_percent": round(usage.used / usage.total * 100, 2)
        }
    except Exception as e:
        return {"error": str(e)}


def run_command(command: str, timeout: int = 30) -> str:
    """
    运行系统命令（注意安全性）
    
    Args:
        command: 要执行的命令
        timeout: 超时时间（秒）
        
    Returns:
        命令输出
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout or result.stderr
    except subprocess.TimeoutExpired:
        return f"错误: 命令执行超时"
    except Exception as e:
        return f"执行命令失败: {str(e)}"


def get_environment_variable(name: str) -> str:
    """
    获取环境变量
    
    Args:
        name: 环境变量名
        
    Returns:
        环境变量值
    """
    value = os.getenv(name)
    return value if value is not None else f"环境变量 '{name}' 不存在"
