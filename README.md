# Hi, I'm Badal Singh 👋

### Generative AI Developer | AI Agents | RAG | LangChain | LangGraph

🎓 B.Tech in Computer Science & Engineering (Data Science)  
💻 Building intelligent applications powered by Large Language Models  
🚀 Aspiring Generative AI Engineer | AI/ML Engineer

I'm a Computer Science graduate passionate about developing practical **Generative AI applications, autonomous AI agents, Retrieval-Augmented Generation (RAG) systems, and LLM-powered workflows**.

My focus is on moving beyond basic LLM prompts to building applications with **tool calling, vector databases, conversational memory, multi-agent orchestration, and human-in-the-loop interactions**.

This repository showcases my hands-on projects and continuous learning in Generative AI engineering.

---

## 🛠️ Technical Skills

| Category | Technologies |
|---|---|
| **Programming** | Python, SQL |
| **GenAI Frameworks** | LangChain, LangGraph |
| **LLMs & APIs** | Groq API, GPT-OSS, Google Gemini |
| **RAG & Embeddings** | Retrieval-Augmented Generation, Hugging Face, Qwen Embeddings |
| **Vector Databases** | ChromaDB, InMemoryVectorStore |
| **Databases** | SQLite, MySQL |
| **Application Development** | Streamlit, REST API Integration |
| **Developer Tools** | Git, GitHub, VS Code, Jupyter Notebook |
| **Core Concepts** | AI Agents, Tool Calling, Prompt Engineering, Human-in-the-Loop, Conversational Memory |

---

## 🚀 Featured Generative AI Projects

### 01. 🧠 AI Blog Writer — Multi-Agent System with Human Feedback

**Python | LangGraph | Groq | Streamlit | Human-in-the-Loop**

Developed a multi-agent blog generation system that coordinates specialized AI agents to research, write, and edit content while allowing human intervention at critical stages.

**Key Features**
- Multi-agent workflow with Researcher, Writer, and Editor nodes.
- Human approval and revision of research before content generation.
- Human review and feedback on generated drafts.
- LangGraph `StateGraph` orchestration and conditional routing.
- Workflow interruption and resumption using `interrupt()` and `Command`.
- Interactive Streamlit interface.

**Architecture**

`User Input → Researcher → Human Review → Writer → Human Review → Editor → Final Blog`

🔗 [View Source Code](https://github.com/bsingh-2004/GEN_AI/blob/main/apps/blog_generator_using_langgraph.py)

---

### 02. 📚 Agentic RAG — Intelligent Document Q&A Assistant

**Python | LangChain | LangGraph | Groq | Hugging Face | Streamlit**

Built an agentic Retrieval-Augmented Generation application that enables users to interact with multiple PDF documents through natural-language conversations.

**Key Features**
- Multi-PDF document processing and question answering.
- Document chunking using `RecursiveCharacterTextSplitter`.
- Semantic search using Qwen3-Embedding-0.6B.
- Top-k similarity retrieval through a custom retrieval tool.
- LLM-driven decisions on when to retrieve document context.
- Conversational memory using LangGraph checkpointing.
- Interactive Streamlit chat interface.

**Architecture**

`PDF Documents → Chunking → Embeddings → Vector Store → Agent → Retrieval Tool → LLM Response`

---

### 03. 🗄️ AI Task Management Agent — Natural Language to SQL

**Python | LangChain | LangGraph | Groq | SQLite | Streamlit**

Developed an LLM-powered task management assistant that translates natural-language instructions into SQL database operations.

**Key Features**
- Create, read, update, and delete tasks using natural language.
- SQL tool integration through LangChain's `SQLDatabaseToolkit`.
- SQLite database integration for persistent task storage.
- Agent-based tool selection and execution.
- Conversational interface built with Streamlit.
- Thread-based conversational memory.

**Example Interactions**

- "Add a task to complete my LangGraph project."
- "Show me all pending tasks."
- "Mark my Python assignment as completed."
- "Delete the completed tasks."

---

### 04. 📄 RAG-Based PDF Chatbot

**Python | LangChain | ChromaDB | Hugging Face | Groq | Streamlit**

Created a document question-answering application that uses Retrieval-Augmented Generation to produce responses based on uploaded PDF content.

**Key Features**
- PDF text extraction and document processing.
- Text chunking and vector embedding generation.
- ChromaDB vector storage and semantic retrieval.
- Context-aware answers using a Groq-hosted LLM.
- Streamlit-based user interface.

🔗 [View Source Code](https://github.com/bsingh-2004/GEN_AI/blob/main/apps/rag_based_pdf_qna_chatbot.py)

---

## 🧩 AI Engineering Concepts Implemented

- **Agentic AI:** LLM-driven agents that decide when to use tools.
- **Multi-Agent Systems:** Specialized agents working together through orchestrated workflows.
- **Retrieval-Augmented Generation:** Grounding LLM responses in external document context.
- **Human-in-the-Loop:** Human approval, feedback, and workflow resumption.
- **Tool Calling:** Integrating language models with retrieval and database tools.
- **Conversational Memory:** Maintaining state across interactions.
- **Semantic Search:** Embedding-based retrieval using vector stores.

---

## 📁 Repository Structure

```text
GEN_AI/
│
├── apps/
│   ├── blog_generator_using_langgraph.py
│   ├── rag_agent.py
│   ├── sql_agent.py
│   ├── rag_based_pdf_qna_chatbot.py
│   ├── qna_bot_with_groq_faster_than_chatgpt.py
│   └── ...
│
├── notebooks/
├── notebooks_cleaned/
├── notebooks_rag/
│
└── README.md
```

*Some projects and notebooks may be available on separate branches.*

---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/bsingh-2004/GEN_AI.git
cd GEN_AI
```

### 2. Create a virtual environment

```bash
python -m venv env
```

Activate it on Windows:

```bash
env\Scripts\activate
```

### 3. Install dependencies

Once the project's `requirements.txt` is available:

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Never commit API keys or `.env` files to GitHub.

### 5. Run the Blog Generator

```bash
streamlit run apps/blog_generator_using_langgraph.py
```

---

## 📈 Currently Exploring

- Advanced LangGraph agent orchestration
- Agentic RAG architectures
- LLM evaluation and optimization
- Machine Learning and Deep Learning fundamentals
- AI application deployment
- Production-ready GenAI workflows

---

## 🎯 Career Interests

I'm actively exploring entry-level opportunities in:

**Generative AI Engineering | AI Engineering | AI/ML Engineering | LLM Application Development**

I'm particularly interested in developing intelligent applications that combine **LLMs, retrieval systems, AI agents, and real-world tools**.

---

## 🤝 Connect With Me

**LinkedIn:** [Badal Singh](https://www.linkedin.com/in/badal-singh-b67826319/)

**GitHub:** [@bsingh-2004](https://github.com/bsingh-2004)

I'm open to discussing Generative AI projects, collaboration, and entry-level AI engineering opportunities.

---

⭐ **If you find this repository useful, consider giving it a star!**

*Building intelligent systems, one project at a time.*
