from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool   # to make functions that will passed as tools to the agents
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch   #to have a search tool to pass to the agent

# these two libraries help us format the LLM responce
from typing import List
from pydantic import BaseModel, Field

class Source (BaseModel):
    """schema for a source used by the agent"
    # generating a pydantic object, nested pydantic object to format the output"""
    
    url:str = Field (description= "the url of the source")
    
class AgentResponce (BaseModel):
    """ Schema for agent response with answer and sources"""
    
    answer:str = Field (description = "the agents answer to the query")
    sources : List [Source] = Field (default_factory=list, description="list of the sources that are used to generate the answer")
    
llm = ChatOpenAI()
tools = [TavilySearch()]
agent = create_agent(model = llm, tools = tools , response_format= AgentResponce)



def main():
    print("second lesson is up and running")
    results = agent.invoke(
        {"messages":HumanMessage(
            content="can you fing 3 job postings for Agentic AI jobs in boston and give me the pay range"
            )
         }
        )
    
    print(results)
    
if __name__ == "__main__":
    main()