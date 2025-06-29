import re
from typing import List, Dict
import sys

KEYWORDS = {
    'int', 'float', 'double', 'boolean', 'void', 'string',
    'true', 'false', 'null', 'if', 'else', 'switch', 'case', 'default',
    'break', 'continue', 'return', 'try', 'catch', 'finally', 'throw',
    'public', 'private', 'protected', 'static', 'final', 'abstract',
    'class', 'interface', 'extends', 'implements', 'new',
    'this', 'super', 'package', 'import'
}

TOKEN_REGEX = [
    (r'//.*',                          'COMMENT'),
    (r'/\*[\s\S]*?\*/',                'BLOCK_COMMENT'),
    (r'\b(true|false|null)\b',         'LITERAL'),
    (r'\b(int|float|double|boolean|void|string)\b', 'TYPE'),
    (r'"[^"]*"',                       'STRING_LITERAL'),
    (r'\b(if|else|switch|case|default)\b', 'CONTROL'),
    (r'\b(for|while|do)\b',            'LOOP'),
    (r'\b(break|continue|return)\b',   'FLOW'),
    (r'\b(try|catch|finally|throw)\b', 'EXCEPTION'),
    (r'\b(public|private|protected|static|final|abstract)\b', 'MODIFIER'),
    (r'\b(class|interface|extends|implements|new|this|super|package|import|System)\b', 'KEYWORD'),
    (r'(\+\+|--|==|!=|>=|<=|&&|\|\||\+=|-=|\*=|/=|%=|instanceof|[+\-*/=><!%])', 'OPERATOR'),
    (r'\b(?!' + '|'.join(KEYWORDS) + r'\b)[a-zA-Z_][a-zA-Z0-9_]*\b', 'IDENTIFIER'),
    (r'\d+\.\d+',                      'NUMDEC'),
    (r'\d+',                           'NUMINT'),
    (r'[{}()\[\];,:\.@]',              'DELIMITER'),
]

class LexicalAnalyzer:
    def __init__(self):
        self.symbol_table = set()
        self.tokens: List[Dict] = []
        self.errors: List[Dict] = []
        self.regex_patterns = self._compile_regex()

    def _compile_regex(self) -> re.Pattern:
        combined = '|'.join(f'(?P<{name}>{pattern})' for pattern, name in TOKEN_REGEX if name)
        return re.compile(combined)

    def _tokenize_line(self, line: str, line_num: int):
        pos = 0
        while pos < len(line):
            if line[pos].isspace():
                pos += 1
                continue
            match = self.regex_patterns.match(line, pos)
            if match:
                token_type = match.lastgroup
                lexeme = match.group()
                pos = match.end()

                if token_type in ['COMMENT', 'BLOCK_COMMENT']:
                    continue

                if token_type == 'IDENTIFIER':
                    if lexeme in KEYWORDS:
                        token_type = 'KEYWORD'
                    else:
                        self.symbol_table.add(lexeme)
                        categoria = 'ID'
                elif token_type == 'NUMINT':
                    categoria = 'D'
                elif token_type == 'NUMDEC':
                    categoria = 'NUMDEC'
                elif token_type == 'STRING_LITERAL':
                    categoria = 'L'
                else:
                    categoria = lexeme  # Para operadores e delimitadores

                if token_type not in ['COMMENT', 'BLOCK_COMMENT']:
                    self.tokens.append({
                        'line': line_num,
                        'token': token_type,
                        'categoria': categoria,
                        'lexeme': lexeme
                    })
            else:
                start = pos
                while pos < len(line) and not line[pos].isspace():
                    pos += 1
                invalid_lex = line[start:pos]
                self.errors.append({
                    'line': line_num,
                    'lexeme': invalid_lex,
                    'message': 'Lexema inválido'
                })

    def analyze(self, code: str):
        in_block_comment = False
        current_line = 1
        for line in code.split('\n'):
            if in_block_comment:
                end = line.find('*/')
                if end != -1:
                    in_block_comment = False
                    line = line[end+2:]
                else:
                    current_line += 1
                    continue
            start = line.find('/*')
            if start != -1:
                in_block_comment = True
                self._tokenize_line(line[:start], current_line)
                line = line[start+2:]
            if in_block_comment:
                end = line.find('*/')
                if end != -1:
                    in_block_comment = False
                    line = line[end+2:]
                else:
                    current_line += 1
                    continue
            if not in_block_comment:
                self._tokenize_line(line, current_line)
            current_line += 1
        if in_block_comment:
            self.errors.append({
                'line': current_line,
                'lexeme': '*/',
                'message': 'Comentário de bloco não fechado'
            })

    def save_results(self, filename: str):
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n=== Tokens Reconhecidos ===\n")
            for token in self.tokens:
                f.write(f"Linha {token['line']:3}: {token['token']:<15} {token['categoria']:<15} {token['lexeme']}\n")
            f.write("\n=== Tabela de Símbolos ===\n")
            for symbol in sorted(self.symbol_table):
                f.write(f"  {symbol}\n")
            f.write("\n=== Erros Léxicos ===\n")
            for error in self.errors:
                f.write(f"Linha {error['line']:3}: '{error['lexeme']}' - {error['message']}\n")

def load_code(filename: str) -> str:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("Arquivo não encontrado. Insira o código (Ctrl+Z + Enter para finalizar):")
        return sys.stdin.read()

if __name__ == "__main__":
    analyzer = LexicalAnalyzer()
    code = load_code("index.txt")
    analyzer.analyze(code)
    analyzer.save_results("resultado_lexico.txt")
