from crewai import Agent, Task, Crew
from crewai_tools import FileReadTool
from dotenv import load_dotenv

load_dotenv('D:\\crewai\\learning-projects\\.env')

file_tool = FileReadTool()

agent = Agent(
    role="文件分析师",
    goal="读取文件内容并总结关键信息",
    backstory="擅长阅读和分析文件的专家",
    llm="openai/deepseek-ai/DeepSeek-V4-flash",
    function_calling_llm="openai/deepseek-ai/DeepSeek-V4-flash",
    tools=[file_tool]
)

task = Task(
    description="读取{topic}文件的内容并总结",
    expected_output="文件内容总结",
    agent=agent
)

crew = Crew(agents=[agent], tasks=[task], verbose=True)

file_path = input("请输入文件路径：")
result = crew.kickoff(inputs={"topic": file_path})
print(result.raw)
