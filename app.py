import time
import streamlit as st
import time
from langchain_core.messages import HumanMessage
from backend import workflow


if 'output' not in st.session_state:
    user_id = st.chat_input("🔐 Enter your ID", )
    
    if user_id in ['7']:    
        st.success(f"ID received: `{user_id}`")
        st.session_state['output'] = user_id
        st.rerun()
   
    elif user_id != None:
        st.error("🚨 Unauthorized access detected!")
        time.sleep(1.5)

        st.error("📡 Tracing IP address...")
        time.sleep(1.7)
        
        st.error("📡 IP address: 192.168.43.127")
        time.sleep(1.7)
        
        st.error("💾 Screenshot taken and archived.")
        st.markdown(
        """
        <audio autoplay>
        <source src="https://sounddino.com/mp3/5/screen-capture-sound-on-phone-or-pc.mp3">
        </audio>
        """,
        unsafe_allow_html=True
        )
        time.sleep(1.3)

        st.error("💀 You have 30 seconds to disconnect.")
        time.sleep(1.3)
        
        st.error("📞 Calling 911 and reporting digital break-in.")
        st.markdown(
        """
        <audio autoplay>
        <source src="https://sounddino.com/mp3/35/car-siren-police-ambulance-fire.mp3">
        </audio>
        """,
        unsafe_allow_html=True
        )
        
    else:
        
        st.markdown("---")  # horizontal line for visual break
        st.markdown("### 👤 User Identification")
        st.markdown("Please enter your unique ID to proceed.")
        st.info("Waiting for input...")
    
else:
    
    st.title("🧠 Chatbot")
    if 'messages' in st.session_state:
        pass
    else:
        st.session_state['messages'] = []

    for role_content in st.session_state['messages']:
        with st.chat_message(role_content['role']):
            st.text(role_content['content'])

        
    response = st.chat_input("write something here:..", )

    if response:
        st.session_state['messages'].append({'role': 'user', 'content': response})

        with st.chat_message('user'):
            st.text(response)    
            
        with st.chat_message('assistant'):
            thread_id = '2'
            config = {"configurable": {"thread_id": thread_id}}
            
            stream = workflow.stream({'messages': [HumanMessage(response)]}, 
                                     config = {'configurable': {'thread_id': thread_id}},
                                     stream_mode='messages'
                                     )
            
            ai_response = st.write_stream(message_chunk.content for message_chunk, _ in stream)
                    
            st.session_state['messages'].append({'role': 'assistant', 'content': ai_response})
                


