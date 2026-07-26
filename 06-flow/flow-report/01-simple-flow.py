from crewai.flow import Flow, start, listen
from dotenv import load_dotenv

load_dotenv("D:\\crewai\\learning-projects\\.env")


class ReportFlow(Flow):
    @start()
    def preprocess_topic(self):
        self.state["topic"] = self.state["topic"]

    @listen(preprocess_topic)
    def generate_outline(self):
        topic = self.state["topic"]
        self.state["outline"] = f"{topic}的三个方面：定义、应用、总结"

    @listen(generate_outline)
    def write_report(self):
        return f"关于【{self.state['topic']}】的报告\n\n{self.state['outline']}"


topic = input("输入报告主题：")

flow = ReportFlow()
result = flow.kickoff(inputs={"topic": topic})
print(result)
