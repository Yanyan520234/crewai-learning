from crewai import  Agent,Task,Crew
from dotenv import  load_dotenv
load_dotenv('d:\crewai\learning-projects\.env')
researcher=Agent(
    role="文化习俗研究员",
    goal="收集{topic}的最新资料和相关信息",
    backstory="经验丰富的信息收集专家",
    llm="openai/Qwen/Qwen2.5-7B-Instruct"
)

writer=Agent(
    role="写作者",
    goal="将收集到的信息写成通俗易懂的内容",
    backstory="写作经验丰富的专家，喜欢将专业知识写成通俗易懂",
    llm="openai/Qwen/Qwen2.5-7B-Instruct"
)

reveiwer=Agent(
    role="审校",
    goal="检查本章质量，确保准确性和可读性",
    backstory="保持文章的严谨",
    llm="openai/deepseek-ai/DeepSeek-V4-Pro"
)
researcher_task=Task(
    description="将收集的{topic}整理，并且深入研究，并整理五个要点",
    expected_output="列出五个要点列表",
    agent=researcher
)

write_task=Task(
    description="根据调研的文章写出一个300字的通俗易懂文章",
    expected_output="300字左右的文章",
    agent=writer
)

reveiwer_task=Task(
    description="审校文章.提出修改意见",
    expected_output="列出修改意见",
    agent=reveiwer
)

crew=Crew(
    agents=[researcher,writer,reveiwer],
    tasks=[researcher_task,write_task,reveiwer_task],
    share_crew=False
)

topic=input("请输入话题:")

result = crew.kickoff(inputs={"topic":topic})
for i,tasks_output in enumerate(result.tasks_output):
    print(f"\n{'='*50}")
    print(f"\n第{i+1}步输出")
    print(f"\n{'='*50}")
    print(tasks_output.raw)