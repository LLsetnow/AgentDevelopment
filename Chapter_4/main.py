import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict, Any
import requests

# 加载 .env 文件中的环境变量
load_dotenv()

# ReAct 提示词模板
REACT_PROMPT_TEMPLATE = """
请注意，你是一个有能力调用外部工具的智能助手。

可用工具如下:
{tools}

请严格按照以下格式进行回应:

Thought: 你的思考过程，用于分析问题、拆解任务和规划下一步行动。
Action: 你决定采取的行动，必须是以下格式之一:
- `{{tool_name}}[{{tool_input}}]`:调用一个可用工具。
- `Finish[最终答案]`:当你认为已经获得最终答案时。
- 当你收集到足够的信息，能够回答用户的最终问题时，你必须在Action:字段后使用 Finish[最终答案] 来输出最终答案。

现在，请开始解决以下问题:
Question: {question}
History: {history}
"""

class HelloAgentsLLM:
    """
    为本书 "Hello Agents" 定制的LLM客户端。
    它用于调用任何兼容OpenAI接口的服务，并默认使用流式响应。
    """
    def __init__(self, model: str = None, apiKey: str = None, baseUrl: str = None, timeout: int = None):
        """
        初始化客户端。优先使用传入参数，如果未提供，则从环境变量加载。
        """
        self.model = model or os.getenv("LLM_MODEL_ID")
        apiKey = apiKey or os.getenv("LLM_API_KEY")
        baseUrl = baseUrl or os.getenv("LLM_BASE_URL")
        timeout = timeout or int(os.getenv("LLM_TIMEOUT", 60))
        
        if not all([self.model, apiKey, baseUrl]):
            raise ValueError("模型ID、API密钥和服务地址必须被提供或在.env文件中定义。")

        self.client = OpenAI(api_key=apiKey, base_url=baseUrl, timeout=timeout)

    def think(self, messages: List[Dict[str, str]], temperature: float = 0) -> str:
        """
        调用大语言模型进行思考，并返回其响应。
        """
        print(f"🧠 正在调用 {self.model} 模型...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
            )
            
            # 处理流式响应
            print("✅ 大语言模型响应成功:")
            collected_content = []
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True)
                collected_content.append(content)
            print()  # 在流式输出结束后换行
            return "".join(collected_content)

        except Exception as e:
            print(f"❌ 调用LLM API时发生错误: {e}")
            return None

class ToolExecutor:
    """
    一个工具执行器，负责管理和执行工具。
    """
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def registerTool(self, name: str, description: str, func: callable):
        """
        向工具箱中注册一个新工具。
        """
        if name in self.tools:
            print(f"警告:工具 '{name}' 已存在，将被覆盖。")
        self.tools[name] = {"description": description, "func": func}
        print(f"工具 '{name}' 已注册。")

    def getTool(self, name: str) -> callable:
        """
        根据名称获取一个工具的执行函数。
        """
        return self.tools.get(name, {}).get("func")

    def getAvailableTools(self) -> str:
        """
        获取所有可用工具的格式化描述字符串。
        """
        return "\n".join([
            f"- {name}: {info['description']}" 
            for name, info in self.tools.items()
        ])

class ReActAgent:
    def __init__(self, llm_client: HelloAgentsLLM, tool_executor: ToolExecutor, max_steps: int = 5):
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.max_steps = max_steps
        self.history = []

    def run(self, question: str):
        """
        运行ReAct智能体来回答一个问题。
        """
        self.history = [] # 每次运行时重置历史记录
        current_step = 0

        while current_step < self.max_steps:
            current_step += 1
            print(f"--- 第 {current_step} 步 ---")

            # 1. 格式化提示词
            tools_desc = self.tool_executor.getAvailableTools()
            history_str = "\n".join(self.history)
            prompt = REACT_PROMPT_TEMPLATE.format(
                tools=tools_desc,
                question=question,
                history=history_str
            )

            # 2. 调用LLM进行思考
            messages = [{"role": "user", "content": prompt}]
            response_text = self.llm_client.think(messages=messages)
            
            if not response_text:
                print("错误:LLM未能返回有效响应。")
                break

            # 3. 解析LLM的输出
            thought, action = self._parse_output(response_text)
            
            if thought:
                print(f"🤔 思考: {thought}")

            if not action:
                print("警告:未能解析出有效的Action，流程终止。")
                break

            # 4. 执行Action
            if action.startswith("Finish"):
                # 如果是Finish指令，提取最终答案并结束
                finish_match = re.match(r"Finish\[(.*)\]", action)
                if finish_match:
                    final_answer = finish_match.group(1)
                    print(f"🎉 最终答案: {final_answer}")
                    return final_answer
                else:
                    print(f"⚠️  警告:无法解析Finish指令: {action}")
                    return f"无法解析的Finish指令: {action}"
            
            tool_name, tool_input = self._parse_action(action)
            if not tool_name or not tool_input:
                observation = f"错误:无法解析Action格式 '{action}'。请使用格式: 工具名[输入内容]"
                self.history.append(f"Action: {action}")
                self.history.append(f"Observation: {observation}")
                print(f"👀 观察: {observation}")
                continue

            print(f"🎬 行动: {tool_name}[{tool_input}]")
            
            tool_function = self.tool_executor.getTool(tool_name)
            if not tool_function:
                observation = f"错误:未找到名为 '{tool_name}' 的工具。"
            else:
                observation = tool_function(tool_input) # 调用真实工具

            # (这段逻辑紧随工具调用之后，在 while 循环的末尾)
            print(f"👀 观察: {observation}")
            
            # 将本轮的Action和Observation添加到历史记录中
            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {observation}")

        # 循环结束
        print("已达到最大步数，流程终止。")
        return None

    def _parse_output(self, text: str):
        """解析LLM的输出，提取Thought和Action。
        """
        # Thought: 匹配到 Action: 或文本末尾
        thought_match = re.search(r"Thought:\s*(.*?)(?=\nAction:|$)", text, re.DOTALL)
        # Action: 匹配到文本末尾
        action_match = re.search(r"Action:\s*(.*?)$", text, re.DOTALL)
        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        return thought, action

    def _parse_action(self, action_text: str):
        """解析Action字符串，提取工具名称和输入。
        """
        match = re.match(r"(\w+)\[(.*)\]", action_text, re.DOTALL)
        if match:
            return match.group(1), match.group(2)
        return None, None


def search(query: str) -> str:
    """
    一个基于博查API的实战网页搜索引擎工具。
    它会智能地解析搜索结果，优先返回直接答案或知识图谱信息。
    """
    print(f"🔍 正在执行 [博查API] 网页搜索: {query}")
    try:
        # 从环境变量获取博查API配置
        api_endpoint = os.getenv("BOC_SEARCH_API_URL", "https://api.bochaai.com/v1/web-search")
        api_key = os.getenv("BOC_SEARCH_API_KEY")
        
        if not api_key or not api_endpoint:
            return "错误: BOC_SEARCH_API_URL 或 BOC_SEARCH_API_KEY 未在 .env 文件中配置。"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "query": query,
            "freshness": "oneYear",
            "summary": True,
            "count": 10
        }
        
        print(f"🌐 连接博查API: {api_endpoint}")
        response = requests.post(
            api_endpoint,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code != 200:
            return f"博查API请求失败，状态码: {response.status_code}, 响应: {response.text[:200]}"
        
        data = response.json()
        
        # 检查API返回状态码 - 博查API使用code=200表示成功
        if "code" in data and data["code"] != 200:
            error_msg = data.get('msg', "未知错误")
            return f"博查API返回错误 (code={data['code']}): {error_msg}"
        
        # 获取实际数据
        response_data = data.get("data", {})
        if not response_data:
            return "博查API返回的数据为空"
        
        # 智能解析:优先寻找最直接的答案
        # 1. 首先检查是否有直接答案（answer字段）
        if "answer" in response_data and response_data["answer"]:
            return f"直接答案:\n{response_data['answer']}"
        
        # 2. 检查是否有总结（summary字段） - 博查API的summary字段通常更完整
        if "summary" in response_data and response_data["summary"]:
            return f"搜索总结:\n{response_data['summary']}"
        
        # 3. 检查博查API的特殊格式：检查第一个结果的summary字段（如果有）
        web_pages = response_data.get("webPages", {})
        if web_pages and "value" in web_pages and web_pages["value"]:
            first_result = web_pages["value"][0] if isinstance(web_pages["value"], list) else {}
            
            # 优先返回更完整的summary字段
            if "summary" in first_result and first_result["summary"]:
                return f"知识摘要:\n{first_result['summary']}"
            
            # 如果没有summary，再返回snippet
            if "snippet" in first_result and first_result["snippet"]:
                return f"知识摘要:\n{first_result['snippet']}"
        
        # 4. 返回有机搜索结果（前三个）
        if "webPages" in response_data and response_data["webPages"]:
            web_pages = response_data["webPages"]
            if "value" in web_pages and web_pages["value"] and isinstance(web_pages["value"], list):
                # 返回前三个有机结果的摘要
                snippets = []
                for i, res in enumerate(web_pages["value"][:3]):
                    title = res.get("name", res.get("title", f"结果 {i+1}"))
                    snippet = res.get("snippet", res.get("description", ""))
                    if title or snippet:
                        snippets.append(f"[{i+1}] {title}\n{snippet}")
                
                if snippets:
                    return "\n\n".join(snippets)
        
        # 5. 尝试其他可能的格式
        for key in ["organic_results", "results", "items"]:
            if key in response_data and response_data[key]:
                items = response_data[key]
                if isinstance(items, list) and items:
                    snippets = []
                    for i, res in enumerate(items[:3]):
                        title = res.get("title", res.get("name", f"结果 {i+1}"))
                        snippet = res.get("snippet", res.get("description", ""))
                        if title or snippet:
                            snippets.append(f"[{i+1}] {title}\n{snippet}")
                    
                    if snippets:
                        return "\n\n".join(snippets)
        
        return f"对不起，没有找到关于 '{query}' 的信息。"

    except requests.exceptions.RequestException as e:
        return f"网络请求错误: {str(e)}"
    except json.JSONDecodeError as e:
        return f"解析API响应失败: {str(e)}"
    except Exception as e:
        return f"搜索时发生错误: {e}"


# --- 工具初始化与使用示例 ---
if __name__ == '__main__':
    # 1. 初始化工具执行器
    toolExecutor = ToolExecutor()

    # 2. 注册我们的实战搜索工具
    search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    toolExecutor.registerTool("Search", search_description, search)
    
    # 3. 打印可用的工具
    print("\n--- 可用的工具 ---")
    print(toolExecutor.getAvailableTools())

    # # 4. 智能体的Action调用，这次我们问一个实时性的问题
    # print("\n--- 执行 Action: Search['英伟达最新的GPU型号是什么'] ---")
    # tool_name = "Search"
    # tool_input = "英伟达最新的GPU型号是什么"

    # tool_function = toolExecutor.getTool(tool_name)
    # if tool_function:
    #     observation = tool_function(tool_input)
    #     print("--- 观察 (Observation) ---")
    #     print(observation)
    # else:
    #     print(f"错误:未找到名为 '{tool_name}' 的工具。")
    
    # 5. 测试 ReActAgent
    print("\n" + "="*60)
    print("🧪 测试 ReActAgent")
    print("="*60)
    
    try:
        # 初始化LLM客户端
        llm_client = HelloAgentsLLM()
        
        # 创建并运行ReActAgent
        agent = ReActAgent(llm_client=llm_client, tool_executor=toolExecutor, max_steps=5)
        
        # 测试1: 简单搜索问题
        print("\n📝 测试案例1: 搜索英伟达最新显卡")
        question1 = "英伟达最新的显卡型号是什么？"
        print(f"问题: {question1}")
        result1 = agent.run(question1)
        if result1:
            print(f"✅ ReActAgent返回结果: {result1[:200]}..." if len(result1) > 200 else f"✅ ReActAgent返回结果: {result1}")
        else:
            print("❌ ReActAgent未能返回结果")
        
        # 测试2: 简单问题测试
        print("\n📝 测试案例2: 简单搜索问题")
        question2 = "Python是什么？"
        print(f"问题: {question2}")
        
        # 重置agent的历史记录
        agent.history = []
        
        result2 = agent.run(question2)
        if result2:
            print(f"✅ ReActAgent返回结果: {result2[:200]}..." if len(result2) > 200 else f"✅ ReActAgent返回结果: {result2}")
        else:
            print("❌ ReActAgent未能返回结果")
            
        # 测试3: 模拟ReAct过程（不实际调用LLM）
        print("\n📝 测试案例3: 模拟ReAct推理过程")
        print("演示ReAct的思想-行动-观察循环:")
        
        print("\n1. Thought: 用户询问英伟达最新GPU型号，我需要使用Search工具查找相关信息。")
        print("   Action: Search[英伟达最新GPU型号]")
        print("   Observation: (搜索结果)")
        
        print("\n2. Thought: 根据搜索结果，我发现是RTX 50系列，现在需要了解具体特点和改进。")
        print("   Action: Search[英伟达RTX 50系列特点改进]")
        print("   Observation: (更详细的搜索结果)")
        
        print("\n3. Thought: 我已经收集到足够的信息，可以综合回答用户的问题。")
        print("   Action: Finish[英伟达最新的GPU型号是RTX 50系列...]")
        
        print("\n🎯 ReActAgent测试完成！")
        
    except Exception as e:
        print(f"❌ ReActAgent测试失败: {e}")
        print("提示: 请确保.env文件中有正确的LLM配置（API密钥、模型ID、Base URL）")
    