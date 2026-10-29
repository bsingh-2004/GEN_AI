from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from pydantic import BaseModel 
from typing import Literal 

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command



class BlogState(BaseModel):
    ## user input
    topic : str =""
    audience : str =""

    ## researcher output
    research : str =""
    research_feedback :str =""


    ## writer output
    draft : str =""
    draft_feedback : str =""


    ## editor output
    final_blog : str ="" 


    ## metadata
    revision_count : int =0


## defining methods

## this method is used for using llm without making llm object again and again
def get_llm(model_name : str ="openai/gpt-oss-20b",temperature : float =0.5):
    ## tempurature is not neccessary
    api_key=os.getenv("GROQ_API_KEY")
    llm=ChatGroq(model=model_name,temperature=temperature,api_key=api_key)
     ## we have to give api key here but its not neccessay
    return llm


## research agent

researcher_prompt=ChatPromptTemplate.from_messages([
    {"role":"system","content":"""
      "you are a research agent . given a blog topic and target audience , produce a clear,"
      "structured research outline . include :\n"
      "1. 5 -7 key points the blog should cover\n"
      "2. important facts , stats , or examples for each points\n"
      "3. suggested angle or hook\n"
      "be concise . use bullet points . do not write the full blog yet ."
      """},
    {"role":"user","content":"topic :{topic},audience:{audience},{revision_hints},write the research outline now"}
])
## this is also a method named researcher_agent
def researcher_agent(llm : ChatGroq, topic : str, audience : str, feedback : str="") -> str:
    revision_hints=f"the human provided this feedback on your previous research - please address it :{feedback}."
    if not feedback:
        revision_hints="this is your first attempt ."

    chain=researcher_prompt | llm

    result=chain.invoke({
        "topic":topic,
        "audience":audience,
        "revision_hints":revision_hints
    })
    return result.content

## writer agent
writer_prompt=ChatPromptTemplate.from_messages([
    {"role":"system","content":"""
      "you are a blog writer agent . using the research notes provided , write a complete ,"
      "engaging blog post .\n"
      "rules :\n"
      "length : 500 -800 words \n"
      "structure : catchy title , intro hook , 3-5 sections with h2 heading , conclusion\n"
      "tone : clear , friendly , suited to the target audience\n"
      "use markdown formattting\n"
      " do not add a 'word count' line at the end"
      """},
    {"role":"user","content":"""
          topic : {topic},
          audience :{audience},
          research notes : {research},

          {revision_hints}

          write a full blog post now .
        
     """}
])


def writer_agent(llm : ChatGroq, topic : str, audience : str, feedback : str="", research : str="") -> str:
    revision_hints=f"the human provided this feedback on your previous draft and asked for these changes:{feedback}. please apply these changes during writing the blog "
    if not feedback:
        revision_hints="this is your first attempt ."

    chain=writer_prompt | llm

    result=chain.invoke({
        "topic":topic,
        "audience":audience,
        "revision_hints":revision_hints,
        "research":research
    })
    return result.content



## editor agent
editor_prompt=ChatPromptTemplate.from_messages([
    {"role":"system","content":"""
      "you are an editor agent - the final quality gate before publishing.\n"
      "take the draft and produce the final polished version . specifically :\n"
      "- fix grammer , spellings , and awkward phrasing\n"
      "- tighten wordy sentences\n"
      "- improve flow and transition between sections\n"
      "- make the title and intro more compelling if needed\n"
      "- keep The same structure and markdown formatting\n"
      "blog wording should look like human , not AI , and don't use special chars and complex / fency word\n"
      "output only the final published blog post - no commentry."
      
      """},
    {"role":"user","content":"""
          topic : {topic},
          draft : {draft}

          return the published blog post.
        
     """}
])

def editor_agent(llm : ChatGroq, topic : str, draft:str="") -> str:
    

    chain=editor_prompt | llm

    result=chain.invoke({
        "topic":topic,
        "draft" : draft

    })
    return result.content


max_revision=3

## defining the  graph nodes

def researcher_node(state:BlogState):
    """researcher agent generates (or revises) the research outline"""## this dock string is not neccessary but better to keep this way
    llm=get_llm()

    research_data=researcher_agent(
        llm=llm,
        topic=state.topic,
        audience=state.audience,
        feedback=state.research_feedback

    )
    state.research=research_data ## updates the resource state 
    state.research_feedback= ""

    return state

def human_review_research_node(state:BlogState):
    """pause and ask the human to approve the research or send the feedback""" ## dock string tells how the node or tool works
    decision =interrupt({ ## decision is the response from the human
        "stage":"researcher_review",
        "research": state.research,           ## all these things are shown when interrupt happens
        "instructions":(
            "reply with approve to continue to writting",
            "or describe what to change to send it back to the researcher"
        )
    })
    ## decision can be a dictionary or a plain string , thats why this 
    if isinstance(decision,dict): ## if the decision comes as a dictionary then only this 
        action=decision.get("action","approve") 
        ## first value is what we want to get here its action and feedback from dictionary
        ## second value is a default value i.e if we get nothing then assume this
        feedback=decision.get("feedback" ,"")
    else:
        text=str(decision)
        action="approve" if text.lower() in ["approve","approved","ok"," yes","process",""] else "revise"
        feedback = "" if action =="approve" else text

    state.research_feedback=feedback
    return state



def writer_node(state:BlogState): ## this node takes writer_agent method 
    ## so we have to pass every argument passed in writer agent method
    """writer agent produce the full draft blog (or revive it)"""
    llm=get_llm()

    draft_data=writer_agent(
        llm=llm,
        topic=state.topic,
        audience=state.audience,
        feedback=state.draft_feedback,
        research=state.research
    )
    state.draft=draft_data
    state.draft_feedback= ""

    return state
## same node as research_review node just for draft
def human_review_draft_node(state:BlogState):
    """pause and ask the human to approve the draft or send the feedback"""
    decision =interrupt({
        "stage":"draft_review",
        "draft": state.draft,
        "instructions":(
            "reply with approve to continue to send the editor",
            "or describe what to change to send it back to the writer"
        )
    })
    if isinstance(decision,dict):
        action=decision.get("action","approve")
        feedback=decision.get("feedback" ,"")
    else:
        text=str(decision)
        action="approve" if text.lower() in ["approve","appreoved","ok"," yes","process",""] else "revise"
        feedback = "" if action =="approve" else text

    state.draft_feedback=feedback
    if feedback:
        state.revision_count += 1
      
    return state



def editor_node(state:BlogState): ## this node takes editor_agent method
    llm=get_llm()
    final=editor_agent(
        llm=llm,
        topic=state.topic,
        draft=state.draft
    )
    state.final_blog=final
    return state

## conditional edges

def route_after_research_review(state:BlogState) -> Literal["research","writer"]:
    if state.research_feedback:
        return "research"        ## if feedback then jump to research node else to writer node
    else:
        return "writer"




def route_after_draft_review(state:BlogState) -> Literal["edit","writer"]:
    if state.draft_feedback and state.revision_count <= max_revision:
        return "writer"    ## if max_revision count is more then 3 then jump to edit node no matter what
    else:                  ## if there is draft feedback rhen jump to writer node else jump to editor node
        return "edit"


## build and compile the graph
def build_blog_graph():  
    builder=StateGraph(BlogState)

    ##add  nodes 
    builder.add_node("research",researcher_node)
    builder.add_node("review_research",human_review_research_node)
    builder.add_node("writer",writer_node)
    builder.add_node("review_draft",human_review_draft_node)
    builder.add_node("edit",editor_node)




    ## add edge
    builder.add_edge(START,"research")
    builder.add_edge("research","review_research")                                ## there is no need to write this because its already written inside route_after_research_review
    builder.add_conditional_edges("review_research",route_after_research_review,{"research":"research" , "writer":"writer"})
    builder.add_edge("writer","review_draft")                                   ## same here but its just for more justification
    builder.add_conditional_edges("review_draft",route_after_draft_review,{"writer":"writer" , "edit":"edit"})
    builder.add_edge("edit",END)


    graph=builder.compile(checkpointer=InMemorySaver())

    return graph

## streamlit UI


st.title("✍️ AI Blog Writer")
st.write("Generate a blog using your AI agents.") ## these are headings for UI interface

topic = st.text_input("Enter Blog Topic") ## takes topic from user
audience = st.selectbox( ## takes audience input  from user as dropdown box
    "Select Audience",
    ["Beginners", "Students", "Working Professionals", "General Readers"]
)

config = {"configurable": {"thread_id": "1"}}
# thread_id identifies this graph execution so LangGraph can find
# its saved checkpoint when we resume the graph

if st.button("Generate Blog"): ## this means when user click the generate blog button
    if not topic.strip():
        st.warning("Please enter a topic.")## this will appear if there is no topic written by user
    else:
        graph = build_blog_graph() 

        result=graph.invoke({"topic":topic,"audience":audience},##graph already knows StateGraph(BlogState)
                            config=config)## these are the initial values in BlogState , when user pass these graph will start from these values
        st.session_state.result=result
        st.session_state.graph=graph  ## these are used to store the result and graph generated inside session state
        ## because streamlit reruns evrything its important to store the previous vlaues

# Human approval

if "result" in st.session_state: ## when there is some result store inside session_state
    result = st.session_state.result ## this fetch the result inside the result variable

    if result.get("__interrupt__"): ## if result is interrupt
        review = result["__interrupt__"][0].value ## takes all the value of interrupt inside review

        if review["stage"] == "researcher_review": ## when interrupt stage is researcher_review 
            st.subheader("Review Research")
            st.write(review["research"]) ## show the research done by the agent 

        else:
            st.subheader("Review Blog Draft") ## if there is no research_review then this 
            st.write(review["draft"])         ## because there are multiple interrupt in our graph

        feedback = st.text_input("What should be changed?") ## this takes feedback from user

        if st.button("Approve"):## when user click the approve button 
            result = st.session_state.graph.invoke( ## when user approve , so start from the previous interrupted graph
                Command(resume={
                    "action": "approve", ## command is approve so feedback is empty
                    "feedback": ""
                }),
                config=config ## configur is important for langgraph
            )

            st.session_state.result= result ## again store the recent result inside session_state 
            st.rerun() ## reruns the stremlit to change the value inside session_state.result and also display the recent value on UI

        if st.button("Request Changes"): ## if user click this button , request changes is the name of the button
            if feedback.strip(): ## strips the spaces from front and end
                result = st.session_state.graph.invoke(
                    Command(resume={
                        "action": "revise",
                        "feedback": feedback ## feedback is not empty anymore 
                    }),
                    config=config ## again important for langgraph 
                )
 
                st.session_state.result = result ## again stores the recent value inside session_state
                st.rerun() ## same to display the recent result and change the value
            else:
                st.warning("Please enter your feedback.") ## if user has not given feedback and press request changes this will display

    elif result.get("final_blog"): ## if there is not interrupt then this will run
        st.subheader("Final Blog")
        st.markdown(result["final_blog"]) ## just markdown the final blog  

