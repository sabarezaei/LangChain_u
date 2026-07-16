from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch





llm = ChatOpenAI()
tools = [TavilySearch()]
agent = create_agent(model = llm, tools = tools)



def main():
    print("second lesson is up and running")
    results = agent.invoke({"messages":HumanMessage(content="can you fing 3 job postings for Agentic AI jobs in boston and give me the pay range")})
    print(results)
    
if __name__ == "__main__":
    main()