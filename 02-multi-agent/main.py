from crewai import Agent, Task, Crew
from dotenv import load_dotenv
load_dotenv('D:\\crewai\\learning-projects\\.env')

# 3 个 Agent
researcher = Agent(
    role="研究员",
    goal="收集{topic}的最新资料和信息",
    backstory="经验丰富的信息搜集专家",
    llm="openai/Qwen/Qwen2.5-7B-Instruct"
)

writer = Agent(
    role="写作者",
    goal="将资料整理成通俗易懂的文章",
    backstory="资深科技写手",
    llm="openai/Qwen/Qwen2.5-7B-Instruct"
)

reviewer = Agent(
    role="审校",
    goal="检查文章质量，确保准确性和可读性",
    backstory="严谨的编辑",
    llm="openai/Qwen/Qwen2.5-7B-Instruct"
)

# 3 个 Task，研究员 → 写作者 → 审校 自动串联
research_task = Task(
    description="对{topic}进行深入调研，收集5个关键要点",
    expected_output="5个关键要点的列表",
    agent=researcher
)

write_task = Task(
    description="根据调研结果写一篇300字的文章",
    expected_output="300字左右的中文文章",
    agent=writer
)

review_task = Task(
    description="审校文章，给出修改建议",
    expected_output="修改意见列表",
    agent=reviewer
)

crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[research_task, write_task, review_task],
    share_crew=False
)

topic = input("请输入话题: ")
result = crew.kickoff(inputs={"topic": topic})
for i, task_output in enumerate(result.tasks_output):
    print(f"\n{'='*50}")
    print(f"第{i+1}步输出：")
    print(f"{'='*50}")
    print(task_output.raw)