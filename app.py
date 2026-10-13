import sys
from pathlib import Path

system_path = Path(__file__).resolve().parents[2]
if str(system_path) not in sys.path:
    sys.path.insert(0,str(system_path))

from backend.agent import run_agent
import streamlit as st

st.set_page_config(
    page_title="EndoAgent",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 EndoAgent")
st.caption("Local autonomous assistant powered by ollama(`qwen2.5:7b`)")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Ask EndoAgent to play music, send an email, etc...")

if user_prompt:

    st.session_state["messages"].append({"role" : "user", "content" : user_prompt})

    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("EndoAgent is thinking..."):
            response = run_agent(user_prompt)
            st.markdown(response)

    st.session_state["messages"].append({"role": "assistant", "content" : response})        
