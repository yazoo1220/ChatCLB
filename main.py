"""Python file to serve as the frontend"""
import streamlit as st
from streamlit_chat import message
import os
import tempfile

st.set_page_config(page_title="ChatTube", page_icon=":robot:")
st.header("▶️ ChatCLB")
if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []

from langchain.llms import OpenAI
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Pinecone


def get_chat_history(inputs) -> str:
    res = []
    for human, ai in inputs:
        res.append(f"Human:{human}\nAI:{ai}")
    return "\n".join(res)


llm = OpenAI(streaming=True, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]), verbose=True, temperature=0)
embeddings = OpenAIEmbeddings()
db = Pinecone.from_existing_index(embedding=embeddings,index_name="test")
retriever = db.as_retriever(search_kwargs={"k": 1})
chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever,get_chat_history=get_chat_history)
    
    
def get_text():
    input_text = st.text_input("You: ", "how can I optimise the schedule?", key="input")
    return input_text


user_input = get_text()
ask_button = st.button('ask')

if ask_button:
    chat_history = []
    result = qa({"question": user_input, "chat_history": chat_history})
    st.session_state.past.append(user_input)
    st.session_state.generated.append(result['answer'])

if st.session_state["generated"]:

    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        try:
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
        except:
            pass
