from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver  # it will save the state of the graph to a file(it is in memory) and load it back when the graph is run again
from langgraph.graph.message import add_messages # it is a reducer fucntion that will add messages to the state of the graph
from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState): 
    
    groq_messages = []
    for message in state["messages"]:
        groq_messages.append({
            "role": "user",
            "content": message.content,
        })
    # send it  to llm
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=groq_messages,
    )
    # response store state
    answer = response.choices[0].message.content
    return {'messages': [answer]}

# MemorySaver is langgraph library to maintaining the chat state to remember the past conversation and continue the conversation from where it left off. It will save the state of the graph to a file and load it back when the graph is run again. It is useful for chatbots that need to maintain state across multiple runs.
checkpointer = MemorySaver()
graph = StateGraph(ChatState)
# add Nodes to graph
graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

# we are compiling the graph and passing the checkpointer to it so that it can save the state of the graph to a file and load it back when the graph is run again
chatbot = graph.compile(checkpointer=checkpointer)   

initial_state = {
    "messages": [
        HumanMessage(content="what is the capital of india?")
    ]
}

config = { 'configurable':{'thread_id': 1}}  

print(chatbot.invoke(initial_state, config=config)["messages"][-1].content)