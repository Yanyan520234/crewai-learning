from crewai import Agent,Task,Crew,Process
from dotenv import load_dotenv
load_dotenv('D:\\crewai\\learning-projects\\.env')

internist=Agent(
    role="内科医生",
    goal="能够专业的处理内科问题",
    backstory="有丰富的内科知识，具有很强的专业性",
    llm="openai/deepseek-ai/DeepSeek-V4-flash"
)
sergeon=Agent(
    role="外科医生",
    goal="能够专业的处理外科手术，最大可能保障患者安全",
    backstory="有丰富的外科经验",
    llm="openai/deepseek-ai/DeepSeek-V4-flash"
)
pharmacist=Agent(
    role="药剂师",
    goal="根据诊断情况合理的开出药物",
    backstory="细心且负责的药剂师",
    llm="openai/deepseek-ai/DeepSeek-V4-flash"
)
internist_task=Task(
    description="诊断{topic}严重性,并能给出优秀的治疗方案",
    expected_output="判断是{topic}属于什么疾病，严重性，并给出治疗方案",
    agent=internist
)
sergeon_task=Task(
    description="诊断{topic}严重性,并能给出优秀的治疗方案",
    expected_output="判断是{topic}属于什么疾病，严重性，并给出治疗方案",
    agent=sergeon
)
pharmacist_task=Task(
    description="通过患者问题，给出适配效果好的药物",
    expected_output="给出药物，并说明为什么以及注意事项",
    agent=pharmacist
)
crew=Crew(
    agents=[internist,sergeon,pharmacist],
    tasks=[internist_task,sergeon_task,pharmacist_task],
    process=Process.hierarchical,
    manager_llm="openai/deepseek-ai/DeepSeek-V4-flash",
    verbose=True
)
topic=input("请输入症状:")
result = crew.kickoff(inputs={"topic": topic})
for i,task_output in enumerate(result.tasks_output):
    print(f"\n{'='*50}")
    print(f"第{i+1}步输出：")
    print(f"{'='*50}")
    print(task_output.raw)

