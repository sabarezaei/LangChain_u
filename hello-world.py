
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

load_dotenv()

def main():
    print("Hello from langchain-u!")
    #print(os.environ.get("OPENAI_API_KEY"))
    
    
    information=  """ Elon Reeve Musk is a businessman and former public official who is the CEO and largest shareholder of Tesla and SpaceX. 
    Musk has been the wealthiest person in the world since 2025, and became the only trillionaire in terms of US dollars in June 2026; 
    as of July 10, 2026, Forbes estimates his net worth to be US$917 billion.

    Born into the wealthy Musk family in Pretoria, South Africa, Musk emigrated in 1989 to Canada;
    he has Canadian citizenship since his mother was born there. He received bachelor's degrees in 1997 from the University of Pennsylvania before moving to 
    California to pursue business ventures. In 1995, Musk co-founded Zip2, a web software company. Following its sale in 1999,
    he co-founded X.com, an e-commerce payment system that merged with Confinity in March 2000 to form PayPal, which was acquired by eBay in 2002.
    Musk also became an American citizen in 2002."""



    summary_template = """given the information {information} about a person, I want you to create:
    1- a short summary
    2- two interesting facts about them
    """
    #llm = ChatOpenAI(temperature=0, model= "gpt-5")
    
    llm = ChatOllama(temperature=0, model= "gpt-oss:latest")


    summary_prompt_template = PromptTemplate(input_variables=["information"],
                                             template = summary_template)
    
    chain = summary_prompt_template | llm 
    
    response = chain.invoke(input={"information": information})

    print (response.content)
    
if __name__ == "__main__":
    main()
