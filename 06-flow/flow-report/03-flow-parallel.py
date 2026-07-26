import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from crewai.flow import Flow, start, listen, router, and_
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
import os

load_dotenv("D:\\crewai\\learning-projects\\.env")

LLM_CONFIG = {
    "model": "deepseek-ai/DeepSeek-V4-flash",
    "base_url": "https://api.siliconflow.cn/v1",
    "api_key": os.getenv("OPENAI_API_KEY"),
    "custom_openai": True,
}


class ReportFlow(Flow):
    @start("调研")
    def research_market(self):
        agent = Agent(
            role="市场分析师",
            goal="分析市场方面的信息",
            backstory="资深市场分析师",
            llm=LLM_CONFIG,
        )
        task = Task(
            description=(
                f"调研{self.state['topic']}的市场方面，包括：\n"
                "1. 市场规模与增长趋势\n"
                "2. 主要品牌与竞争格局\n"
                "3. 目标用户群体分析\n"
                "4. 营销渠道与模式\n"
                "5. 市场机会与风险\n"
                "给出每个方面的具体分析"
            ),
            expected_output="市场方面的五个方面详细分析",
            agent=agent,
        )
        crew = Crew(agents=[agent], tasks=[task])
        result = crew.kickoff()
        self.state["market_info"] = result.raw

    @start("调研")
    def research_tech(self):
        agent = Agent(
            role="技术分析师",
            goal="分析技术方面的信息",
            backstory="资深技术分析师",
            llm=LLM_CONFIG,
        )
        task = Task(
            description=(
                f"调研{self.state['topic']}的技术方面，包括：\n"
                "1. 核心技术原理\n"
                "2. 生产工艺/流程\n"
                "3. 技术发展趋势\n"
                "4. 关键技术瓶颈\n"
                "5. 技术差异对比\n"
                "给出每个方面的具体分析"
            ),
            expected_output="技术方面的五个方面详细分析",
            agent=agent,
        )
        crew = Crew(agents=[agent], tasks=[task])
        result = crew.kickoff()
        self.state["tech_info"] = result.raw

    @router(and_(research_market, research_tech), emit=["市场", "技术", "综合"])
    def classify_and_route(self):
        market = self.state["market_info"]
        tech = self.state["tech_info"]
        agent = Agent(
            role="分类专家",
            goal="判断报告类型",
            backstory="擅长内容分类",
            llm=LLM_CONFIG,
        )
        task = Task(
            description=f"市场内容：{market}\n技术内容：{tech}\n\n请判断这份报告应该归类为「市场」「技术」还是「综合」",
            expected_output="只输出「市场」「技术」或「综合」其中一个词",
            agent=agent,
        )
        crew = Crew(agents=[agent], tasks=[task])
        result = crew.kickoff()
        return result.raw.strip()

    @listen("市场")
    def write_market_report(self):
        return f"【市场报告】{self.state['topic']}\n\n{self.state['market_info']}"

    @listen("技术")
    def write_tech_report(self):
        return f"【技术报告】{self.state['topic']}\n\n{self.state['tech_info']}"

    @listen("综合")
    def write_comprehensive_report(self):
        return (
            f"【综合报告】{self.state['topic']}\n\n"
            f"市场方面：\n{self.state['market_info']}\n\n"
            f"技术方面：\n{self.state['tech_info']}"
        )


topic = input("输入报告主题：")
flow = ReportFlow()
result = flow.kickoff(inputs={"topic": topic})
print(result)
