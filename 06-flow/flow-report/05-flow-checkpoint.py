import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from crewai.flow import Flow, start, listen, or_, and_
from crewai import Agent, Task, Crew
from crewai.state.checkpoint_config import CheckpointConfig
from dotenv import load_dotenv
import os, glob, json, shutil

load_dotenv("D:\\crewai\\learning-projects\\.env")

LLM_CONFIG = {
    "model": "deepseek-ai/DeepSeek-V4-flash",
    "base_url": "https://api.siliconflow.cn/v1",
    "api_key": os.getenv("OPENAI_API_KEY"),
    "custom_openai": True,
}

CHECKPOINT_DIR = "./.checkpoints/report"


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

    @listen(or_(research_market, research_tech))
    def quick_summary(self):
        topic = self.state["topic"]
        if "market_info" in self.state:
            text = f"快速预览 - {topic}\n\n【市场方面抢先完成】\n{self.state['market_info'][:200]}"
        else:
            text = f"快速预览 - {topic}\n\n【技术方面抢先完成】\n{self.state['tech_info'][:200]}"
        print(text)
        return text

    @listen(and_(research_market, research_tech))
    def full_report(self):
        return (
            f"完整报告 - {self.state['topic']}\n\n"
            f"市场方面：\n{self.state['market_info']}\n\n"
            f"技术方面：\n{self.state['tech_info']}"
        )


topic = input("输入报告主题：")
flow = ReportFlow()

checkpoint_files = sorted(glob.glob(f"{CHECKPOINT_DIR}/main/*.json"))
if checkpoint_files:
    latest = checkpoint_files[-1]
    with open(latest) as f:
        data = json.load(f)

    saved_topic = None
    for entity in data.get("entities", []):
        cs = entity.get("checkpoint_state")
        if cs:
            saved_topic = cs.get("topic")
            break

    if saved_topic == topic:
        print("话题一致，从 checkpoint 恢复（跳过已完成步骤）...")
        result = flow.kickoff(
            inputs={"topic": topic},
            from_checkpoint=CheckpointConfig(restore_from=latest),
        )
        print(result)
        exit()

    print(f"话题不一致（存档: {saved_topic} → 本次: {topic}），清空存档重新执行...")
    shutil.rmtree(CHECKPOINT_DIR)
else:
    print("首次运行，启用自动 checkpoint...")

flow.checkpoint = CheckpointConfig(
    location=CHECKPOINT_DIR,
    on_events=["method_execution_finished"],
)
result = flow.kickoff(inputs={"topic": topic})
print(result)
