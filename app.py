
import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# 🔧 Import your tools
from utils import (
    pdf_to_text,
    read_document,
    answer_from_document,
    list_steps_dynamic,
    situation,
    fill_template,
    text_to_pdf,
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
    ["Upload Document", "Display Document", "Ask Questions", "Explain a Process", "Analyze a Situation", "Fill the Template","Generate PDF from Filled Template",],
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
elif page == "Display Document":
    st.header("Display Document")

    # List all text files in the uploads folder
    txt_files = [f for f in os.listdir(UPLOAD_DIRECTORY) if f.endswith(".txt")]

    if txt_files:
        file = st.selectbox("Choose a text document:", txt_files)

        if st.button("Display"):
            content = read_document.invoke({"file_name": file})
            st.text_area("Document Content", content, height=600) 
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

    txt_files = [f for f in os.listdir(UPLOAD_DIRECTORY) if f.endswith(".txt")]

    if txt_files:
        file = st.selectbox("Select document:", txt_files)
        process = st.text_input("What process should I explain?")
    
        if st.button("Generate Steps"):
            response = list_steps_dynamic(process)
            st.write("### Steps:")
            st.write(response)
    else:
        st.warning("No text files available. Upload a PDF first.")


elif page == "Analyze a Situation":
    st.header("Generate a situation analysis")

    txt_files = [f for f in os.listdir(UPLOAD_DIRECTORY) if f.endswith(".txt")]

    if txt_files:
        file = st.selectbox("Select document:", txt_files)
        situation = st.text_input("What is your situation")

        if st.button("Analyze"):
            response = list_steps_dynamic(situation)
            st.write("### Analysis:")
            st.write(response)
    else:
        st.warning("No text files available. Upload a PDF first.")

# elif page == "Explain the Procedures":
#     st.header("Generate all of the procedures of this administration process")

#     txt_files = [f for f in os.listdir(UPLOAD_DIRECTORY) if f.endswith(".txt")]

#     if txt_files:
#         process_name = st.text_input("What is your situation")
#         if st.button("Procedures"):
#             response = list_steps_dynamic(process_name)
#             st.write("### Procedures:")
#             st.write(response)

#     else:
#         st.warning("No text files available. Upload a PDF first.")

# ====TEST====
elif page == "Fill the Template":
    st.header("Generate what to fill in the blanks")

    txt_files = [f for f in os.listdir(UPLOAD_DIRECTORY) if f.endswith(".txt")]

    if txt_files:
        file = st.selectbox("Select a template file:", txt_files)

        template_path = UPLOAD_DIRECTORY / file
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()

        st.subheader("Template Preview")
        st.text_area("Template content", template, height=200)

        # Detect fields
        lines = template.splitlines()
        fields = [line.split(":")[0].strip() for line in lines if ":" in line]

        if fields:
            st.subheader("Fill in the fields")
            user_inputs = {}
            for i, field in enumerate(fields):
                user_inputs[field] = st.text_input(f"{field}:", key=f"{field}_{i}")

            if st.button("Generate Filled Template"):
                # Replace each field's dots with user input
                filled_lines = []
                for line in lines:
                    if ":" in line:
                        key = line.split(":")[0].strip()
                        value = user_inputs.get(key, "")
                        filled_lines.append(f"{key}: {value}")
                    else:
                        filled_lines.append(line)

                filled_template = "\n".join(filled_lines)

                # Optional: polish with LLM
                prompt = f"Polish this template while keeping the values:\n\n{filled_template}"
                messages = [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
                polished = llm.invoke(messages).content

                # Save polished text to a file
                filled_txt_path = UPLOAD_DIRECTORY / "filled_template.txt"
                with open(filled_txt_path, "w", encoding="utf-8") as f:
                    f.write(polished.strip())

                st.success("Template filled and saved as filled_template.txt")
                st.text_area("Filled Template", polished, height=400)
        else:
            st.info("No fields detected in the template.")
    else:
        st.warning("No text templates available. Upload a template first.")

elif page == "Generate PDF from Filled Template":
    st.header("Convert a filled template TXT to PDF")

    # List all filled .txt files
    filled_txt_files = [f for f in os.listdir(UPLOAD_DIRECTORY) if f.endswith(".txt") and "filled" in f]

    if filled_txt_files:
        file = st.selectbox("Select a filled template:", filled_txt_files)

        output_name = file.replace(".txt", "")

        if st.button("Generate PDF"):
            # Convert to PDF
            pdf_path = text_to_pdf.invoke({
                "txt_file_path": str(UPLOAD_DIRECTORY / file),
                "output_name": output_name
            })

            st.success(f"PDF generated: {output_name}.pdf")

            # Provide download button
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()

            st.download_button(
                "Download PDF",
                data=pdf_bytes,
                file_name=f"{output_name}.pdf",
                mime="application/pdf"
            )
    else:
        st.warning("No filled templates found. Fill a template first.")
