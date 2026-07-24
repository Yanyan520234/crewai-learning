from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from dotenv import load_dotenv

load_dotenv('D:\\crewai\\learning-projects\\.env')

class GitHubSearchTool(BaseTool):
    name: str = "GitHub项目搜索"
    description: str = "搜索 GitHub 上指定主题 star 最高的 5 个项目"

    def _run(self, theme: str) -> str:
        import requests
        try:
            resp = requests.get(
                f"https://api.github.com/search/repositories?q={theme}&sort=stars&order=desc",
                timeout=10
            )
            data = resp.json()
            if "items" not in data:
                return f"查询失败：{data.get('message', '未知错误')}"
            items = data['items'][:5]
            result = [f"⭐ {item['name']}: {item.get('description', '无描述')}" for item in items]
            return "\n".join(result)
        except Exception as e:
            return f"搜索失败：{e}"

agent = Agent(
    role="GitHub 项目搜索专家",
    goal="根据用户输入的主题搜索 GitHub 上 star 最高的项目",
    backstory="擅长发现优质开源项目的专家",
    llm="openai/deepseek-ai/DeepSeek-V4-flash",
    function_calling_llm="openai/deepseek-ai/DeepSeek-V4-flash",
    tools=[GitHubSearchTool()]
)

task = Task(
    description="搜索 GitHub 上关于{topic}的 star 最高的项目",
    expected_output="项目列表（名称+描述）",
    agent=agent
)

crew = Crew(agents=[agent], tasks=[task], verbose=True)

keyword = input("请输入搜索主题（如：AI、CrewAI、Python）：")
result = crew.kickoff(inputs={"topic": keyword})
print(result.raw)
