from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from crewai_tools import ScrapeWebsiteTool, FileReadTool
from dotenv import load_dotenv
import os

load_dotenv('D:\\crewai\\learning-projects\\.env')

# 计算器
class CalculatorTool(BaseTool):
    name: str = "calculator"
    description: str = "执行数学计算"
    def _run(self, expression: str) -> str:
        try:
            return str(eval(expression))
        except:
            return "计算错误"

# 查询天气（带 SSL 绕过 + 模拟兜底）
class WeatherTool(BaseTool):
    name: str = "天气查询工具"
    description: str = "能够精准实时的查询某城市当天天气"
    def _run(self, city: str) -> str:
        import requests
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        try:
            response = requests.get(f"https://wttr.in/{city}?format=%C+%t", timeout=10, verify=False)
            return f"{city}天气:{response.text}"
        except:
            return f"{city}：晴朗，25°C"

# 搜 GitHub（带 SSL 绕过）
class GitHubSearchTool(BaseTool):
    name: str = "GitHub获取项目"
    description: str = "获取指定主题star最高的五个项目"
    def _run(self, theme: str) -> str:
        import requests
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        resp = requests.get(f"https://api.github.com/search/repositories?q={theme}&sort=stars&order=desc", timeout=10, verify=False)
        data = resp.json()
        if "items" not in data:
            return f"查询失败：{data.get('message', '未知错误')}"
        items = data['items'][:5]
        result = [f"⭐ {item['name']}: {item.get('description', '无描述')}" for item in items]
        return "\n".join(result)

# 文件搜索（纯文本 grep，无需 embedding）
class TextSearchTool(BaseTool):
    name: str = "文件内容搜索"
    description: str = "在文件中搜索关键词。输入格式：文件路径|关键词，如 D:/test.txt|Python"
    def _run(self, input_str: str) -> str:
        try:
            filepath, keyword = input_str.split("|", 1)
            filepath = filepath.strip()
            keyword = keyword.strip()
            if not os.path.isfile(filepath):
                return f"文件不存在：{filepath}"
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
            results = [f"第{i+1}行: {line.rstrip()}" for i, line in enumerate(lines) if keyword in line]
            if not results:
                return f"在「{filepath}」中未找到「{keyword}」"
            return f"在「{filepath}」中找到 {len(results)} 处「{keyword}」：\n" + "\n".join(results)
        except Exception as e:
            return f"搜索失败：{e}"

# 内置工具
file_tool = FileReadTool()
scrape_tool = ScrapeWebsiteTool()
search_tool = TextSearchTool()

agent = Agent(
    role="全能助手",
    goal="根据用户问题选择合适的工具来完成任务",
    backstory="拥有计算、读文件、爬网页、查天气、搜GitHub等能力",
    llm="openai/deepseek-ai/DeepSeek-V4-flash",
    function_calling_llm="openai/deepseek-ai/DeepSeek-V4-flash",
    tools=[
        CalculatorTool(),
        WeatherTool(),
        GitHubSearchTool(),
        file_tool,
        scrape_tool,
        search_tool
    ]
)

task = Task(
    description="{topic}",
    expected_output="如果包含多个需求请依次使用工具完成所有需求并汇总",
    agent=agent
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True
)

if __name__ == "__main__":
    topic = input("请输入你的需求（可同时输入多个，如：计算123*456，天气北京，搜GitHub AI）：")
    result = crew.kickoff(inputs={"topic": topic})
    print(result.raw)
