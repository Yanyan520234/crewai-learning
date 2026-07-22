from crewai import Agent, Task, Crew
from dotenv import load_dotenv
load_dotenv('D:\\crewai\\learning-projects\\.env')

agent = Agent(
    role="技术研究员",
    goal="用中文回答{topic}的问题",
    backstory="资深工程师",
    llm="openai/deepseek-ai/DeepSeek-V3"
)

task = Task(
    description="解释{topic}的核心概念",
    expected_output="500字以内的中文解释",
    agent=agent
)

crew = Crew(agents=[agent], tasks=[task], share_crew=False)

while True:
    topic = input("\n请输入你想了解的话题（输入 q 退出）: ")
    if topic.lower() == 'q':
        break
    if not topic.strip():
        continue
    result = crew.kickoff(inputs={"topic": topic})
    print("\n" + "="*50)
    print(result.raw)
    print("="*50)
