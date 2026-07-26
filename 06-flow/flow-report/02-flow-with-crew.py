from crewai.flow import Flow, start, listen
from crewai import Agent,Task,Crew
from dotenv import load_dotenv

load_dotenv("D:\\crewai\\learning-projects\\.env")


class ReportFlow(Flow):
    @start()
    def preprocess_topic(self):
        self.state["topic"] = self.state["topic"]

    @listen(preprocess_topic)
    def generate_outline(self):
        topic = self.state["topic"]
        agent=Agent(
            role="分析师",
            goal="生成专业且严谨的报告",
            backstory="资深行业分析师",
            llm="openai/deepseek-ai/DeepSeek-V4-flash"
        )
        task=Task(
            description=f"写{self.state["topic"]}主题的三个方面:定义，应用，总结",
            expected_output="三个方面的大纲",
            agent=agent,
        )  
        crew=Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )
        result=crew.kickoff(inputs={"topic":topic})
        self.state["outline"]=result.raw

    @listen(generate_outline)
    def write_report(self):
        return f"关于【{self.state['topic']}】的报告\n\n{self.state['outline']}"
topic = input("输入报告主题：")

flow = ReportFlow()
result = flow.kickoff(inputs={"topic": topic})
print(result)
