import re
import io
import requests
from langchain_core.tools import tool
from typing import Annotated, Sequence, TypedDict, Optional
import PyPDF2
import shutil
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv

# Load environment variables from .env file
if os.path.exists(".env"):
    load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm_client = ChatOpenAI (model_name = "gpt-5", temperature= 0.0)
# Create a path where the doc will be loaded from 
UPLOAD_DIRECTORY = Path("./Project_Agentic/") / "uploads"
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

# Convert .pdf to .txt
def pdf_to_text(pdf_path: str) -> str:
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# define tools
@tool
def upload_document(source_path: str, destination_name: str = None) -> str:
    """
    upload the document 
    """
    destination_name = destination_name or Path(source_path).name
    destination_path = UPLOAD_DIRECTORY / destination_name
    shutil.copy(source_path, destination_path)
    return f"File uploaded successfully as {destination_name}"

@tool
def read_document(file_name: str, start: int = None, end: int = None) -> str:
    """
    Read the document 
    """
    with (UPLOAD_DIRECTORY / file_name).open("r", encoding="utf-8") as f:
        lines = f.readlines()
    start = start or 0
    return "\n".join(lines[start:end])

@tool
def answer_from_document(user_message: str, file_name: str) -> str:
    """
    generate an answer with information given from the document 
    """
    
    document_content = read_document.invoke({"file_name": file_name})
    messages = [
        {"role": "system", "content": "You answer questions based only on the provided document."},
        {"role": "user", "content": f"Document content:\n{document_content}"},
        {"role": "user", "content": f"Question: {user_message}"}
    ]
    response = llm_client.invoke(messages)
    return response.content

def list_steps_dynamic(process_name: str) -> str:
    """
    Uses the LLM to generate step-by-step instructions
    for any user input process or task.
    """
    prompt = f"Provide clear, step-by-step instructions to complete the following process:\n'{process_name}'"
    
    # Call the LLM
    messages = [
        {"role": "system", "content": "You provide clear, practical, step-by-step instructions."},
        {"role": "user", "content": prompt}
    ]
    response = llm_client.invoke(messages)
    return response.content

@tool
def list_steps(process_name: str) -> str:
    """
    list all of the steps needed
    """
    return list_steps_dynamic(process_name)

all_tools = [pdf_to_text, read_document, upload_document, answer_from_document,  list_steps_dynamic, list_steps]