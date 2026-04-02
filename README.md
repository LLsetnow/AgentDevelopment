# DeepSeek Agent 框架

一个简单易用的 Agent 开发框架，基于 DeepSeek API。

## 项目结构

```
AgentDevelopment/
├── simple.py                    # 主程序入口
├── config.yaml                  # 配置文件（不提交）
├── .gitignore                   # Git 忽略规则
│
├── skills/                      # 技能模块
│   ├── reasoning.py            # 推理能力
│   ├── planning.py             # 规划能力
│   └── memory.py               # 记忆管理
│
├── tools/                       # 工具函数
│   ├── web_tools.py            # 网络工具
│   ├── file_tools.py           # 文件工具
│   └── system_tools.py         # 系统工具
│
├── docs/                        # 参考文档
│   ├── 00-项目结构说明.md
│   ├── 01-技能开发指南.md
│   ├── 02-工具开发指南.md
│   ├── 03-配置说明.md
│   └── 04-最佳实践.md
│
├── examples/                    # 示例代码
│   ├── basic_usage.py          # 基础用法
│   ├── custom_skill.py         # 自定义技能
│   └── custom_tool.py          # 自定义工具
│
└── tests/                       # 测试代码
    ├── test_tools.py           # 工具测试
    └── test_skills.py          # 技能测试
```

## 快速开始

### 1. 安装依赖

```bash
pip install requests pyyaml
```

### 2. 配置 API Key

复制 `config.yaml.example`（如果有）并重命名为 `config.yaml`，填入你的 DeepSeek API Key：

```yaml
api:
  key: "your_deepseek_api_key_here"
  model: "deepseek-chat"

request:
  temperature: 0.7
```

或者直接编辑 `config.yaml` 文件。

### 3. 基础使用

```python
from simple import DeepSeekAgent, load_config

# 加载配置
config = load_config()
agent = DeepSeekAgent(api_key=config["api"]["key"])

# 简单对话
response = agent.chat("你好")
print(response)

# 思考任务
thought = agent.think("如何提高工作效率？")
print(thought)

# 制定计划
plan = agent.plan("学习 Python 编程")
print(plan)
```

## 主要功能

### 对话管理
- 支持多轮对话
- 自动保存历史记录
- 可清空对话历史

### 技能系统
- **推理技能**: 逻辑推理和问题分析
- **规划技能**: 制定执行计划
- **记忆技能**: 长期记忆存储和管理

### 工具系统
- **网络工具**: 搜索、网页获取
- **文件工具**: 读写、列表、删除
- **系统工具**: 时间、系统信息、命令执行

## 示例代码

### 使用技能

```python
from skills.reasoning import ReasoningSkill

# 创建技能
reasoning = ReasoningSkill(agent)

# 执行推理
result = reasoning.execute(problem="为什么物体下落时会加速？")
```

### 使用工具

```python
from tools.system_tools import get_current_time

# 获取当前时间
time_str = get_current_time()
print(time_str)
```

### 自定义技能

```python
from skills.reasoning import BaseSkill

class MySkill(BaseSkill):
    def execute(self, task: str) -> dict:
        # 实现你的逻辑
        return {
            "success": True,
            "result": f"处理了: {task}"
        }
```

### 自定义工具

```python
def my_tool(param: str) -> str:
    # 实现工具逻辑
    return f"结果: {param}"

# 添加到 Agent
agent.add_tool("my_tool", "工具描述", my_tool)

# 执行工具
result = agent.execute_tool("my_tool", param="测试")
```

## 运行示例

```bash
# 基础使用
python examples/basic_usage.py

# 自定义技能
python examples/custom_skill.py

# 自定义工具
python examples/custom_tool.py
```

## 运行测试

```bash
# 测试所有
python -m pytest tests/

# 测试工具
python tests/test_tools.py

# 测试技能
python tests/test_skills.py
```

## 文档

详细的开发文档请查看 `docs/` 目录：

- [项目结构说明](docs/00-项目结构说明.md)
- [技能开发指南](docs/01-技能开发指南.md)
- [工具开发指南](docs/02-工具开发指南.md)
- [配置说明](docs/03-配置说明.md)
- [最佳实践](docs/04-最佳实践.md)

## 安全建议

1. **不要提交 config.yaml**: 已在 `.gitignore` 中配置
2. **使用环境变量**: 敏感信息建议通过环境变量传递
3. **定期更换 API Key**: 定期更新你的 API 密钥

## 开发路线

- [ ] 支持流式响应
- [ ] 添加更多工具
- [ ] 支持多模态
- [ ] Web UI 界面
- [ ] 插件系统

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可

MIT License
