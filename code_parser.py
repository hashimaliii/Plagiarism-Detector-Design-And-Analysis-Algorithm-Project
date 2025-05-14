import re
from typing import List, Dict, Optional
import os
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CodeParser:
    def __init__(self):
        # Common programming language keywords to preserve
        self.keywords = {
            # Python
            'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue',
            'return', 'try', 'catch', 'finally', 'throw', 'throws', 'class', 'interface',
            'extends', 'implements', 'public', 'private', 'protected', 'static', 'final',
            'void', 'int', 'float', 'double', 'boolean', 'char', 'string', 'null', 'true', 'false',
            # Java
            'package', 'import', 'extends', 'implements', 'interface', 'abstract', 'synchronized',
            'volatile', 'transient', 'native', 'strictfp',
            # C/C++
            'include', 'define', 'typedef', 'struct', 'union', 'enum', 'extern', 'auto',
            'register', 'const', 'inline', 'virtual', 'explicit', 'friend', 'namespace',
            # JavaScript
            'let', 'const', 'var', 'function', 'async', 'await', 'export', 'import',
            'default', 'extends', 'implements', 'interface', 'type', 'enum'
        }
        
        # Language-specific comment patterns
        self.comment_patterns = {
            '.py': {
                'single_line': r'#.*?$',
                'multi_line': r'""".*?"""|\'\'\'.*?\'\'\''
            },
            '.java': {
                'single_line': r'//.*?$',
                'multi_line': r'/\*.*?\*/'
            },
            '.cpp': {
                'single_line': r'//.*?$',
                'multi_line': r'/\*.*?\*/'
            },
            '.c': {
                'single_line': r'//.*?$',
                'multi_line': r'/\*.*?\*/'
            },
            '.h': {
                'single_line': r'//.*?$',
                'multi_line': r'/\*.*?\*/'
            },
            '.js': {
                'single_line': r'//.*?$',
                'multi_line': r'/\*.*?\*/'
            },
            '.ts': {
                'single_line': r'//.*?$',
                'multi_line': r'/\*.*?\*/'
            },
            '.rb': {
                'single_line': r'#.*?$',
                'multi_line': r'=begin.*?=end'
            }
        }
        
        # Language-specific token patterns
        self.token_patterns = {
            '.py': r'\b\w+\b|[^\w\s]',
            '.java': r'\b\w+\b|[^\w\s]',
            '.cpp': r'\b\w+\b|[^\w\s]',
            '.c': r'\b\w+\b|[^\w\s]',
            '.h': r'\b\w+\b|[^\w\s]',
            '.js': r'\b\w+\b|[^\w\s]',
            '.ts': r'\b\w+\b|[^\w\s]',
            '.rb': r'\b\w+\b|[^\w\s]'
        }
    
    def parse_file(self, file_path: str) -> Optional[List[str]]:
        """
        Parse a code file and return a list of tokens.
        Handles comments, whitespace, and preserves important keywords.
        """
        try:
            # Validate file exists and is readable
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return None
            
            if not os.access(file_path, os.R_OK):
                logger.error(f"File not readable: {file_path}")
                return None
            
            # Get file extension
            ext = os.path.splitext(file_path)[1].lower()
            if ext not in self.comment_patterns:
                logger.warning(f"Unsupported file type: {ext}")
                return None
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove comments based on file type
            content = self._remove_comments(content, ext)
            
            # Tokenize the code
            tokens = self._tokenize(content, ext)
            
            return tokens
            
        except Exception as e:
            logger.error(f"Error parsing file {file_path}: {str(e)}")
            return None
    
    def _remove_comments(self, content: str, file_ext: str) -> str:
        """Remove both single-line and multi-line comments based on file type."""
        patterns = self.comment_patterns[file_ext]
        
        # Remove multi-line comments
        content = re.sub(patterns['multi_line'], '', content, flags=re.DOTALL)
        # Remove single-line comments
        content = re.sub(patterns['single_line'], '', content, flags=re.MULTILINE)
        return content
    
    def _tokenize(self, content: str, file_ext: str) -> List[str]:
        """Convert code into a list of tokens based on file type."""
        pattern = self.token_patterns[file_ext]
        tokens = re.findall(pattern, content)
        
        # Filter out empty tokens and normalize
        tokens = [t.lower() for t in tokens if t.strip()]
        
        return tokens
    
    def get_metadata(self, file_path: str) -> Dict:
        """Extract metadata from the file path."""
        try:
            file_stat = os.stat(file_path)
            return {
                'file_name': os.path.basename(file_path),
                'file_path': file_path,
                'file_size': file_stat.st_size,
                'created_time': datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                'modified_time': datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                'language': self._detect_language(file_path)
            }
        except Exception as e:
            logger.error(f"Error getting metadata for {file_path}: {str(e)}")
            return {
                'file_name': os.path.basename(file_path),
                'file_path': file_path,
                'error': str(e)
            }
    
    def _detect_language(self, file_path: str) -> str:
        """Detect programming language based on file extension."""
        ext = os.path.splitext(file_path)[1].lower()
        language_map = {
            '.py': 'Python',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.h': 'C/C++ Header',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.rb': 'Ruby'
        }
        return language_map.get(ext, 'Unknown') 