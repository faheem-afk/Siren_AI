from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from dotenv import load_dotenv
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
import time
import os
import streamlit as st

# load_dotenv()
openai_api_key = st.secrets.get("OPENAI_API_KEY")
llm = ChatOpenAI(openai_api_key = openai_api_key)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    
    
def chatbot(ChatState) -> dict:
    message = llm.invoke(ChatState['messages']).content
    
    return {"messages": message}


checkpointer = InMemorySaver()
graph = StateGraph(ChatState)

graph.add_node("chatbot", chatbot)

graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)

workflow = graph.compile(checkpointer=checkpointer)
