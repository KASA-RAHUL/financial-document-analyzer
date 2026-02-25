# 📈 Financial Document Analyzer - Pro Edition

## Project Overview
A highly professional, AI-powered system that analyzes financial documents (like Q-reports and 10-Ks). It processes files using an intelligent Multi-Agent architecture (CrewAI) to verify, analyze, calculate risks, and generate data-driven investment recommendations.

## 🐛 Bugs Squashed & Fixes Implemented

### 1. Deterministic/Code Bugs Fixed
* **Undefined LLM (`agents.py`)**: The code crashed instantly because `llm = llm` wasn't pointing to any actual language model. Fixed by implementing `ChatOpenAI` through LangChain.
* **Missing Tool Imports & PDF Extraction (`tools.py`)**: `Pdf().load()` referenced a non-existent class. Refactored `read_data_tool` using the `crewai @tool` decorator and `PyPDF2` to read files robustly.
* **Unutilized Agents & Tasks (`main.py` & `task.py`)**: The original script created 4 tasks and 4 agents but only passed `financial_analyst` to the Crew. Fixed to sequentially pipeline: **Verification → Analysis → Risk → Investment**.
* **Hardcoded Paths (`tools.py` & `main.py`)**: The PDF path was hardcoded inside the tool definition causing concurrency crashes and logic loops. Dynamic `{file_path}` variables are now correctly passed into CrewAI's `kickoff(inputs=...)` method.
* **Premature File Deletion (`main.py`)**: Hardcoded immediate file deletion meant async processing would fail before reading. Cleanups are now tied to task completion safely.

### 2. Prompt Engineering Fixes
* **Hallucination Prompts**: The original AI personas were instructed to "make up facts", "give bad advice", and "ignore risks."
* **Fix**: Completely rewrote Agent Personas (Roles, Backstories, Goals) and Task Descriptions. The AI now acts as a fiduciary advisory team that strictly extracts actual numbers from the uploaded PDFs to make logical deductions. 

### 🌟 Bonus Points Achieved!
1. **Queue Worker Model Implementation**: Refactored `main.py` to utilize FastAPI's `BackgroundTasks`. The `/analyze` endpoint now returns a `job_id` instantly while processing happens sequentially in the background—preventing server timeout limits!
2. **Database Integration**: Added `database.py` with SQLite to track application state. Users can now poll `/status/{job_id}` to retrieve asynchronous results or check if their job is pending, complete, or failed.

### 🔐 API Keys & Security
This project integrates external LLM and search APIs.  
For security reasons, API keys are **not included** in this repository.

To run locally, create a `.env` file using the variables shown in `.env.example`.

---

## 🚀 Getting Started

### 1. Installation
Ensure Python 3.10+ is installed.
```sh
pip install -r requirements.txt