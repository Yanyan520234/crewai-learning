from crewai import Agent, Task, Crew
from crewai_tools import TXTSearchTool
from dotenv import load_dotenv

load_dotenv('D:\\crewai\\learning-projects\\.env')

search_tool = TXTSearchTool()

agent = Agent(
    role="文件搜索专家",
    goal="在文件中搜索指定的关键词",
    backstory="擅长从文件中快速定位信息的专家",
    llm="openai/deepseek-ai/DeepSeek-V4-flash",
    function_calling_llm="openai/deepseek-ai/DeepSeek-V4-flash",
    tools=[search_tool]
)

task = Task(
    description="在{topic}中搜索关键词并返回结果",
    expected_output="搜索结果",
    agent=agent
)

crew = Crew(agents=[agent], tasks=[task], verbose=True)

query = input("请输入搜索内容（如：txt文件路径中搜索关键词）：")
result = crew.kickoff(inputs={"topic": query})
print(result.raw)
