from ply.lex import lex
from ply.yacc import yacc

reserved = {
    'int':'INT',
    'char':'CHAR',
    'float':'FLOAT',
    'if':'IF',
    'else':'ELSE',
    'while':'WHILE'
}

tokens = ( 
    'PLUS_EQUAL',#Soma a variavel de destino a segunda variáve informada i += x
    'MINUS_EQUAL',#Subtrai a variavel de destino a segunda variáve informada i -= x
    'TIMES_EQUAL',#Soma a variavel de destino a segunda variáve informada i += x
    'DIVIDE_EQUAL',#Subtrai a variavel de destino a segunda variáve informada i -= x
    'MINUS',
    'PLUS',
    'MINUS_ONE',#Subtrai um i--
    'PLUS_ONE',#Soma um i++
    'TIMES',
    'DIVIDE',
    'LPAREN', 
    'RPAREN',
    'EQUAL',
    'NAME', 
    'NUMBER',
    'CHAR_VALUE',#Cadeia de caracteres
    'REALNUMBER',
    'COMMA',
    'SEMICOLON'
) + tuple(reserved.values())

# Ignored characters
t_ignore = ' \t\n'

literals = [';', ',']

t_PLUS_EQUAL = r'\+='
t_MINUS_EQUAL = r'-='
t_TIMES_EQUAL = r'\*='
t_DIVIDE_EQUAL = r'/='
t_PLUS_ONE = r'\+\+'
t_MINUS_ONE = '--'
t_MINUS = '-'
t_PLUS = r'\+'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUAL = r'='
t_CHAR_VALUE = r"'.*'"

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


precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)


##### MATH ##########
def p_math_expr_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]

def p_expression(p):
    '''expression : expression PLUS term
                  | expression MINUS term
                  | NAME assig_expression
                  | term
    '''
    if len(p) == 4:
        p[0] = (p[2], # Operation 
                p[1], # term
                p[3]  # factor
               )
    elif len(p) == 3:
        p[0] = (p[2], # NAME 
                p[1] # assig_expression
               )
    else:
        p[0] = p[1]

def p_math_expression(p):
    '''term : term TIMES factor
            | term DIVIDE factor
    '''
    p[0] = (p[2], # Operation 
            p[1], # term
            p[3]  # factor
            )

def p_math_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_math_factor_num(p):
    '''factor : NUMBER
              | REALNUMBER
              | NAME 
    '''
    p[0] = p[1]

def p_math_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]


####### ASSIGNMENT #######

def p_assig_expression(p):
    '''assig_expression : EQUAL assig_term_factor
                        | PLUS_EQUAL assig_term
                        | MINUS_EQUAL assig_term
                        | TIMES_EQUAL assig_term
                        | DIVIDE_EQUAL assig_term
    '''
    p[0] = (p[1], # Operation 
            p[2] # term
            )

def p_assig_term_factor(p):
    '''assig_term_factor : assig_term
                         | CHAR_VALUE
    '''
    p[0] = p[1]

def p_assig_term(p):
    '''assig_term : NAME
                  | NUMBER
                  | REALNUMBER
    '''
    p[0] = p[1]

####### RELATIONAL ########

def p_error(p):
    print(f'Syntax error at {p.value!r}')

# Build the parser
parser = yacc()

# Parse an expression
ast = parser.parse('X = 1')
print(ast)