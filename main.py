import streamlit as st
from agent import run_agent
from config import WORKSPACE

st.set_page_config(page_title="CodePilot", page_icon="🤖", layout="wide")
st.title("🤖 CodePilot")
st.caption("Personal AI coding agent · controlled workspace")

with st.sidebar:
    st.subheader("Workspace")
    st.code(str(WORKSPACE))
    st.info("File operations are confined to this workspace. Generated code is not executed.")
    if st.button("Clear conversation"):
        st.session_state.messages=[]
        st.session_state.activity=[]
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages=[]
if "activity" not in st.session_state:
    st.session_state.activity=[]

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt=st.chat_input("Describe a coding task...")
if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        placeholder=st.empty()
        try:
            result, activity=run_agent(prompt, st.session_state.messages[:-1])
            placeholder.markdown(result)
            st.session_state.activity.extend(activity)
            st.session_state.messages.append({"role":"assistant","content":result})
        except Exception as e:
            placeholder.error(f"Agent error: {e}")
            st.session_state.messages.append({"role":"assistant","content":f"Agent error: {e}"})

if st.session_state.activity:
    with st.expander("Agent activity"):
        for item in st.session_state.activity[-60:]:
            st.write(item)
