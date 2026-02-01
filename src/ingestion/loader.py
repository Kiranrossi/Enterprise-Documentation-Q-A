"""Document loader for multiple file formats."""

from pathlib import Path
from typing import List, Dict, Optional
import PyPDF2
import docx
import markdown
from bs4 import BeautifulSoup

from ..utils import log


class DocumentLoader:
    """Load documents from various file formats."""
    
    SUPPORTED_FORMATS = {'.pdf', '.txt', '.md', '.docx', '.html'}
    
    def __init__(self):
        """Initialize the document loader."""
        self.documents = []
    
    def load_file(self, file_path: Path) -> Optional[Dict[str, str]]:
        """
        Load a single file and extract text.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with metadata and text content
        """
        if not file_path.exists():
            log.error(f"File not found: {file_path}")
            return None
        
        suffix = file_path.suffix.lower()
        
        if suffix not in self.SUPPORTED_FORMATS:
            log.warning(f"Unsupported file format: {suffix}")
            return None
        
        try:
            if suffix == '.pdf':
                text = self._load_pdf(file_path)
            elif suffix == '.txt':
                text = self._load_txt(file_path)
            elif suffix == '.md':
                text = self._load_markdown(file_path)
            elif suffix == '.docx':
                text = self._load_docx(file_path)
            elif suffix == '.html':
                text = self._load_html(file_path)
            else:
                return None
            
            if text:
                log.info(f"Loaded {file_path.name}: {len(text)} characters")
                return {
                    "source": str(file_path),
                    "filename": file_path.name,
                    "format": suffix,
                    "text": text
                }
            else:
                log.warning(f"No text extracted from {file_path.name}")
                return None
                
        except Exception as e:
            log.error(f"Error loading {file_path.name}: {e}")
            return None
    
    def _load_pdf(self, file_path: Path) -> str:
        """Load PDF file."""
        text = []
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
        return "\n\n".join(text)
    
    def _load_txt(self, file_path: Path) -> str:
        """Load text file."""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            return file.read()
    
    def _load_markdown(self, file_path: Path) -> str:
        """Load Markdown file and convert to plain text."""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            md_content = file.read()
        
        # Convert markdown to HTML then to plain text
        html = markdown.markdown(md_content)
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text()
    
    def _load_docx(self, file_path: Path) -> str:
        """Load DOCX file."""
        doc = docx.Document(file_path)
        text = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text.append(paragraph.text)
        return "\n\n".join(text)
    
    def _load_html(self, file_path: Path) -> str:
        """Load HTML file."""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            html_content = file.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        return soup.get_text()
    
    def load_directory(self, directory: Path, recursive: bool = True) -> List[Dict[str, str]]:
        """
        Load all supported documents from a directory.
        
        Args:
            directory: Path to directory
            recursive: Whether to search subdirectories
            
        Returns:
            List of document dictionaries
        """
        documents = []
        
        if not directory.exists():
            log.error(f"Directory not found: {directory}")
            return documents
        
        pattern = "**/*" if recursive else "*"
        
        for file_path in directory.glob(pattern):
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_FORMATS:
                doc = self.load_file(file_path)
                if doc:
                    documents.append(doc)
        
        log.info(f"Loaded {len(documents)} documents from {directory}")
        return documents
