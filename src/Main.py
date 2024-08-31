from ply.lex import lex
from ply.yacc import yacc

# All tokens must be named in advance.
reserved = {'int':'INT','char':'CHAR','float':'FLOAT'}

tokens = ( 
    'PLUS', 
    'MINUS', 
    'TIMES', 
    'DIVIDE', 
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
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKETS = r'\['
t_RBRACKETS = r'\]'
t_SEMICOLON = r';'

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
def p_expression(p):
    '''
    expression : term PLUS term
               | term MINUS term
    '''
    # p is a sequence that represents rule contents.
    #
    # expression : term PLUS term
    #   p[0]     : p[1] p[2] p[3]
    # 
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_term(p):
    '''
    expression : term
    '''
    p[0] = p[1]

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
ast = parser.parse('2 * 3 + 4 * (5 - x)')
print(ast)