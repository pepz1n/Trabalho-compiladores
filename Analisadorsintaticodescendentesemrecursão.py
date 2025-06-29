import re
from typing import List, Dict

# Tabela sintática LL(1) atualizada

tabela_sintatica = {
    # S (sequência de instruções)
    ('S', 'public'): ['U', 'S'],
    ('S', 'private'): ['U', 'S'],
    ('S', 'protected'): ['U', 'S'],
    ('S', 'static'): ['U', 'S'],
    ('S', 'final'): ['U', 'S'],
    ('S', 'abstract'): ['U', 'S'],
    ('S', 'int'): ['U', 'S'],
    ('S', 'boolean'): ['U', 'S'],
    ('S', 'ID'): ['U', 'S'],
    ('S', 'if'): ['U', 'S'],
    ('S', 'while'): ['U', 'S'],
    ('S', 'do'): ['U', 'S'],
    ('S', 'for'): ['U', 'S'],
    ('S', 'break'): ['U', 'S'],
    ('S', 'continue'): ['U', 'S'],
    ('S', 'return'): ['U', 'S'],
    ('S', 'try'): ['U', 'S'],
    ('S', 'throw'): ['U', 'S'],
    ('S', '{'): ['U', 'S'],
    ('S', '}'): ['ε'],
    ('S', '$'): ['ε'],

    # U (instrução única)
    # ('U', 'public'): ['D', 'class', 'ID', '{', 'H', '}'],
    # ('U', 'private'): ['D', 'class', 'ID', '{', 'H', '}'],
    ('U', 'public'): ['D', 'K', 'ID', '{', 'H', '}'],
    ('U', 'private'): ['D', 'K', 'ID', '{', 'H', '}'],
    ('U', 'protected'): ['D', 'K', 'ID', '{', 'H', '}'],
    ('U', 'static'): ['D', 'K', 'ID', '{', 'H', '}'],
    ('U', 'final'): ['D', 'K', 'ID', '{', 'H', '}'],
    ('U', 'abstract'): ['D', 'K', 'ID', '{', 'H', '}'],

    ('U', 'if'): ['C'],
    ('U', 'while'): ['C'],
    ('U', 'do'): ['C'],
    ('U', 'for'): ['C'],
    ('U', 'break'): ['C'],
    ('U', 'continue'): ['C'],
    ('U', 'return'): ['C'],
    ('U', 'try'): ['C'],
    ('U', 'throw'): ['C'],
    ('U', '{'): ['C'],
    ('U', 'ID'): ['G', ';'],
    ('U', 'int'): ['int', "T'", 'ID', '=', 'G', ';'],
    ('U', 'boolean'): ['boolean', "T'", 'ID', '=', 'G', ';'],

    # T' (array opcional)
    ("T'", '['): ['[', ']'],
    ("T'", 'ID'): ['ε'],

    # D (modificadores)
    ('D', 'public'): ['public'],
    ('D', 'private'): ['private'],
    ('D', 'protected'): ['protected'],
    ('D', 'static'): ['static'],
    ('D', 'final'): ['final'],
    ('D', 'abstract'): ['abstract'],

    # C (comandos)
    ('C', 'if'): ['if', '(', 'G', ')', 'S'],
    ('C', 'while'): ['while', '(', 'G', ')', 'S'],
    ('C', 'do'): ['do', 'S', 'while', '(', 'G', ')', ';'],
    ('C', 'for'): ['for', '(', 'G', ';', 'G', ';', 'G', ')', 'S'],
    ('C', 'break'): ['break', ';'],
    ('C', 'continue'): ['continue', ';'],
    ('C', 'return'): ['return', 'G', ';'],
    ('C', 'try'): ['try', '{', 'H', '}', 'catch', '(', 'ID', ')', '{', 'H', '}', 'finally', '{', 'H', '}'],
    ('C', 'throw'): ['throw', 'G', ';'],
    ('C', '{'): ['{', 'H', '}'],

    # H (bloco)
    ('H', 'public'): ['S', "H'"],
    ('H', 'private'): ['S', "H'"],
    ('H', 'protected'): ['S', "H'"],
    ('H', 'static'): ['S', "H'"],
    ('H', 'final'): ['S', "H'"],
    ('H', 'abstract'): ['S', "H'"],
    ('H', 'if'): ['S', "H'"],
    ('H', 'while'): ['S', "H'"],
    ('H', 'do'): ['S', "H'"],
    ('H', 'for'): ['S', "H'"],
    ('H', 'break'): ['S', "H'"],
    ('H', 'continue'): ['S', "H'"],
    ('H', 'return'): ['S', "H'"],
    ('H', 'try'): ['S', "H'"],
    ('H', 'throw'): ['S', "H'"],
    ('H', '{'): ['S', "H'"],
    ('H', 'ID'): ['S', "H'"],
    ('H', 'int'): ['S', "H'"],
    ('H', 'boolean'): ['S', "H'"],
    ('H', '}'): ['ε'],

    # H' (continuação de H)
    ("H'", 'public'): ['S', "H'"],
    ("H'", 'private'): ['S', "H'"],
    ("H'", 'protected'): ['S', "H'"],
    ("H'", 'static'): ['S', "H'"],
    ("H'", 'final'): ['S', "H'"],
    ("H'", 'abstract'): ['S', "H'"],
    ("H'", 'if'): ['S', "H'"],
    ("H'", 'while'): ['S', "H'"],
    ("H'", 'do'): ['S', "H'"],
    ("H'", 'for'): ['S', "H'"],
    ("H'", 'break'): ['S', "H'"],
    ("H'", 'continue'): ['S', "H'"],
    ("H'", 'return'): ['S', "H'"],
    ("H'", 'try'): ['S', "H'"],
    ("H'", 'throw'): ['S', "H'"],
    ("H'", '{'): ['S', "H'"],
    ("H'", 'ID'): ['S', "H'"],
    ("H'", 'int'): ['S', "H'"],
    ("H'", 'boolean'): ['S', "H'"],
    ("H'", '}'): ['ε'],

    # G (expressões)
    ('G', 'ID'): ['ID', "G'"],
    ('G', 'D'): ['D', "G'"],
    ('G', '('): ['(', 'G', ')', "G'"],
    ('G', '!'): ['!', 'G'],
    ('G', '-'): ['-', 'G'],
    ('G', '+'): ['+', 'G'],
    ('G', '{'): ['{', 'L', '}'],

   # G' (continuação de expressão)
    ("G'", '='): ['=', 'G'],
    ("G'", '+='): ['+=', 'G'],
    ("G'", '-='): ['-=', 'G'],
    ("G'", '*='): ['*=', 'G'],
    ("G'", '/='): ['/=', 'G'],
    ("G'", '++'): ['++'],
    ("G'", '--'): ['--'],
    ("G'", '+'): ['+', 'G'],
    ("G'", '-'): ['-', 'G'],
    ("G'", '*'): ['*', 'G'],
    ("G'", '/'): ['/', 'G'],
    ("G'", '=='): ['==', 'G'],
    ("G'", '!='): ['!=', 'G'],
    ("G'", '>'): ['>', 'G'],
    ("G'", '<'): ['<', 'G'],
    ("G'", '>='): ['>=', 'G'],
    ("G'", '<='): ['<=', 'G'],
    ("G'", '&&'): ['&&', 'G'],
    ("G'", '||'): ['||', 'G'],
    ("G'", '('): ['(', 'ListaArgumentos', ')'],
    ("G'", ';'): ['ε'],
    ("G'", ')'): ['ε'],
    ("G'", ','): ['ε'],
    ("G'", ']'): ['ε'],

    # L (lista dentro de chaves)
    ('L', 'D'): ['D', "L'"],
    ("L'", ','): [',', 'D', "L'"],
    ("L'", '}'): ['ε'],

    ('K', 'class'): ['class'],
    ('K', 'interface'): ['interface'],
}

terminais = {
    'public', 'private', 'protected', 'static', 'final', 'abstract',
    'class', 'interface', 'ID', '{', '}', '(', ')', ';', '=', '+=',
    '-=', '*=', '/=', '++', '--', 'if', 'while', 'do', 'for',
    'break', 'continue', 'return', 'try', 'catch', 'finally', 'throw',
    'ListaArgumentos', '$', 'int', 'boolean', '[', ']', '!', '+', '-'
}

def ler_tokens_arquivo(nome_arquivo: str) -> List[str]:
    tokens = []
    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        for linha in f:
            if not linha.startswith("Linha"):
                continue
            partes = linha.strip().split()
            if len(partes) >= 5:
                categoria = partes[3]
                tokens.append(categoria)
    return tokens

def analisador(tokens):
    print("\nTokens de entrada:")
    print(tokens)
    pilha = ['$', 'S']
    entrada = tokens + ['$']

    print(f"\n{'PILHA':<40} {'ENTRADA':<40} AÇÃO")
    while pilha:
        topo = pilha.pop()
        atual = entrada[0]

        print(f"{' '.join(pilha):<40} {' '.join(entrada):<40}", end=' ')

        if topo == atual:
            print(f"✔️ Consome '{atual}'")
            entrada.pop(0)
        elif topo in terminais:
            print(f"❌ Erro: esperado '{topo}', encontrado '{atual}'")
            return False
        elif (topo, atual) in tabela_sintatica:
            producao = tabela_sintatica[(topo, atual)]
            print(f"→ {topo} → {' '.join(producao)}")
            for simbolo in reversed(producao):
                if simbolo != 'ε':
                    pilha.append(simbolo)
        else:
            print(f"❌ Erro: sem produção para ({topo}, {atual})")
            return False

        if topo == '$' and atual == '$':
            break

    print("✅ Análise sintática concluída com sucesso.")
    return True

if __name__ == "__main__":
    tokens = ler_tokens_arquivo("resultado_lexico.txt")
    analisador(tokens)