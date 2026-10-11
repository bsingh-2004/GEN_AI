from dotenv import load_dotenv
load_dotenv()

## pypdfdirectoryloader is used to load multple files or documents better than pypdfloader
from langchain_community.document_loaders import PyPDFLoader,PyPDFDirectoryLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import InMemoryVectorStore ## we can also use Chroma db
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
import streamlit as st

## data in st session
if "document_uploaded" not in st.session_state: ## till document is not uploaded 
    st.session_state.document_uploaded=False

if "agent" not in st.session_state: ## till no agent is made
    st.session_state.agent=None

## after making document and agent make them true 

if "vector_store" not in st.session_state: ## till no vector db is made
    st.session_state.vector_store=None 

if "messages" not in st.session_state: ## till no message in session_state
    st.session_state.messages=[]

def process_documents(path):
## load the document
 loader = PyPDFDirectoryLoader(path)
 docs=loader.load()

 ## split into chunks
 splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
 docs=splitter.split_documents(docs)

 ## embeddings and vector db
 embedding=HuggingFaceEmbeddings( 
        model_name="Qwen/Qwen3-Embedding-0.6B"
    )
 ## we can also use chroma db
 vector_db=InMemoryVectorStore.from_documents(
    documents=docs,
    embedding=embedding
)
## create a agent - tool ,llm ,prompt
 llm=ChatGroq(model="openai/gpt-oss-20b")

 @tool ## creates tool
 def retrieve_context(query:str):
    """
    retrieve documents relevant to the query from the knowlegde base .
    """
    context=""

    docs=vector_db.similarity_search(query=query,k=4)
    for doc in docs:
        context +=doc.page_content + "\n\n"

    return context

 system_prompt="""you are a helpful assitant that answers questions using retrieved context.
 my knowledge base consists of the details from the uploaded documnent .
 always use the ' retrieve_context' tool for the question requiring external knowledge"""

 memory=InMemorySaver()
 agent=create_agent(
    model=llm,
    tools=[retrieve_context],
    system_prompt=system_prompt,
    checkpointer=memory
)
 ## after making , them make them true
 st.session_state.agent=agent
 st.session_state.document_uploaded=True

## upload ui
if not st.session_state.document_uploaded:
 ## till no document uploaded , this is the first thing visible on streamlit interface
    uploaded=st.file_uploader(label="select pdf files",type=["pdf"],accept_multiple_files=True)
    if uploaded:
        with st.spinner("processing..."):
            path = "./apps/docs_files/" ## this is the path on my  folder , we can also give any path 
 ## streamlit stores data in memory not in disk so we have to create path for storing files
            for file in uploaded:
                with open(path + file.name , "wb")as f:
## wb means write binary i.e pdfs are mixer of images ,text etc so wb converts pdfs into binary code
## what ever value we get from wb store it in path + file name , .getvalue() do this 
                    f.write(file.getvalue())
            process_documents(path)
            
            st.rerun()
## this is done to refresh streamlit as we have made uploaded and agent true in process_documnet function


## chat ui
## after uploading the document and making agent show this part 
## this is same 
if st.session_state.document_uploaded and st.session_state.agent:

    for message in st.session_state.messages:
        role=message.get("role")
        content=message.get("content")
        st.chat_message(role).markdown(content)

    query=st.chat_input("Ask anything related to uploaded document...")
    if query:
        st.session_state.messages.append({"role":"user","content":query})
        st.chat_message("user").markdown(query)
        response=st.session_state.agent.invoke(
            {"messages":[{"role":"user","content":query}]},
            {"configurable":{"thread_id":1}}
        )
        answer=response["messages"][-1].content

        st.chat_message("ai").markdown(answer)
        st.session_state.messages.append({"role":"ai","content":answer})