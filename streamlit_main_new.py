import streamlit as st
from dotenv import load_dotenv
import openai
import os
from app_main_new import main_agent 
import json

load_dotenv() 
openai_key = os.getenv("OPENAI_API_KEY")
openai.api_key=openai_key

st.title("Recruiter Chat Agent")
st.header("GenAI final project")
st.subheader('💡 Tip: input date for Schedule assistant')


# Sidebar functionalities
st.sidebar.title("Session Controls")

# Export chat history
if st.sidebar.button("📤 Export Chat History()"):
    history_text1 = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.get("messages", [])])
    with open("chat_history.txt", "w", encoding="utf-8") as f:
        f.write(history_text1)
    st.sidebar.success("Chat history exported to chat_history.txt")

# Start new session
if st.sidebar.button("🔄 Start New Session"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, thanks for submitting your application for our Python Developer role. Could you share a bit about your Python experience?"}
    ]
    st.sidebar.success("New session started!")

# Export chat history
if st.sidebar.button("📤 Export Chat History (JSON)"):
    # Convert chat history to JSON
    chat_json = json.dumps(st.session_state.get("messages", []), indent=2, ensure_ascii=False)
    
    # Save to file
    with open("chat_history.json", "w", encoding="utf-8") as f:
        f.write(chat_json)
    
    st.sidebar.success("Chat history exported to chat_history.json")


#--------------------------------------------------------
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, thanks for submitting your application for our Python Developer role. Could you share a bit about your Python experience?"}
    ]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Get user input
user_msg = st.chat_input("Type your message...")

if user_msg:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
        st.write(user_msg)
  
    history_text = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages])

    # Send to LangChain agent
    agent_response = main_agent.invoke({"input": history_text})

    #  extract last line as final response
    final_response = agent_response["output"]

    #new
    #  extract intermediate steps response#new
    intermediate_steps = agent_response.get("intermediate_steps", [])

    #new
    # Get the last tool used #new
    last_tool_name = None
    if intermediate_steps:
        last_tool_name = intermediate_steps[-1][0].tool  # This gives you the tool name, e.g., "info_advisor"
        last_tool_id = last_tool_name.split("_")[0].capitalize()  # e.g., "info" → "Info"
    else:
        last_tool_id = "None"



    # Add assistant response to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": final_response,
         "last_tool_used": last_tool_id  # This will be included in JSON export
         })
    with st.chat_message("assistant"):
        st.write(final_response)

    





