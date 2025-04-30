from typing import List, Dict

# Palavras-chave da linguagem
KEYWORDS = {
    "int", "float", "double", "boolean", "void", "string",
    "true", "false", "null", "if", "else", "switch", "case", "default",
    "for", "while", "do", "break", "continue", "return", "try", "catch",
    "finally", "throw", "public", "private", "protected", "static", "final",
    "abstract", "class", "interface", "extends", "implements", "new",
    "this", "super", "package", "import"
}

# Operadores
OPERATORS = {
    "==", "!=", ">=", "<=", "++", "--", "+=", "-=", "*=", "/=",
    "+", "-", "*", "/", "=", ">", "<", "&&", "||", "!", "instanceof"
}

# Delimitadores
DELIMITERS = {"{", "}", "(", ")", "[", "]", ";", ",", ".", ":", "@"}

# Tabelas
symbol_table = set()
tokens: List[Dict] = []
errors: List[Dict] = []

# Auxiliares
def is_identifier_start(char):
    return char.isalpha() or char == '_'

def is_identifier_char(char):
    return char.isalnum() or char == '_'

# Tokenização de uma linha
def tokenize_line(line: str, line_number: int):
    i = 0
    while i < len(line):
        ch = line[i]

        # Ignora espaços
        if ch.isspace():
            i += 1
            continue

        # Comentários de linha
        if line[i:i+2] == "//":
            break

        # Ignorar /* ou */ diretamente
        if line[i:i+2] in {"/*", "*/"}:
            i += 2
            continue

        # Strings
        if ch == '"':
            end = i + 1
            while end < len(line) and line[end] != '"':
                end += 1
            if end >= len(line):
                errors.append({"line": line_number, "lexeme": line[i:], "message": "String literal não fechada"})
                break
            tokens.append({"line": line_number, "token": "STRING_LITERAL", "lexeme": line[i:end+1]})
            i = end + 1
            continue

        # Operadores
        matched = False
        for op in sorted(OPERATORS, key=len, reverse=True):
            if line.startswith(op, i):
                tokens.append({"line": line_number, "token": "OPERATOR", "lexeme": op})
                i += len(op)
                matched = True
                break
        if matched:
            continue

        # Delimitadores
        if ch in DELIMITERS:
            tokens.append({"line": line_number, "token": "DELIMITER", "lexeme": ch})
            i += 1
            continue

        # Números
        if ch.isdigit():
            start = i
            has_dot = False
            while i < len(line) and (line[i].isdigit() or (line[i] == '.' and not has_dot)):
                if line[i] == '.':
                    has_dot = True
                i += 1
            lex = line[start:i]
            token_type = "NUMBER_FLOAT" if '.' in lex else "NUMBER_INT"
            tokens.append({"line": line_number, "token": token_type, "lexeme": lex})
            continue

        # Identificadores e palavras-chave
        if is_identifier_start(ch):
            start = i
            while i < len(line) and is_identifier_char(line[i]):
                i += 1
            lex = line[start:i]
            if lex in KEYWORDS:
                tokens.append({"line": line_number, "token": "KEYWORD", "lexeme": lex})
            else:
                tokens.append({"line": line_number, "token": "IDENTIFIER", "lexeme": lex})
                symbol_table.add(lex)
            continue

        # Lexema inválido
        errors.append({"line": line_number, "lexeme": ch, "message": "Lexema inválido"})
        i += 1

# Análise com suporte a comentários multilinha
def analisar_codigo(codigo: str):
    inside_block_comment = False
    i = 0
    lines = codigo.splitlines()

    while i < len(lines):
        line = lines[i]
        if inside_block_comment:
            end = line.find("*/")
            if end != -1:
                inside_block_comment = False
                lines[i] = line[end + 2:]
            else:
                i += 1
                continue
        start = line.find("/*")
        if start != -1:
            inside_block_comment = True
            before = line[:start]
            tokenize_line(before, i + 1)
            i += 1
            continue
        tokenize_line(line, i + 1)
        i += 1

    if inside_block_comment:
        errors.append({
            "line": len(lines),
            "lexeme": "/* comentário de bloco sem fechamento",
            "message": "Comentário de bloco não fechado"
        })

# Impressão dos resultados
def imprimir_resultado():
    print("\n### Lista de Tokens Reconhecidos:")
    for t in tokens:
        print(f"Linha {t['line']:>2}: {t['token']:<14} => {t['lexeme']}")
    print("\n### Tabela de Símbolos:")
    for s in sorted(symbol_table):
        print(f"ID => {s}")
    print("\n### Relatório de Erros Léxicos:")
    for e in errors:
        print(f"Linha {e['line']}: '{e['lexeme']}' → {e['message']}")

# Leitura do código
def carregar_codigo():
    try:
        with open("index.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("Arquivo 'index.txt' não encontrado. Insira código manualmente (Ctrl+D para encerrar):")
        return "".join(iter(input, ""))

# Execução principal
if __name__ == "__main__":
    codigo = carregar_codigo()
    analisar_codigo(codigo)
    imprimir_resultado()
