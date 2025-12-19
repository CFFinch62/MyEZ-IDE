"""
EZ Language Syntax Highlighter
Provides syntax highlighting for the EZ programming language
"""

from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from typing import Dict, List, Tuple

from app.themes import Theme, SyntaxColors


# EZ Language keywords (from tokenizer)
EZ_KEYWORDS = [
    'temp', 'const', 'do', 'return', 'if', 'or', 'otherwise',
    'for', 'for_each', 'as_long_as', 'loop', 'break', 'continue',
    'in', 'not_in', 'range', 'import', 'using', 'struct', 'enum',
    'nil', 'new', 'true', 'false', 'module', 'private', 'use',
    'when', 'is', 'default', 'cast'
]

# EZ Built-in types
EZ_TYPES = [
    'int', 'float', 'string', 'bool', 'char', 'void', 'any'
]

# EZ Built-in functions (common ones from stdlib)
EZ_BUILTINS = [
    'println', 'print', 'input', 'len', 'append', 'remove',
    'contains', 'keys', 'values', 'type_of', 'to_string',
    'to_int', 'to_float', 'abs', 'min', 'max', 'floor', 'ceil',
    'round', 'sqrt', 'pow', 'sin', 'cos', 'tan', 'log', 'exp',
    'random', 'seed', 'time', 'sleep', 'format', 'split', 'join',
    'trim', 'upper', 'lower', 'replace', 'starts_with', 'ends_with',
    'substring', 'index_of', 'last_index_of', 'char_at', 'parse_int',
    'parse_float', 'read_file', 'write_file', 'file_exists'
]


class EZHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for the EZ programming language"""
    
    def __init__(self, parent=None, theme: Theme = None):
        super().__init__(parent)
        self.theme = theme
        self._formats: Dict[str, QTextCharFormat] = {}
        self._rules: List[Tuple[QRegularExpression, str]] = []
        
        self._setup_formats()
        self._setup_rules()
    
    def set_theme(self, theme: Theme):
        """Update the theme and recreate formats"""
        self.theme = theme
        self._setup_formats()
        self.rehighlight()
    
    def _setup_formats(self):
        """Set up text formats based on theme colors"""
        if self.theme is None:
            from app.themes import DARK_THEME
            self.theme = DARK_THEME
        
        colors = self.theme.syntax
        
        # Keyword format
        keyword_fmt = QTextCharFormat()
        keyword_fmt.setForeground(QColor(colors.keyword))
        keyword_fmt.setFontWeight(QFont.Weight.Bold)
        self._formats['keyword'] = keyword_fmt
        
        # Type format
        type_fmt = QTextCharFormat()
        type_fmt.setForeground(QColor(colors.type))
        self._formats['type'] = type_fmt
        
        # Built-in function format
        builtin_fmt = QTextCharFormat()
        builtin_fmt.setForeground(QColor(colors.builtin))
        self._formats['builtin'] = builtin_fmt
        
        # String format
        string_fmt = QTextCharFormat()
        string_fmt.setForeground(QColor(colors.string))
        self._formats['string'] = string_fmt
        
        # Number format
        number_fmt = QTextCharFormat()
        number_fmt.setForeground(QColor(colors.number))
        self._formats['number'] = number_fmt
        
        # Comment format
        comment_fmt = QTextCharFormat()
        comment_fmt.setForeground(QColor(colors.comment))
        comment_fmt.setFontItalic(True)
        self._formats['comment'] = comment_fmt
        
        # Operator format
        operator_fmt = QTextCharFormat()
        operator_fmt.setForeground(QColor(colors.operator))
        self._formats['operator'] = operator_fmt
        
        # Function format (user-defined)
        function_fmt = QTextCharFormat()
        function_fmt.setForeground(QColor(colors.function))
        self._formats['function'] = function_fmt
        
        # Variable format (for special identifiers)
        variable_fmt = QTextCharFormat()
        variable_fmt.setForeground(QColor(colors.variable))
        self._formats['variable'] = variable_fmt
        
        # Constant format
        constant_fmt = QTextCharFormat()
        constant_fmt.setForeground(QColor(colors.constant))
        self._formats['constant'] = constant_fmt
        
        # Identifier format (default)
        identifier_fmt = QTextCharFormat()
        identifier_fmt.setForeground(QColor(colors.identifier))
        self._formats['identifier'] = identifier_fmt
        
        # Interpolation format (${...})
        interp_fmt = QTextCharFormat()
        interp_fmt.setForeground(QColor(colors.variable))
        self._formats['interpolation'] = interp_fmt
        
        # Attribute format (@...)
        attr_fmt = QTextCharFormat()
        attr_fmt.setForeground(QColor(colors.constant))
        self._formats['attribute'] = attr_fmt
    
    def _setup_rules(self):
        """Set up highlighting rules"""
        self._rules = []
        
        # Keywords (word boundaries required)
        keyword_pattern = r'\b(' + '|'.join(EZ_KEYWORDS) + r')\b'
        self._rules.append((QRegularExpression(keyword_pattern), 'keyword'))
        
        # Types (word boundaries required)
        type_pattern = r'\b(' + '|'.join(EZ_TYPES) + r')\b'
        self._rules.append((QRegularExpression(type_pattern), 'type'))
        
        # Built-in functions
        builtin_pattern = r'\b(' + '|'.join(EZ_BUILTINS) + r')\s*(?=\()'
        self._rules.append((QRegularExpression(builtin_pattern), 'builtin'))
        
        # User-defined function declarations: do name(...)
        func_decl_pattern = r'\bdo\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?=\()'
        self._rules.append((QRegularExpression(func_decl_pattern), 'function'))
        
        # Function calls: name(...)
        func_call_pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*(?=\()'
        self._rules.append((QRegularExpression(func_call_pattern), 'function'))
        
        # Struct/enum names: const Name struct/enum
        struct_pattern = r'\bconst\s+([A-Z][a-zA-Z0-9_]*)\s+(?:struct|enum)\b'
        self._rules.append((QRegularExpression(struct_pattern), 'type'))
        
        # Attributes (@std, @enum, @flags)
        attr_pattern = r'@[a-zA-Z_][a-zA-Z0-9_]*'
        self._rules.append((QRegularExpression(attr_pattern), 'attribute'))
        
        # Numbers (integers and floats with underscores)
        number_pattern = r'\b[0-9][0-9_]*\.?[0-9_]*(?:[eE][+-]?[0-9_]+)?\b'
        self._rules.append((QRegularExpression(number_pattern), 'number'))
        
        # Operators
        operator_pattern = r'[+\-*/%=<>!&|^~:]+|->|\.\.'
        self._rules.append((QRegularExpression(operator_pattern), 'operator'))
        
        # Character literals 'x'
        char_pattern = r"'(?:[^'\\]|\\.)'"
        self._rules.append((QRegularExpression(char_pattern), 'string'))
        
        # String interpolation markers ${...}
        interp_pattern = r'\$\{[^}]*\}'
        self._rules.append((QRegularExpression(interp_pattern), 'interpolation'))
        
        # String literals "..."
        string_pattern = r'"(?:[^"\\]|\\.)*"'
        self._rules.append((QRegularExpression(string_pattern), 'string'))
        
        # Raw strings `...`
        raw_string_pattern = r'`[^`]*`'
        self._rules.append((QRegularExpression(raw_string_pattern), 'string'))
        
        # Single-line comments //
        comment_pattern = r'//[^\n]*'
        self._rules.append((QRegularExpression(comment_pattern), 'comment'))
    
    def highlightBlock(self, text: str):
        """Highlight a single block of text"""
        # Apply regular rules
        for pattern, format_name in self._rules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                # For patterns with capture groups, highlight the group
                if match.lastCapturedIndex() > 0:
                    start = match.capturedStart(1)
                    length = match.capturedLength(1)
                else:
                    start = match.capturedStart(0)
                    length = match.capturedLength(0)
                
                self.setFormat(start, length, self._formats[format_name])
        
        # Handle multi-line comments /* ... */
        self._handle_multiline_comments(text)
    
    def _handle_multiline_comments(self, text: str):
        """Handle multi-line block comments"""
        comment_start = QRegularExpression(r'/\*')
        comment_end = QRegularExpression(r'\*/')
        
        self.setCurrentBlockState(0)
        
        start_index = 0
        if self.previousBlockState() != 1:
            match = comment_start.match(text)
            if match.hasMatch():
                start_index = match.capturedStart()
            else:
                start_index = -1
        
        while start_index >= 0:
            end_match = comment_end.match(text, start_index)
            if end_match.hasMatch():
                end_index = end_match.capturedStart()
                comment_length = end_index - start_index + end_match.capturedLength()
                self.setCurrentBlockState(0)
            else:
                self.setCurrentBlockState(1)
                comment_length = len(text) - start_index
            
            self.setFormat(start_index, comment_length, self._formats['comment'])
            
            start_match = comment_start.match(text, start_index + comment_length)
            if start_match.hasMatch():
                start_index = start_match.capturedStart()
            else:
                start_index = -1


class GenericHighlighter(QSyntaxHighlighter):
    """Generic syntax highlighter for common languages"""
    
    def __init__(self, parent=None, theme: Theme = None, language: str = ""):
        super().__init__(parent)
        self.theme = theme
        self.language = language.lower()
        self._formats: Dict[str, QTextCharFormat] = {}
        self._rules: List[Tuple[QRegularExpression, str]] = []
        
        self._setup_formats()
        self._setup_rules()
    
    def set_theme(self, theme: Theme):
        """Update the theme and recreate formats"""
        self.theme = theme
        self._setup_formats()
        self.rehighlight()
    
    def _setup_formats(self):
        """Set up text formats based on theme colors"""
        if self.theme is None:
            from app.themes import DARK_THEME
            self.theme = DARK_THEME
        
        colors = self.theme.syntax
        
        keyword_fmt = QTextCharFormat()
        keyword_fmt.setForeground(QColor(colors.keyword))
        keyword_fmt.setFontWeight(QFont.Weight.Bold)
        self._formats['keyword'] = keyword_fmt
        
        string_fmt = QTextCharFormat()
        string_fmt.setForeground(QColor(colors.string))
        self._formats['string'] = string_fmt
        
        number_fmt = QTextCharFormat()
        number_fmt.setForeground(QColor(colors.number))
        self._formats['number'] = number_fmt
        
        comment_fmt = QTextCharFormat()
        comment_fmt.setForeground(QColor(colors.comment))
        comment_fmt.setFontItalic(True)
        self._formats['comment'] = comment_fmt
        
        function_fmt = QTextCharFormat()
        function_fmt.setForeground(QColor(colors.function))
        self._formats['function'] = function_fmt
    
    def _setup_rules(self):
        """Set up basic highlighting rules"""
        self._rules = []
        
        # Common programming constructs
        # Numbers
        self._rules.append((QRegularExpression(r'\b[0-9]+\.?[0-9]*\b'), 'number'))
        
        # Strings
        self._rules.append((QRegularExpression(r'"[^"]*"'), 'string'))
        self._rules.append((QRegularExpression(r"'[^']*'"), 'string'))
        
        # Comments (common styles)  
        self._rules.append((QRegularExpression(r'//[^\n]*'), 'comment'))
        self._rules.append((QRegularExpression(r'#[^\n]*'), 'comment'))
    
    def highlightBlock(self, text: str):
        """Highlight a single block of text"""
        for pattern, format_name in self._rules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), 
                             self._formats[format_name])
