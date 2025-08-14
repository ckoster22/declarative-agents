"""
Custom tools for saving research reports to the reports directory.
"""

import re
from pathlib import Path
import logging
from datetime import datetime
import markdown
from weasyprint import HTML

logger = logging.getLogger(__name__)

def save_report_to_file(filename: str, content: str, report_type: str = "markdown") -> str:
    """
    Save a research report to the reports directory.
    
    Args:
        filename: The filename for the report (will be sanitized)
        content: The content to write to the file
        report_type: Type of report (markdown, pdf, etc.)
    
    Returns:
        Success message with file path
    """
    # Ensure reports directory exists
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    # Sanitize filename - remove/replace unsafe characters
    safe_filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    safe_filename = re.sub(r'\s+', '_', safe_filename)  # Replace spaces with underscores
    safe_filename = safe_filename.strip('.')  # Remove leading/trailing dots
    
    # Ensure proper extension
    if report_type == "markdown" and not safe_filename.endswith('.md'):
        safe_filename += ".md"
    elif report_type != "markdown" and not safe_filename.endswith(f'.{report_type}'):
        safe_filename += f".{report_type}"
    
    file_path = reports_dir / safe_filename
    
    # Write the content to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    absolute_path = file_path.absolute()
    logger.info(f"Successfully saved report to: {absolute_path}")
    
    return f"Successfully saved report to: {absolute_path}"


def create_timestamped_filename(topic: str, extension: str = "md") -> str:
    """
    Create a timestamped filename based on the research topic.
    
    Args:
        topic: The research topic
        extension: File extension (default: md)
    
    Returns:
        Formatted filename with timestamp
    """
    # Clean up topic for filename
    topic_clean = re.sub(r'[<>:"/\\|?*\.]', '', topic)
    topic_clean = re.sub(r'\s+', '_', topic_clean)
    topic_clean = topic_clean[:50]  # Limit length
    
    # Get timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    return f"report_{topic_clean}_{timestamp}.{extension}"


def get_reports_directory_info() -> str:
    """
    Get information about the reports directory and existing files.
    
    Returns:
        Information about the reports directory
    """
    reports_dir = Path("reports")
    if not reports_dir.exists():
        return "Reports directory does not exist yet. It will be created when the first report is saved."
    
    files = [f.name for f in reports_dir.iterdir() if f.is_file()]
    file_count = len(files)
    
    abs_path = reports_dir.absolute()
    
    if files:
        file_list = "\n  ".join(files)
        return f"Reports directory: {abs_path}\nFiles ({file_count}):\n  {file_list}"
    else:
        return f"Reports directory: {abs_path}\nNo files found."


def save_report_as_pdf(filename: str, markdown_content: str) -> str:
    """
    Convert markdown content to PDF and save to reports directory.
    
    Args:
        filename: The filename for the PDF (will be sanitized)
        markdown_content: The markdown content to convert
    
    Returns:
        Success message with file path or error if PDF generation unavailable
    """
    # Ensure reports directory exists
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    # Sanitize filename
    safe_filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    safe_filename = re.sub(r'\s+', '_', safe_filename)
    safe_filename = safe_filename.strip('.')
    
    if not safe_filename.endswith('.pdf'):
        safe_filename += '.pdf'
    
    file_path = reports_dir / safe_filename
    
    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_content, extensions=['tables', 'fenced_code'])
    
    # Add basic CSS styling for better PDF appearance
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{ size: A4; margin: 0.75in; }}
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            h1, h2, h3 {{ color: #333; }}
            h1 {{ border-bottom: 2px solid #333; padding-bottom: 10px; }}
            h2 {{ border-bottom: 1px solid #ccc; padding-bottom: 5px; }}
            code {{ background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px; }}
            pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Convert HTML to PDF using WeasyPrint
    HTML(string=styled_html).write_pdf(str(file_path))
    
    absolute_path = file_path.absolute()
    logger.info(f"Successfully saved PDF report to: {absolute_path}")
    
    return f"Successfully saved PDF report to: {absolute_path}"

def save_report_both_formats(topic: str, markdown_content: str) -> str:
    """
    Save a report in both markdown and PDF formats.
    
    Args:
        topic: The research topic for filename generation
        markdown_content: The markdown content to save
    
    Returns:
        Status message for both saves
    """
    # Create timestamped filename
    md_filename = create_timestamped_filename(topic, "md")
    pdf_filename = create_timestamped_filename(topic, "pdf")
    
    # Save markdown
    md_result = save_report_to_file(md_filename, markdown_content, "markdown")
    
    # Save PDF
    pdf_result = save_report_as_pdf(pdf_filename, markdown_content)
    
    return f"Markdown: {md_result}\nPDF: {pdf_result}"
