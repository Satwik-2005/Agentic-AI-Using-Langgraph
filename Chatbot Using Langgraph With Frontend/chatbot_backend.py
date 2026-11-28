## This file contains the backend code which has the graph and also its states

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages

from langchain_core.messages import BaseMessage
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from typing import TypedDict, Annotated
from dotenv import load_dotenv


## Loading the api keys
load_dotenv()


## Accessing the model through llm variable
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")


## Creating a state for the graph we gonna create
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


## Create the chat node using chat node function
def chat_node(state: ChatState) -> ChatState:
    messages = state["messages"]
    response = llm.invoke(messages)

    return {"messages": [response]}


## Creating a check pointer
check_pointer = InMemorySaver()


## Defining the graph
graph = StateGraph(ChatState)


## Add nodes
graph.add_node("chat_node", chat_node)


## Add edges
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)


## Compiling the graph
workflow = graph.compile(checkpointer=check_pointer)