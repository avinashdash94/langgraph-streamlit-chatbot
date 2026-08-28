import streamlit as st

#use below chatbot from langgraph_backend_streaming_data.py to get the streaming response
from langgraph_backend_streaming import chatbot
from langchain_core.messages import HumanMessage


CONFIG = { 'configurable':{'thread_id': 'thread-1'}}  # we are passing the thread_id to the config so that the chat state is maintained across multiple runs of the chatbot. It will save the state of the graph to a file and load it back when the graph is run again. It is useful for chatbots that need to maintain state across multiple runs.

# it will  store the chat so that same meessage chat_message() should not get  updated instead it should be stored in a variable called message_history and then it should be displayed in the chat message box as new message
# st.session_state it is a dictionary that will store the chat messages so that they can be displayed in the chat message box as new messages. 
# It will also store the user input so that it can be displayed in the chat message box as new messages.
# It will also store the assistant response so that it can be displayed in the chat message box as new messages.
# we are not using simple lit of message as on enter page reloads and the message array list becom empty and soing like updateing single message only not like chat conversation.
if "message_history" not in st.session_state:
    st.session_state['message_history'] = []

for message in st.session_state['message_history']:
    with st.chat_message(message["role"]):
        st.text(message["content"])

# below line to read user input from the chat input box and store it in a variable called user_input
user_input = st.chat_input("Type your message here...") 

if user_input:
    # below line to display the user input in the chat message box
    st.session_state['message_history'].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)
    
    # below code will shod the ai response in UI
    with st.chat_message("assistant"):
        # below code willl read the ai respose in sreaming mode and display it like typing effect.
        # we will store that final response in ai_messge varaible to store in st.session_state['message_history'].
        # so that it can be displayed in the chat message box as new messages and.
        ai_messge = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config = { 'configurable':{'thread_id': 'thread-2'}}  ,
                stream_mode = 'messages'
            )
        )

    st.session_state['message_history'].append({"role": "assistant", "content": ai_messge})