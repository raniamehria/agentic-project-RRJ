
import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# 🔧 Import your tools
from utils import (
    pdf_to_text,
    upload_document,
    read_document,
    answer_from_document,
    list_steps_dynamic,
)

# Load environment variables
if os.path.exists(".env"):
    load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# Initialize LLM
llm = ChatOpenAI(model_name="gpt-5", temperature=0.0)

UPLOAD_DIRECTORY = Path("./Project_Agentic/uploads")
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------
# 🚀 Streamlit UI
# ----------------------------------------------------------

st.set_page_config(page_title="AI Document Agent", layout="wide")
st.title("📄 AI Agent – Document Assistant")

page = st.sidebar.radio(
    "Navigation",
    ["Upload Document", "Read Document", "Ask Questions", "Explain a Process"],
)

# ----------------------------------------------------------
# 📤 Upload PDF + convert to text
# ----------------------------------------------------------
if page == "Upload Document":
    st.header("Upload a PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_file:
        pdf_path = UPLOAD_DIRECTORY / uploaded_file.name

        # Save PDF
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"Uploaded: {uploaded_file.name}")

        # Convert to text
        text_content = pdf_to_text(str(pdf_path))
        txt_path = pdf_path.with_suffix(".txt")

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text_content)

        st.success(f"Converted to text: {txt_path.name}")
        st.text_area("Extracted Text", text_content, height=300)

# ----------------------------------------------------------
# 📖 Read a document (.txt)
# ----------------------------------------------------------
elif page == "Read Document":
    st.header("Read a document")

    txt_files = [f for f in os.listdir(UPLOAD_DIRECTORY) if f.endswith(".txt")]

    if txt_files:
        file = st.selectbox("Choose a text document:", txt_files)

        start = st.number_input("Start line", min_value=0, value=0)
        end = st.number_input("End line (optional)", min_value=0, value=0)

        if st.button("Read"):
            content = read_document.invoke(
                {"file_name": file, "start": start, "end": end or None}
            )
            st.text_area("Document Content", content, height=400)
    else:
        st.warning("No text documents available. Upload a PDF first.")

# ----------------------------------------------------------
# ❓ Ask questions about a document
# ----------------------------------------------------------
elif page == "Ask Questions":
    st.header("Ask a question based on a document")

    txt_files = [f for f in os.listdir(UPLOAD_DIRECTORY) if f.endswith(".txt")]

    if txt_files:
        file = st.selectbox("Select document:", txt_files)
        user_question = st.text_input("Your question:")

        if st.button("Ask"):
            answer = answer_from_document.invoke(
                {"user_message": user_question, "file_name": file}
            )
            st.write("### Answer:")
            st.write(answer)
    else:
        st.warning("No text files available. Upload a PDF first.")

# ----------------------------------------------------------
# 🧩 Step-by-step instructions generator
# ----------------------------------------------------------
elif page == "Explain a Process":
    st.header("Generate step-by-step instructions")

    process = st.text_input("What process should I explain?")
    if st.button("Generate Steps"):
        response = list_steps_dynamic(process)
        st.write("### Steps:")
        st.write(response)
