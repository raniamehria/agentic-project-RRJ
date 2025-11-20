# 1. Project Title  
## Agentic System – Intelligent Document Assistant

---

# 2. Executive Summary

Agentic System is an AI-driven assistant designed to help users understand and process complex documents more efficiently.  
Using LangChain and LangGraph, the system automates multi-step reasoning tasks such as extracting information, summarising content, answering questions, and generating procedural guidance.  
The Streamlit interface makes the tool simple to use for anyone needing support with administrative or technical documents.

---

# 3. Problem Statement

Users often struggle with long, complex, or technical documents, especially in administrative and academic contexts. These documents require time to read, contain dense information, and may lead to misunderstandings or missed requirements.

Common difficulties include:
- Time-consuming manual reading  
- Lack of clarity in official language  
- Risk of missing important instructions  
- Repetitive document interpretation  
- Limited tools offering structured guidance  

Agentic System addresses these challenges by automating document analysis and providing clear, actionable assistance.

# 4. Proposed Solution & Value Proposition

Agentic System provides an AI-powered workflow that automates the understanding and processing of complex documents. Instead of manually reading and interpreting content, users interact with an agent capable of structured reasoning and tool-based actions.

### Key elements of the solution:
- Automated extraction and interpretation of document content  
- Step-by-step guidance for administrative or procedural tasks  
- Question–answering based on document context  
- Structured reasoning enabled by LangGraph (rather than simple free-form generation)  
- Simple and accessible interface through Streamlit  

### Value Proposition
Agentic System reduces time spent on document reading, prevents misunderstandings, and provides clear actionable guidance. It transforms complex documents into concise, usable information and supports users through tasks that would otherwise be repetitive, slow, or difficult to interpret.
# 5. Functional Overview

Agentic System provides a simple and efficient workflow that allows users to interact with documents through an intelligent agent.  
The main functionalities available through the Streamlit interface are:

### • Document upload
Users can upload a PDF or text document for analysis.

### • Automatic document processing
The system extracts and interprets the key elements of the uploaded document.

### • Question answering
Users can ask questions directly related to the document’s content and receive precise, context-aware answers.

### • Step-by-step guidance
The agent generates clear procedural steps based on the document, helping users navigate administrative or informational tasks.

### • Agentic reasoning workflow
The system relies on a LangGraph-based workflow that ensures structured reasoning, tool execution, and controlled decision making.

Overall, the interface provides an accessible entry point to advanced agentic capabilities without requiring technical expertise from the user.

# 6. Technical Architecture

Agentic System is structured around four main layers:  
(1) the user interface,  
(2) the agent logic,  
(3) the tools,  
(4) the underlying LLM.

The architecture is organised as follows:

### 6.1 Streamlit Interface (Frontend)
The Streamlit application (`app.py`) provides the entry point for the user.  
Its responsibilities include:
- Uploading documents  
- Sending user queries to the agent  
- Displaying the extracted information, answers, and step-by-step guidance  

### 6.2 Agent Logic (LangGraph)
The core logic of the system is implemented using LangGraph.  
The agent follows a structured workflow composed of:
- **State management:** tracking messages, tool inputs, and intermediate results  
- **Node transitions:** determining the next step in the reasoning cycle  
- **LLM decisions:** prompting the model to select an appropriate action  
- **Tool invocation:** executing utilities when required  

This graph-based structure ensures deterministic, step-by-step reasoning rather than uncontrolled free generation.

### 6.3 Tools Layer (`utils.py`)
Custom tools are implemented to extend the agent’s capabilities.  
These may include:
- PDF text extraction  
- Utility functions for text processing  
- External resource calls (if needed)

The agent can call these tools when the reasoning process determines that tool execution is required.

### 6.4 LLM Backend (OpenAI API)
The language model provides the reasoning engine used in:
- Document interpretation  
- Answer generation  
- Action selection within the agentic workflow  

The API key is loaded using environment variables defined in the `.env` file.

### 6.5 Data Flow Overview
1. The user uploads a document through Streamlit.  
2. The document is processed and passed to the agent.  
3. The agent enters the LangGraph reasoning loop.  
4. Depending on the task, the agent may call a tool, request more context, or produce final output.  
5. Results are displayed in the Streamlit interface.

This architecture separates concerns clearly and enables a robust, maintainable agentic workflow.

# 7. Repository Structure

The repository is organised to separate the user interface, agent logic, utility functions, and environment configuration.  
This structure allows the examiner to understand the project quickly and run the system without difficulty.
Each component is isolated to ensure modularity:

- The **Streamlit interface** is independent of the agent logic.  
- The **agent logic** (LangChain + LangGraph) and **tools** are grouped into dedicated files for clarity.  
- The **requirements** file ensures easy installation.  
- The **notebook** documents development and supports evaluation during the pitch.
  

# 8. Technologies Used

The project relies on a combination of modern AI frameworks, agentic workflow libraries, and lightweight frontend tools.  
Each technology was selected to support structured reasoning, tool execution, and an accessible user interface.

### • Python  
### • LangChain  
### • LangGraph  
### • OpenAI API  
### • Streamlit  
### • PyPDF2  
### • python-dotenv  
### • Additional standard libraries  


# 9. Installation Guide

This section provides the complete setup instructions required to run the project.  
Follow each step carefully to ensure the environment is correctly configured.

---

## 9.1. Clone the Repository

```bash
git clone <repository_url>
cd <repository_folder>
````

---

## 9.2. Create and Activate a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate    # MacOS / Linux
.\.venv\Scripts\activate     # Windows
```

---

## 9.3. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

---

## 9.4. Set Up Environment Variables

Create a `.env` file in the project root and add your OpenAI API key

---

## 9.5. Launch the Streamlit Application

Run the main interface:

```bash
streamlit run app.py
```

This opens the application in your browser, allowing you to upload a document and interact with the agent.

---

## 9.6.  Run the Notebook

If you want to explore the prototype or development steps:

```bash
jupyter notebook
```

Open `project.ipynb` and execute the cells.

---

Here is a **more concise and professional** version of **Section 11 – Usage Guide**, formatted in Markdown and ready to paste into GitHub.

---

# 10. Usage Guide

This section explains how to interact with the system once it is running.

---

## 10.1. Start the Application

```bash
streamlit run app.py
````

Streamlit will open the interface in your browser.

---

## 10.2. Upload a Document

Use the upload area to submit a PDF or text file.
The system automatically extracts and prepares the content for analysis.

---

## 10.3. Ask Questions

Enter any question related to the document, such as:

* “What is this document about?”
* “What steps do I need to follow?”

The agent answers based on the extracted content.

---

## 10.4. Generate Guidance

The system can produce short summaries or step-by-step instructions derived from the document.

---

## 10.5. Reset or Upload a New Document

You may upload a new file at any time; the agent processes each document independently.

# 12. Limitations

Despite its capabilities, the system has several limitations:

- The quality of results depends on the clarity and structure of the uploaded document.  
- Complex PDFs (tables, scanned pages, images) may not be fully extracted by the current tools.  
- The agent relies on an external LLM (OpenAI API), which requires internet access and a valid API key.  
- The system does not store long-term memory between sessions.  
- Reasoning quality may vary depending on the model used and the document complexity.  
- The Streamlit interface is minimal and not yet optimized for large-scale use.

# 13. Conclusion

Agentic System demonstrates how agentic workflows can be applied to real-world document processing challenges.  
By combining LangChain, LangGraph, Streamlit, and custom tools, the project delivers a functional AI assistant capable of analysing documents, extracting information, answering questions, and providing actionable guidance.

The system offers a clear illustration of structured multi-step reasoning and serves as a foundation for more advanced agentic applications.  
Its modular architecture makes it easy to extend with new tools, improved document extraction, and richer user interfaces in the future.

# Authors

This project was developed by:

- **Julia Randriatsimivony**  
- **Rania Mehria**  
- **Ryme Belouahri**

  ALBERT SCHOOL 2025







