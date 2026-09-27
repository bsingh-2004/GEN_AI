from dotenv import load_dotenv
import os

load_dotenv()


#LLM.TOOLS,AGENT,SYSTEM_PROMT 

from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit ## this provide pre-built tools to communicate  with database
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
import streamlit as st


db=SQLDatabase.from_uri("sqlite:///my_tasks.db")
db.run("""
    CREATE TABLE IF NOT EXISTS tasks(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      description TEXT,
      status TEXT  CHECK  (status IN('pending','in_progress','completed')) DEFAULT 'pending',
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

""")

## llm,toools,memory,system_prompt
model=ChatGroq(model="openai/gpt-oss-20b")
toolkit=SQLDatabaseToolkit(db=db,llm=model)
tools=toolkit.get_tools()  ## this will give every tool used for database
memory=InMemorySaver()

system_prompt="""
you are a task management assistant that interacts with a SQL database containing a 'tasks' table.

TASK RULES:
1. Limit select queries to 10 results max with ORDER BY created_at DESC 
2. After CREATE/UPDATE/DELETE , confirm with select query
3. If the user requests a list of tasks ,present the output in a structured table format  to ensure a clean and organized diaplay in the browser.

CRUD OPERATIONS:
  CREATE : Insert INto tasks(title,description,status)
  READ: select * from tasks where ... limit 10
  update: update tasks set status=? where id=? ot title=?
  DELETE: DELETE from tasks where id=? or title=?

Table schema : id,title,description,status(pending/in_progress/completed),created_at
"""
## whenever a user enters a query streamlit run the entire code from 1 to last line 
@st.cache_resource ## this decorator insures that this function does not run again and again
def get_agent(): ## this way we do not have to create session_state object of memory
    agent=create_agent(
        model=model,
        tools=tools,
        checkpointer=InMemorySaver(),
        system_prompt=system_prompt
    )
    return agent


agent=get_agent()

st.subheader("taskbot - manage your tasks")

if "message" not in st.session_state:
    st.session_state.history=[]

for message in st.session_state.history:
    st.chat_message(message["role"]).markdown(message["content"])


prompt=st.chat_input("Ask me to manage your tasks ?")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.history.append({"role":"user","content":prompt})
    with st.chat_message("ai"):
        with st.spinner("processing..."):
            response=agent.invoke(
                    {"messages":[{"role":"user","content":prompt}]},
                    {"configurable":{"thread_id":"1"}}
                )
            result=response["messages"][-1].content
            st.markdown(result)
            st.session_state.history.append({"role":"ai","content":result})

    
    


