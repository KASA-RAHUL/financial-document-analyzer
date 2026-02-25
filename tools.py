import os
import PyPDF2
from dotenv import load_dotenv
from crewai.tools import tool
from crewai_tools import SerperDevTool

load_dotenv()

# Search tool is fine as is, assuming SERPER_API_KEY is in .env
search_tool = SerperDevTool()

@tool("Read Financial Document")
def read_data_tool(file_path: str) -> str:
    """
    Reads text data from a PDF financial document. 
    You MUST pass the exact 'file_path' variable to this tool.
    """
    try:
        full_report = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    # Clean and format
                    text = text.replace("\n\n", "\n")
                    full_report += text + "\n"
        return full_report
    except Exception as e:
        return f"Error reading PDF from {file_path}: {str(e)}"