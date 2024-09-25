from ply.lex import lex
from ply.yacc import yacc

reserved = {'int':'INT','char':'CHAR','float':'FLOAT'}

tokens = ( 
    'LPAREN', 
    'RPAREN',
    'NAME', 
    'NUMBER',
    'REALNUMBER',
    'LBRACKETS',
    'RBRACKETS',
    'COMMA',
    'SEMICOLON'
) + tuple(reserved.values())

# Ignored characters
t_ignore = ' \t\n'

# Token matching rules are written as regexs
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKETS = r'\['
t_RBRACKETS = r'\]'
t_SEMICOLON = r';'
t_COMMA = r','

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'NAME')
    return t

def t_REALNUMBER(t):
    r'(\d+\.\d+)'
    t.value = float(t.value)
    return t

# A function can be used if there is an associated action.
# Write the matching regex in the docstring.
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

# Build the lexer object
lexer = lex()

index  = 1
# Write functions for each grammar rule which is
# specified in the docstring.
def p_declaration(p):
    '''
    declaration : term SEMICOLON
    '''
    # p is a sequence that represents rule contents.
    #
    # expression : term SEMICOLON
    #   p[0]     : p[1] p[2]
    # 
    p[0] = ('declaration', p[1], p[2])

def p_declaration_term_char(p):
    '''
    term : CHAR factor_char
         | INT factor_number
         | FLOAT factor_number
    '''
    p[0] = (p[1], p[2])

def p_term_factor_number(p):
    '''
    factor_number : factor

    '''
    p[0] = p[1] 

def p_term_factor_char(p):
    '''
    factor_char : factor LBRACKETS NUMBER RBRACKETS 	
                | factor_char COMMA factor_char
                | factor

    '''
    if len(p) == 5:
        p[0] = ('char_length', p[1], p[2], p[3], p[4])
    elif len(p) == 4:
        p[0] = ('list', p[1], p[2], p[3])
    else:
        p[0] = p[1]   

def p_term_factor(p):
    '''
    factor : factor COMMA NAME
           | NAME
    '''
    if len(p) == 4:
        p[0] = ('list', p[1], p[2],('name', p[3]))
    else:
        p[0] = ('name', p[1])


precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)

# dictionary of names
names = {}

def p_statement_assign(p):
    'statement : NAME "=" expression'
    names[p[1]] = p[3]


def p_statement_expr(p):
    'statement : expression'
    print(p[1])


def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]


def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]


def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]


def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0


def p_error(p):
    print(f'Syntax error at {p.value!r}')

# Build the parser
parser = yacc()

# Parse an expression
ast = parser.parse(input('digite a expressao: '))
print(ast)