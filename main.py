"""Python file to serve as the frontend"""
import streamlit as st
from streamlit_chat import message
import os

st.set_page_config(page_title="ChatTube", page_icon=":robot:")
st.header("▶️ ChatCLB")
if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []


from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyMuPDFLoader

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
file_url = ''
if uploaded_file is not None:
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(f"{tmpdir}/{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
        file_url = f"{tmpdir}/{uploaded_file.name}"

if file_url:
    loader = PyMuPDFLoader(file_url)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_documents(texts, embeddings)
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever(search_kwargs={"k": 1})) 
else:
    pass
    
    
def get_text():
    input_text = st.text_input("You: ", "how can I optimise the schedule?", key="input")
    return input_text


user_input = get_text()
load_button = st.button('ask')

from langchain.document_loaders import YoutubeLoader
index = ""
if load_button:
    try:
        pass
    except Exception as e:
        st.write("error loading the video: "+ str(e))
else:
    st.write("Please ask me anything about Calabrio ;)")


if index == "":
    pass
else:
    with st.spinner('typing...'):
        output = qa.run(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output.response)


if st.session_state["generated"]:

    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        try:
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
        except:
            pass
