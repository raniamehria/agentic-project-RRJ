import re
import io
import requests
from langchain_core.tools import tool
from typing import Annotated, Sequence, TypedDict, Optional

@tool
def read_document(
    file_name: Annotated[str, "File path to read the document from."],
    start: Annotated[Optional[int], "The start line. Default is 0"] = None,
    end: Annotated[Optional[int], "The end line. Default is None"] = None,
) -> str:
    """Read the specified document."""
    with (WORKING_DIRECTORY / file_name).open("r") as file:
        lines = file.readlines()
    if start is None:
        start = 0
    return "\n".join(lines[start:end])

from typing import Annotated, Optional
import shutil

from pathlib import Path

UPLOAD_DIRECTORY = Path("./Project_Agentic/") / "uploads"
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

@tool
def upload_document(
    source_path: Annotated[str, "Local file path to upload."],
    destination_name: Annotated[Optional[str], "Name to save the file as."] = None,
) -> str:
    """Upload a document into the working directory."""
    destination_name = destination_name or source_path.split("/")[-1]
    destination_path = UPLOAD_DIRECTORY / destination_name
    shutil.copy(source_path, destination_path)
    return f"File uploaded successfully as {destination_name}"
