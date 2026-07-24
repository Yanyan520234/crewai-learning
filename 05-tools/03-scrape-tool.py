from crewai import Agent, Task, Crew
from crewai_tools import ScrapeWebsiteTool
from dotenv import load_dotenv

load_dotenv('D:\\crewai\\learning-projects\\.env')

scrape_tool = ScrapeWebsiteTool()

agent = Agent(
    role="网页分析师",
    goal="爬取网页内容并提取关键信息",
    backstory="擅长从网页提取有用信息的专家",
    llm="openai/deepseek-ai/DeepSeek-V4-flash",
    function_calling_llm="openai/deepseek-ai/DeepSeek-V4-flash",
    tools=[scrape_tool]
)

task = Task(
    description="爬取{topic}的内容并用中文总结",
    expected_output="网页内容用中文总结",
    agent=agent
)

crew = Crew(agents=[agent], tasks=[task], verbose=True)

url = input("请输入网址：")
result = crew.kickoff(inputs={"topic": url})
print(result.raw)
