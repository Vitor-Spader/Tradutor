from ply.lex import lex
from ply.yacc import yacc

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

def p_declaration_term(p):
    '''
    term : CHAR factor_char 
         | INT factor 
         | FLOAT factor
    '''
    p[0] = ('term', p[1], p[2])

# def p_term(p):
#     '''
#     term : CHAR factor_char 
#          | INT factor 
#          | FLOAT factor
#     '''
#     print(p)
#     p[0] = p[1]

def p_term_factor_char(p):
    '''
    factor_char : factor LBRACKETS NUMBER RBRACKETS 
                | factor_char COMMA factor_char 
                | factor COMMA factor
    '''
    p[0] = p[1]


def p_term_factor(p):
    '''
    factor : NAME 
           | NAME COMMA factor
    '''
    p[0] = ('name', p[1])

def p_error(p):
    print(f'Syntax error at {p.value!r}')

# Build the parser
parser = yacc()

# Parse an expression
ast = parser.parse('float a;')
print(ast)