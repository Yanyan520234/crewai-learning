from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from dotenv import load_dotenv
load_dotenv('D:\\crewai\\learning-projects\\.env')
class CalculatorTool(BaseTool):
    name: str = "calculator"
    description: str = "处理计算问题"

    def _run(self, expression: str) -> str:
        try:
            return str(eval(expression))
        except:
            return "计算错误"

calculator = CalculatorTool()

agent = Agent(
    role="数学助手",
    goal="用计算器准确的算出{topic}答案",
    backstory="数学专家，擅长使用计算器",
    llm="openai/deepseek-ai/DeepSeek-V4-flash",
    function_calling_llm="openai/deepseek-ai/DeepSeek-V4-flash",
    tools=[calculator]

)

task=Task(
    description="不复杂的计算{topic}任务",
    expected_output="输出正确答案",
    agent=agent
)
crew=Crew(
    agents=[agent],
    tasks=[task],
    verbose=True
)

topic=input("请输入数学表达式:")

result=crew.kickoff(inputs={"topic":topic})
print (result.raw)
