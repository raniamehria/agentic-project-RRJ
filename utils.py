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
import fpdf
from fpdf import FPDF

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

def explain_procedures(process_name: str) -> str:
    """
    Uses the LLM to generate the steps to a procedure
    for any user input process or task.
    """
    prompt = f"Provide clear, easy to understand steps for the administrative procedure:\n'{process_name}'"
    
    # Call the LLM
    messages = [
        {"role": "system", "content": "You provide clear, not too long, practical, step-by-step for the administrative procedure."},
        {"role": "user", "content": prompt}
    ]
    response = llm_client.invoke(messages)
    return response.content

@tool
def procedure(process_name: str) -> str:
    """
    list the steps of the administrative procedure
    """
    return explain_procedures(process_name)


def analyze_situation(user_situation : str) -> str:
    """
    According to the information provided by the user, 
    you must analyze and summarize their situation 
    and provide a soltion in a short paragraph
    """
    prompt = f"I would like to know what should I do if this is my situation:\n'{analyze_situation}'"
    # Call the LLM
    messages = [
        {"role": "system", "content": "You provide an explaination of my situation and clear, practical soluton summary."},
        {"role": "user", "content": prompt}
    ]
    response = llm_client.invoke(messages)
    return response.content

@tool
def situation(user_situation : str) -> str: 
    """
    Give a summary of the situation of the user then provide a solution
    """
    return analyze_situation(user_situation)

   

# ====TEST====
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import re

# Assuming you already have llm_client defined
# llm_client = ChatOpenAI(model_name="gpt-5", temperature=0.0)

def fill_template_interactive(template: str, user_inputs: dict, output_name: str) -> str:
    """
    Fill a template, polish it with the LLM, save it as TXT, and return file path.
    """
    # Build filled text
    lines = template.splitlines()
    filled_lines = []

    for line in lines:
        if ":" in line:
            key = line.split(":")[0].strip()
            value = user_inputs.get(key, "")
            filled_lines.append(f"{key}: {value}")
        else:
            filled_lines.append(line)

    raw_filled = "\n".join(filled_lines)

    # Polish with LLM
    prompt = f"Polish this template while keeping the values:\n\n{raw_filled}"
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    polished = llm_client.invoke(messages).content

    # Save polished template as TXT
    txt_path = UPLOAD_DIRECTORY / f"{output_name}.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(polished)

    return fill_template_interactive(template, user_inputs, output_name)


@tool
def fill_template(template: str, user_inputs: dict, output_name: str) -> str:
    """
    Fill a template and save it as a TXT file.
    Returns the path to the generated TXT file.
    """
    return fill_template_interactive(template, user_inputs, output_name)


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from pathlib import Path

PDF_DIRECTORY = Path("./Project_Agentic/pdfs")
PDF_DIRECTORY.mkdir(parents=True, exist_ok=True)

def text_to_pdf_dynamic(txt_file_path: str, output_name: str) -> str:
    pdf_path = PDF_DIRECTORY / f"{output_name}.pdf"

    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    width, height = A4
    y = height - 40  # Start near top
    line_height = 14

    with open(txt_file_path, "r", encoding="utf-8") as f:
        for line in f:
            if y < 40:  # Start a new page
                c.showPage()
                y = height - 40
            c.drawString(40, y, line.strip())
            y -= line_height

    c.save()
    return str(pdf_path)


@tool
def text_to_pdf(txt_file_path: str, output_name: str) -> str:
    """
    Convert a TXT file to a PDF.
    """
    return text_to_pdf_dynamic(txt_file_path, output_name)
