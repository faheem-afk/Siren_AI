import streamlit as st
import time
from langchain_core.messages import HumanMessage
from backend import workflow
import uuid


# utility functions:

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id


def reset_chat():
    st.session_state['messages'] = []
    
    
def append_threads(id):
    st.session_state['thread_history'].append(id)
    

def load_conversation(id):
    CONFIG = {'configurable': {'thread_id': id}}
    return workflow.get_state(config=CONFIG).values['messages']

    
# check if the message list exist in the session_state 
st.title("🧠 Chatbot")
if 'messages' in st.session_state:
    pass
else:
    st.session_state['messages'] = []

if 'thread_history' not in st.session_state:
    st.session_state['thread_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = str(generate_thread_id())
    append_threads(str(st.session_state['thread_id']))
        

# add a sidebar to the chatbot
st.sidebar.title("Langraph Chatbot")    
sidebar_button = st.sidebar.button("New Chat")
if sidebar_button:
    generated_id = str(generate_thread_id())
    st.session_state['thread_id'] = generated_id
    append_threads(generated_id)
    reset_chat()
    
    
st.sidebar.header("My Conversations")
for index, id_ in enumerate(st.session_state['thread_history']):
        if st.sidebar.button(f'chat {index+1}'):
            reset_chat()
            
            st.session_state['thread_id'] = id_
            CONFIG = {'configurable': {'thread_id': id_}}
            if 'messages' in workflow.get_state(config=CONFIG).values:
                messages = load_conversation(id_)
            
                for idx, messg in enumerate(messages):
                    if (idx+1) % 2 != 0:
                        st.session_state['messages'].append({'role': 'user', 'content': messg.content})
                    else:
                        st.session_state['messages'].append({'role': 'assistant', 'content': messg.content})
                        
            

# re-render all the saved messages from the message variable in session state for any effect
for role_content in st.session_state['messages']:
    with st.chat_message(role_content['role']):
        st.text(role_content['content'])


# input box
response = st.chat_input("write something here...")

# execute this if the user writes something to the chatbot
if response:
    st.session_state['messages'].append({'role': 'user', 'content': response})

    with st.chat_message('user'):
        st.text(response)    
    
    # send the user's response to the chatbot for processing
    with st.chat_message('assistant'):

        ai_message = st.write_stream(
                message_chunk.content for message_chunk, _ in workflow.stream(
                {'messages': [HumanMessage(content=response)]},
                config= {'configurable': {'thread_id': st.session_state['thread_id']}},
                stream_mode= 'messages'
            )
        )
    # save the ai assistant's reponse in the message variable of the session state
    st.session_state['messages'].append({'role': 'assistant', 'content': ai_message})
    