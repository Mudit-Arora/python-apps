import os
from dotenv import load_dotenv
from datetime import datetime

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
# from langchain_ollama import ChatOllama

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

def get_date():
    """Get the current date"""
    return datetime.now().strftime("%Y-%m-%d")

llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", api_key=api_key)
# llm = ChatOllama(model="qwen2.5:3b")

system_prompt = """
You are a helpful assistant that can answer questions and help with tasks.
"""

agent = create_agent(model=llm, tools=[get_date], system_prompt=system_prompt)

user_query = input("Enter a query: ")
resposne = agent.invoke({"messages": [{"role": "user", "content": user_query}]})
print(resposne['messages'][-1].content[0]['text'])
# print(resposne['messages'][-1].content)