# =========================================================
#
# Use this file to get response as Streaming / Progressive Response
#
# stream() returns the LLM response progressively as message
# chunks while the model is generating the output.
# Use this when the frontend needs to display the response
# progressively instead of waiting for the complete response.
# =========================================================
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_groq import ChatGroq

# Below we use SqliteSaver instead of MemorySaver for persistent storage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages

from dotenv import load_dotenv
import sqlite3

# ---------------------------------------------------------
# Load environment variables from .env
# GROQ_API_KEY should be present in the .env file
# ---------------------------------------------------------
load_dotenv()


# ---------------------------------------------------------
# Create Groq LLM using LangChain integration
#
# ChatGroq automatically reads GROQ_API_KEY
# from the environment.
# ---------------------------------------------------------
llm = ChatGroq(
    model="openai/gpt-oss-120b"
)


# ---------------------------------------------------------
# Define LangGraph State
#
# add_messages is a reducer that appends new messages
# instead of replacing the existing conversation history.
# ---------------------------------------------------------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# ---------------------------------------------------------
# Chat Node
#
# We can directly pass LangChain messages to ChatGroq.
#
# HumanMessage -> user
# AIMessage    -> assistant
# SystemMessage -> system
#
# No manual role conversion is required.
# ---------------------------------------------------------
def chat_node(state: ChatState):
    messages = state.get("messages", [])
    if not messages:
        return {"messages": []}

    response = llm.invoke(messages)

    return {
        "messages": [response]
    }


# ---------------------------------------------------------
# SqliteSaver
#
# Maintains conversation state in a SQLite database.
# thread_id identifies a particular conversation.
#
# Note:
# sqlite3 will use to connect to the "chatbot.db" database. if it is not there it will crreat the database file automatically.
# check_same_thread=False allows SQLite to be used across multiple threads. As AI is using multiple threads, this is necessary. else it may raise threading errors.
# SqliteSaver provides persistent storage.
# Conversations are saved to "chatbot_memory.db".
# ---------------------------------------------------------
connection = sqlite3.connect(database="chatbot.db", check_same_thread=False)
checkpointer = SqliteSaver(conn = connection)


# ---------------------------------------------------------
# Build LangGraph
# ---------------------------------------------------------
graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)

graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)


# ---------------------------------------------------------
# Compile graph with memory
# ---------------------------------------------------------
chatbot = graph.compile(
    checkpointer=checkpointer
)

def retrive_all_threads():
    all_threads = set()
    # checkpointer.list(None) will give all the list of checkpoints stored in the database.
    # Annd store all unique thread IDs present in the database in the all_threads set.
    # we will use all_threads to get all the thread ids in frontend on laod of the app
    for checkpoint in checkpointer.list(None):
        #print(checkpoint.config['configurable']['thread_id'])
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)

# =========================================================
# Example 1:
# Streaming response
#
# stream_mode="messages" gives LLM message chunks while
# the model is generating the response.
# =========================================================

# print("\nTesting chatbot from backend:")

# CONFIG = { 'configurable':{'thread_id': 'thread-3'}}  # st.session_state['thread_id'] is generated at the time of new  chat creation.
# # below to test the streaming response from the chatbot
# response = chatbot.invoke(
#     {'messages': [HumanMessage(content="what is my name")]},
#     config = CONFIG,
#     stream_mode = 'messages'
# )
# print(response)  # Get the current state of the conversation for thread-1 
