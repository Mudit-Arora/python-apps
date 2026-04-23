import uuid
import os
from dotenv import load_dotenv
from datetime import datetime

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
# from langchain_ollama import ChatOllama
from langgraph.checkpoint.sqlite import SqliteSaver # Memory for the agent
import sqlite3

import gradio as gr

from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

def get_date():
    """Get the current date"""
    return datetime.now().strftime("%Y-%m-%d")

search = TavilySearchResults(api_key=os.getenv("TAVILY_API_KEY")) # Web Search Tool

conn = sqlite3.connect("langgraph.db", check_same_thread=False) # can have multiple instances of the app
checkpoint = SqliteSaver(conn=conn)

llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", api_key=api_key)
# llm = ChatOllama(model="qwen2.5:3b")

system_prompt = """
You are a helpful assistant that can answer questions and help with tasks.
Use the web search tool to find the latest information on the topic.
"""

agent = create_agent(model=llm,
                 tools=[get_date, TavilySearchResults()], 
                 system_prompt=system_prompt, 
                checkpointer=checkpoint) # Memory for the agent

# user_query = input("Enter a query: ")
# resposne = agent.invoke({"messages": [{"role": "user", "content": user_query}]})
# print(resposne['messages'][-1].content[0]['text']) # for Gemini
# print(resposne['messages'][-1].content) # for local LLM

def chat(message, history, thread_id):
    config = {"configurable": {"thread_id": thread_id}}
    response = agent.invoke(
        {"messages": [{"role": "user", "content": message}]},
        config=config)
    return response['messages'][-1].content[0]['text']

with gr.Blocks() as demo:
    gr.Markdown("# AI Agent") #H1 heading
    thread_id = gr.State(value= lambda: str(uuid.uuid4())) # for generating a unique thread id for each user
    gr.ChatInterface(fn=chat, additional_inputs=[thread_id])

demo.launch()