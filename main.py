import ply.lex as lex
import ply.yacc as yacc

# Definición de tokens
tokens = (
    'ID',
    'EQUALS',
    'LPAREN',
    'RPAREN',
    'PLUS',
    'NUMBER',
    'PRINT',
    'NEWLINE',
)

# Expresiones regulares para los tokens
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_NUMBER = r'\d+'
t_PRINT = r'print'
t_NEWLINE = r'\n'

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Manejo de errores léxicos
def t_error(t):
    print(f"Ilegal character '{t.value[0]}' at position {t.lexpos}")
    t.lexer.skip(1)

# Construcción del analizador léxico
lexer = lex.lex()

# Reglas de la gramática
def p_statements(p):
    '''
    statements : statement
               | statements statement
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement_assign(p):
    'statement : ID EQUALS expression NEWLINE'
    p[0] = f'var {p[1]} = {p[3]};'

def p_statement_print(p):
    'statement : ID LPAREN expression RPAREN NEWLINE'
    p[0] = f'console.log({p[1]});'

def p_expression_binop(p):
    '''
    expression : expression PLUS term
               | term
    '''
    if len(p) == 4:
        p[0] = f'{p[1]} + {p[3]}'
    else:
        p[0] = p[1]

def p_term_number(p):
    'term : NUMBER'
    p[0] = p[1]

def p_term_id(p):
    'term : ID'
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' at position {p.lexpos}")
    else:
        print("Syntax error: unexpected end of file")

# Regla para manejar el final del archivo
def p_empty(p):
    'empty :'
    pass

# Crear analizador sintactico
parser = yacc.yacc()

# Traductor de Python a JavaScript
def translate_python_to_js(python_code):
    return parser.parse(python_code)

# Bucle principal
while True:
    # Entrada de usuario
    print("Ingresa el código en Python. Presiona Enter para traducir. Para salir, deja una línea en blanco. Para salir ingresa la letra Q")
    lines_of_code = []
    while True:
        line = input()
        if not line:
            break
        lines_of_code.append(line)

    python_code = '\n'.join(lines_of_code)

    # Agregamos una nueva línea al final del código para manejar EOF
    python_code += '\n'

    # Verificar si el usuario quiere salir
    if python_code.strip().lower() == 'q':
        break

    # Traducción y resultado
    js_code = translate_python_to_js(python_code)
    print("\nTraducción a JavaScript:")
    print(js_code)
