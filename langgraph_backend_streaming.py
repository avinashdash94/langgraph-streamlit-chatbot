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

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages

from dotenv import load_dotenv


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

    response = llm.invoke(state["messages"])

    return {
        "messages": [response]
    }


# ---------------------------------------------------------
# MemorySaver
#
# Maintains conversation state in memory.
# thread_id identifies a particular conversation.
#
# Note:
# MemorySaver is in-memory persistence.
# It does NOT permanently save conversations to a file.
# ---------------------------------------------------------
checkpointer = MemorySaver()


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



# =========================================================
# Example 1:
# Streaming response
#
# stream_mode="messages" gives LLM message chunks while
# the model is generating the response.
# =========================================================

print("\nStreaming Response:")

# below to test the streaming response from the chatbot
for message_chunk, metadata in chatbot.stream(
    {'messages': [HumanMessage(content="what is the recipe to make pasta in 100 word?")]},
    config = { 'configurable':{'thread_id': 'thread-2'}}  ,
    stream_mode = 'messages'
):

    if message_chunk.content:
        print(
            message_chunk.content,
            end="",
            flush=True
        )
