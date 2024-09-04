from ply.lex import lex
from ply.yacc import yacc

tokens = ( 
    'LPAREN', 
    'RPAREN',
    'NAME', 
    'NUMBER',
    'REALNUMBER',
    'LBRACKETS',
    'RBRACKETS',
    'COMMA',
    'SEMICOLON',
    'TYPE'
)

# Ignored characters
t_ignore = ' \t\n'

# Token matching rules are written as regexs
t_TYPE = r'^int\b|^float\b|^char\b'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKETS = r'\['
t_RBRACKETS = r'\]'
t_SEMICOLON = r';'
t_COMMA = r','
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

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

data = '''
int ;
'''

#lexer.input(data)

#while True:
#    tok = lexer.token()
    # if not tok:
    #     break
    # print(tok)

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
    print(p[0])

def p_declaration_term(p):
    '''
    term: CHAR factor_char | type factor
    '''
    p[0] = (p[1])

def p_term(p):
    '''
    term : factor TIMES factor
         | factor DIVIDE factor
    '''
    p[0] = ('binop', p[2], p[1], p[3])

def p_term_factor(p):
    '''
    term : factor
    '''
    p[0] = p[1]

def p_factor_number(p):
    '''
    factor : NUMBER
    '''
    p[0] = ('number', p[1])

def p_factor_name(p):
    '''
    factor : NAME
    '''
    p[0] = ('name', p[1])

def p_factor_unary(p):
    '''
    factor : PLUS factor
           | MINUS factor
    '''
    p[0] = ('unary', p[1], p[2])

def p_factor_grouped(p):
    '''
    factor : LPAREN expression RPAREN
    '''
    p[0] = ('grouped', p[2])

def p_error(p):
    print(f'Syntax error at {p.value!r}')

# Build the parser
parser = yacc()

# Parse an expression
ast = parser.parse('int a;')
print(ast)