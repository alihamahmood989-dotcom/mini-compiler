# =========================
# MINI COMPILER: STEP 1–6
# =========================

import re

# ===== STEP 1: LEXICAL ANALYZER =====
TOKEN_SPECIFICATION = [
    ('KEYWORD',  r'\bint\b'),      # keyword
    ('ID',       r'[a-zA-Z_]\w*'), # identifier
    ('NUMBER',   r'\d+'),           # number
    ('ASSIGN',   r'='),
    ('OP',       r'[+\-*/]'),
    ('SEMICOL',  r';'),
    ('SKIP',     r'[ \t\n]+'),      # spaces/newlines
]

def lexer(code):
    token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECIFICATION)
    tokens = []
    for match in re.finditer(token_regex, code):
        kind = match.lastgroup
        value = match.group()
        if kind == 'SKIP':
            continue
        tokens.append((kind, value))
    return tokens

# ===== STEP 2: SYNTAX ANALYZER =====
def parser(tokens):
    if len(tokens) < 5:
        raise SyntaxError("Incomplete statement")
    if tokens[0][0] != 'KEYWORD':
        raise SyntaxError("Declaration missing")
    if tokens[1][0] != 'ID':
        raise SyntaxError("Identifier expected")
    if tokens[2][0] != 'ASSIGN':
        raise SyntaxError("Assignment '=' missing")
    if tokens[-1][0] != 'SEMICOL':
        raise SyntaxError("Semicolon missing")
    print("Syntax correct ✔")

# ===== STEP 3: SEMANTIC ANALYZER =====
symbol_table = {}

def semantic_analysis(tokens):
    var = tokens[1][1]
    if var in symbol_table:
        raise Exception("Variable already declared")
    symbol_table[var] = 'int'
    print("Semantic correct ✔")

# ===== STEP 4: INTERMEDIATE CODE GENERATION =====
def generate_ir(tokens):
    ir = []
    # t1 = 5 + 3
    ir.append(f"t1 = {tokens[3][1]} {tokens[4][1]} {tokens[5][1]}")
    # a = t1
    ir.append(f"{tokens[1][1]} = t1")
    return ir

# ===== STEP 5: IR OPTIMIZATION =====
def optimize_ir(ir):
    optimized = []
    for line in ir:
        if '+' in line or '-' in line or '*' in line or '/' in line:
            left, expr = line.split('=')
            a, op, b = expr.strip().split()
            result = eval(a + op + b)
            optimized.append(f"{left}= {result}")
        else:
            optimized.append(line)
    return optimized

# ===== STEP 6: TARGET CODE GENERATION =====
def generate_target_code(ir):
    code = []
    for line in ir:
        left, right = line.split('=')
        code.append(f"LOAD {right.strip()}")
        code.append(f"STORE {left.strip()}")
    return code

# ===== TESTING =====
source_code = "int a = 5 + 3;"
tokens = lexer(source_code)

print("TOKENS:")
for t in tokens:
    print(t)

parser(tokens)
semantic_analysis(tokens)

ir = generate_ir(tokens)
print("\nIntermediate Code (IR):")
for line in ir:
    print(line)

optimized_ir = optimize_ir(ir)
print("\nOptimized IR:")
for line in optimized_ir:
    print(line)

target_code = generate_target_code(optimized_ir)
print("\nTarget Code:")
for line in target_code:
    print(line)






