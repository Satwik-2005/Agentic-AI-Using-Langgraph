import streamlit as st
from chatbot_backend import workflow
from langchain_core.messages import HumanMessage

## Creating a session using threads and it should be configurable
CONFIG = {"configurable": {"thread_id": "thread-1"}}


## With st.sessioin state we can create a session and the data can be saved 
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []


## Loading the conversational history of the session
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])


## Taking the user input using st.chat_input() so we can get the avatar at the start
user_input = st.chat_input("Type here")


## Noe start the chatbot by printing the user message and the Ai Message
if user_input:
    ## First add the message to the message history
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.text(user_input)


    ## create response to provide AI Message
    response = workflow.invoke({"messages": [HumanMessage(content=user_input)]}, config=CONFIG)


    ## First add the message to the message history and the following response to the ai message
    # ai_message = response["messages"][-1].content
    ai_message = response["messages"][-1].content

    if isinstance(ai_message, list):
        ai_message = "\n".join (
            block["text"]
            for block in ai_message
            if block.get("type") == "text"
        )


    st.session_state["message_history"].append({"role": "assistant", "content": ai_message})

    with st.chat_message("assistant"):
        st.text(ai_message)