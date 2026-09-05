# In this file we will add feature to have left side menu to have new chat or reuse existing chat.
import streamlit as st

#use below chatbot from langgraph_backend_streaming_Database_SqlLite.py to get the streaming response
from langgraph_backend_streaming_Database_SqlLite import chatbot, retrive_all_threads
from langchain_core.messages import HumanMessage
import uuid # it is used to create a uinque random  id for each new chat.

#************* Utility Functions Start ***********************

def generate_thread_id():
    """Generate a unique thread ID."""
    thread_id = uuid.uuid4()
    print(f"Generated new thread ID: {thread_id}")
    return thread_id

# On click of "New Chat" button, reset the chat state and generate a new thread ID.
def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id # create and use new thread_id for new chat session.
    add_thread(st.session_state['thread_id'])  # Add the new thread ID to the list of chat threads.
    st.session_state['message_history'] = [] # reset the message history for new chat session. to start as fresh chat.

# Add a new thread ID to the list of chat threads if it doesn't already exist.(for side bar  previous conversations)
def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

# loadthe chat from chatbot state for the given thread_id and return the messages. on clcik of past converstion history.
def laod_conversation(thread_id):
    """Load the conversation for the given thread ID."""
    config = {"configurable": {"thread_id": thread_id}}
    state = chatbot.get_state(config=config)

    messages = (state.values or {}).get("messages", [])
    #print(messages)

    return messages
 
#************* Utility Functions End ***********************

# it will  store the chat so that same meessage chat_message() should not get  updated instead it should be stored in a variable called message_history and then it should be displayed in the chat message box as new message
# st.session_state it is a dictionary that will store the chat messages so that they can be displayed in the chat message box as new messages. 
# It will also store the user input so that it can be displayed in the chat message box as new messages.
# It will also store the assistant response so that it can be displayed in the chat message box as new messages.
# we are not using simple lit of message as on enter page reloads and the message array list becom empty and soing like updateing single message only not like chat conversation.
if "message_history" not in st.session_state:
    st.session_state['message_history'] = []

if "thread_id" not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id() # Generate a new thread ID for the first chat session.

# It will create session for side bar previous conversations chat id.
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrive_all_threads()  # On load of the app, retrieve all existing chat threads from the database.

add_thread(st.session_state['thread_id'])  # Add the current thread ID to the list of chat threads.(on laod of Page)

#*****************Left Side Menu for New Chat and Existing Chat Start***********************
st.sidebar.title("Lnagraph Chatbot")
if st.sidebar.button("New Chat"): # this is syntex of button click  in streamlit. using If and call reset_chat() funtion.
    reset_chat()  # Reset the chat state and generate a new thread ID for a new chat session.
st.sidebar.header("My Conversations")
# Note: below comented line is to show single  chat thread id in side bar.
#st.sidebar.text(st.session_state['thread_id']) # Display the current thread ID in the sidebar.

# Display the list of existing chat threads in the sidebar.
for thread_id in st.session_state['chat_threads'][::-1]:  # Display the threads in reverse order (most recent first).
    # bewlo if is the way to call a fucntion on click of button.
    if st.sidebar.button(str(thread_id)):  # Display each thread ID in the sidebar.
        messages = laod_conversation(thread_id)  # Load the conversation for the selected thread ID.
       
        # As the st.session_state['message_history'] have diffrent messages formate and laod_conversation() is re sturning diffrent format
        # So we have to fomrate the messges for the session message_history in the form of {"role": "user", "content": user_input} and {"role": "assistant", "content": ai_messge} so that it can be displayed in the chat message box as new messages.
        temp_messages= []
        for message in messages:
            if isinstance(message, HumanMessage):
                role = "user"
            else:
                role = "assistant"
            temp_messages.append({"role": role, "content": message.content})

        st.session_state['message_history'] = temp_messages  # Update the message history for the selected thread ID.

#*****************Left Side Menu for New Chat and Existing Chat End***********************

for message in st.session_state['message_history']:
    with st.chat_message(message["role"]):
        st.text(message["content"])

# below line to read user input from the chat input box and store it in a variable called user_input
user_input = st.chat_input("Type your message here...") 

if user_input and user_input.strip():
    user_input = user_input.strip()
    # below line to display the user input in the chat message box
    st.session_state['message_history'].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)

    # creting config for session state management of chat.
    print(f"Using thread ID: {st.session_state['thread_id']} for the current chat session.")
    
    CONFIG = { 'configurable':{'thread_id': st.session_state['thread_id']}}  # st.session_state['thread_id'] is generated at the time of new  chat creation.        
    # below code will shod the ai response in UI
    with st.chat_message("assistant"):
        # below code willl read the ai respose in sreaming mode and display it like typing effect.
        # we will store that final response in ai_messge varaible to store in st.session_state['message_history'].
        # so that it can be displayed in the chat message box as new messages and.
        ai_messge = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config = CONFIG,
                stream_mode = 'messages'
            )
        )

    st.session_state['message_history'].append({"role": "assistant", "content": ai_messge})