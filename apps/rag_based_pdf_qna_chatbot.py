## requirements
## llm model
## document loader
## text splitter
## embedding model
## vctor db
## streamlit

from dotenv import load_dotenv ## loads environment variables 
load_dotenv()

## libraries 
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader,CSVLoader,WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
import streamlit as st

## web interface
st.title(" RAG PDF Chatbot")
st.write("Ask Questions about your pdfs ")

## model
llm =ChatGroq(model="openai/gpt-oss-20b")

## document loader
## here we can upload any pdf or multiple pdfs aswell
## but for csvloader we need to make another loader named loader2 or anything
loader = PyPDFLoader("data/Data Science Bro_New (1) (2) (1).pdf")
docs=loader.load()
## and after creating loader2 docs will look like this docs=loader1.load() + loader2.load()

## text splitter
splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=500)
splitted_data=splitter.split_documents(docs)

## cache_resource helps stremlit to not build vector stores again and again
## and cache insure that it won't calculate the result again and again because its heavy 
@st.cache_resource
def get_vector_store():## this function creates the result of embeddings and vector db

    embedding=HuggingFaceEmbeddings( 
        model_name="Qwen/Qwen3-Embedding-0.6B"
    )

    vector_store=Chroma.from_documents(
        documents=splitted_data,
        embedding=embedding
    )

    return vector_store

vector_store=get_vector_store()

## history managment part
if "history" not in st.session_state:
    st.session_state.history=[]

for history in st.session_state.history:
    st.chat_message(history["role"]).markdown(history["content"])



query=st.chat_input("Ask Anything ?")
if query:
    st.chat_message("user").markdown(query)
    st.session_state.history.append({"role":"user","content":query})

    ## similarity_search helps in search similar result from vector db
    data=vector_store.similarity_search(query=query)

    context=""

    for doc in data:
        context +=doc.page_content + "\n"

    ## memory managmeent
    chat_history=""

    for history in st.session_state.history:
        chat_history += f'{history["role"]}:{history["content"]}\n'


    prompt=PromptTemplate.from_template("""
         you are a helpful assistant and provide answer based on the context for user question and
         if you don't know the answer , then you can say that 'sorry , not from this course '
          conversation history :{chat_history}
          context:{context}
          question:{question}
           """)
    ## this is where we provide our context and query to llm and llm answers 
    final_prompt=prompt.format(
        chat_history=chat_history,
        context=context,
        question=query
    )
    res = llm.invoke(final_prompt)

    st.chat_message("ai").markdown(res.content)
    st.session_state.history.append({"role":"ai","content":res.content})
        

    
    



