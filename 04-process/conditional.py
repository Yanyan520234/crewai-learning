from crewai import Agent, Task, Crew, Process
from crewai.tasks.conditional_task import ConditionalTask
from dotenv import load_dotenv

load_dotenv('D:\\crewai\\learning-projects\\.env')

researcher = Agent(
    role="研究员",
    goal="对{topic}进行深入研究，整理五个关键要点",
    backstory="经验丰富的信息收集专家",
    llm="openai/deepseek-ai/DeepSeek-V4-flash"
)

writer = Agent(
    role="写作者",
    goal="根据调研结果写成通俗易懂的文章",
    backstory="写作经验丰富的专家",
    llm="openai/deepseek-ai/DeepSeek-V4-flash"
)

reviewer = Agent(
    role="审校",
    goal="检查文章质量，确保准确性和可读性",
    backstory="严谨的编辑",
    llm="openai/deepseek-ai/DeepSeek-V4-flash"
)

research_task = Task(
    description="对{topic}进行深入研究，整理五个关键要点",
    expected_output="关于{topic}的五个关键要点的调研笔记",
    agent=researcher
)

write_task = Task(
    description="根据调研结果写一篇带有一定专业性且通俗易懂的文章",
    expected_output="专业文章",
    agent=writer
)
def need_review(context) -> bool:
    return len(context.raw) > 700
review_task = ConditionalTask(
    description="审校文章，提出修改意见",
    expected_output="修改意见列表",
    agent=reviewer,
    context=[write_task],
    condition=need_review
)
crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[research_task, write_task, review_task],
    process=Process.sequential,
    verbose=True
)
topic = input("你需要的话题是:")
result = crew.kickoff(inputs={"topic": topic})
print(result.raw)
