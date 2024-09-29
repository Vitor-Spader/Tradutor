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
    'EQUAL_TO',
    'EQUAL',
    'NOT_EQUAL',
    'LESS_THAN',
    'GREATER_THAN',
    'LESS_EQUAL',
    'GREATER_EQUAL',
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
    'LBRACKET', 
    'RBRACKET',
    'LCBRACKET',
    'RCBRACKET',
    'NAME', 
    'NUMBER',
    'CHAR_VALUE',#Cadeia de caracteres
    'REALNUMBER',
    'COMMA',
    'SEMICOLON'
) + tuple(reserved.values())

# Ignored characters
t_ignore = ' \t\n'

t_SEMICOLON = r';'
t_EQUAL_TO = r'=='
t_EQUAL = r'='
t_NOT_EQUAL = r'!='
t_LESS_THAN = r'<'
t_GREATER_THAN = r'>'
t_LESS_EQUAL = r'<='
t_GREATER_EQUAL = r'>='
t_PLUS_EQUAL = r'\+='
t_MINUS_EQUAL = r'-='
t_TIMES_EQUAL = r'\*='
t_DIVIDE_EQUAL = r'/='
t_PLUS_ONE = r'\+\+'
t_MINUS_ONE = r'--'
t_MINUS = r'-'
t_PLUS = r'\+'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\[' 
t_RBRACKET = r'\]'
t_LCBRACKET = r'\{'
t_RCBRACKET = r'\}'
t_CHAR_VALUE = r"'.*'"
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

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)

########## GRAMÁTICA GLOBAL ##########
def p_declaration(p):
    '''declaration : expression terminal_semicolon declaration
                   | assign_expression terminal_semicolon declaration
                   | empty
    '''
    if len(p) == 4:
        p[0] = (
            'instr', #ID instruction
            p[1], # expression_terminal
            #p[2], # terminal_semicolon
            p[3]  # declaration
        )
    
def p_expression(p):
    '''expression : declar_expression
                  | cond_expression
                  | loop_expression
    '''
    p[0] = p[1]

def p_term_num_char(p):
    '''term_num_char : terminal_num
                     | terminal_char
    '''
    p[0] = p[1] #terminal_num/terminal_char

def p_terminal_num(p):
    '''terminal_num : terminal_number
	                | REALNUMBER
	                | terminal_name
    '''
    p[0] = p[1]

def p_terminal_name(p):
    '''terminal_name : NAME
    '''
    p[0] = p[1]

def p_terminal_number(p):
    '''terminal_number : NUMBER
    '''
    p[0] = p[1]

def p_terminal_char(p):
    '''terminal_char : CHAR_VALUE
    '''
    p[0] = p[1]

def p_terminal_lparen(p):
    '''terminal_lparen : LPAREN
    '''
    p[0] = p[1]

def p_terminal_rparen(p):
    '''terminal_rparen : RPAREN
    '''
    p[0] = p[1]

def p_terminal_lcbracket(p):
    '''terminal_lcbracket : LCBRACKET
    '''
    p[0] = p[1]

def p_terminal_rcbracket(p):
    '''terminal_rcbracket : RCBRACKET
    '''
    p[0] = p[1]

def p_terminal_semicolon(p):
    '''terminal_semicolon : SEMICOLON
    '''
    p[0] = p[1]

def p_empty(p):
    'empty :'
    pass
    
########## Gramática -> Declaração de Variáveis ##########
def p_declar_expression(p):
    '''declar_expression : INT declar_factor
                         | FLOAT declar_factor
                         | CHAR declar_factor_char
    '''
    p[0] = (p[1], # TYPE 
            p[2], # declar_factor/declar_factor_char
            )
    
def p_declar_factor_char(p):
    '''declar_factor_char : declar_factor LBRACKET terminal_number RBRACKET 	
                          | declar_factor   
    '''
    if len(p) == 5:
        p[0] = (
                p[1], # declar_factor 
                p[2], # LBRACKET
                p[3], # terminal_number
                p[4]  # RBRACKET
               )
    elif len(p) == 2:
        p[0] = p[1]

def p_declar_factor(p):
    '''declar_factor : terminal_name COMMA declar_factor
                     | terminal_name
    '''
    if len(p) == 2:
        p[0] = p[1] #NAME 
               
    elif len(p) == 4:
        p[0] = (
                p[1], # terminal_name
                #p[2], # COMMA
                p[3]  # declar_factor
               )
               
########## Gramática -> Operações Matemáticas ##########
def p_math_expression_uminus(p):
    'math_expression : MINUS math_expression %prec UMINUS'
    p[0] = -p[2]

def p_math_expression(p):
    '''math_expression : math_expression PLUS math_term
                       | math_expression MINUS math_term 
                       | math_term
    '''
    if len(p) == 2:
        p[0] = p[1] #math_term 
    elif len(p) == 4:
        p[0] = (
                p[2], # math_expression 
                p[1], # PLUS/MINUS
                p[3]  # math_term
               )
        
def p_math_term(p):
    '''math_term : math_term TIMES math_factor 
        	     | math_term DIVIDE math_factor
                 | math_factor
    '''
    if len(p) == 2:
        p[0] = p[1] #math_factor
    elif len(p) == 4:
        if (p[2] == '/' and p[3] == 0):
            print(f'Syntax error at 0, Division By Zero')
            raise SyntaxError
        
        p[0] = (
                p[2], # TIMES/DIVIDE 
                p[1], # math_term
                p[3]  # math_factor
               )

def p_math_factor(p):
    '''math_factor : terminal_num
                   | terminal_lparen math_expression terminal_rparen
    '''
    if len(p) == 2:
        p[0] = p[1] #terminal_num
    elif len(p) == 4:
        p[0] = (
                'prec',
                #p[1], # LPAREN 
                p[2], # math_expression
                #p[3]  # RPAREN
               )

########## Gramática -> Operações de Atribuição ##########
def p_assign_expression(p):
    '''assign_expression : terminal_name PLUS_ONE 
                         | terminal_name MINUS_ONE 
                         | terminal_name PLUS_EQUAL terminal_num 
                         | terminal_name MINUS_EQUAL terminal_num 
                         | terminal_name TIMES_EQUAL terminal_num 
                         | terminal_name DIVIDE_EQUAL terminal_num 
                         | terminal_name EQUAL assign_term 
                         | terminal_name EQUAL term_num_char 
    '''
    if len(p) == 3:
        p[0] = (
                f'{p[2][1]}=', # PLUS_ONE/MINUS_ONE 
                p[1], # terminal_name
                1
               )
    elif len(p) == 4:
        p[0] = (
                p[2], # EQUAL/PLUS_EQUAL/MINUS_EQUAL/TIMES_EQUAL/DIVIDE_EQUAL
                p[1], # terminal_name 
                p[3]  #assign_term/terminal_num
               )

def p_assign_term(p):
    '''assign_term : math_expression 
    '''
    p[0] = p[1]
    
    
########## Gramática -> Operações de Lógica ##########
def p_logic_expression(p):
    '''logic_expression : term_num_char EQUAL_TO term_num_char 
		                | term_num_char  NOT_EQUAL term_num_char  
                        | terminal_num LESS_THAN terminal_num 
                        | terminal_num GREATER_THAN terminal_num 
                        | terminal_num LESS_EQUAL terminal_num 
                        | terminal_num GREATER_EQUAL terminal_num 
    '''
    p[0] = (
            p[2], # EQUAL_TO/NOT_EQUAL/LESS_THAN/GREATER_THAN/LESS_EQUAL/GREATER_EQUAL
            p[1], # term_num_char
            p[3]  # term_num_char
           )
    

########## Gramática -> Bloco de Execução ##########
def p_block_expression(p):
    '''block_expression : terminal_lparen logic_expression terminal_rparen block_term
    '''
    p[0] = (
            #p[1], # LPAREN
            p[2], # logic_expression
            #p[3]  # terminal_rparen
            p[4]  # block_term
           )
    
def p_block_term(p):
    '''block_term : terminal_lcbracket math_expression terminal_semicolon terminal_rcbracket
    '''
    p[0] = (
            #p[1], # LCBRACKET
            p[2] # math_expression
            #p[3] # terminal_semicolon
            #p[4]  # RCBRACKET
           )

########## Gramática -> Condicional ##########
def p_cond_expression(p):
    '''cond_expression : IF block_expression cond_term 
    '''
    p[0] = (
            p[1], # IF
            p[2], # block_expression
            p[3]  # cond_term
           )
    
def p_cond_term(p):
    '''cond_term : ELSE block_term
                 | empty
    '''
    if len(p) == 3:
        p[0] = (
                p[1], # ELSE
                p[2] # block_term
               )
    else:
        pass
        
########## Gramática -> Loop ##########
def p_loop_expression(p):
    '''loop_expression : WHILE block_expression
    '''
    p[0] = (
            p[1], # WHILE
            p[2]  # block_expression
           )

def p_error(p):
    print(f'Syntax error at {p.value!r}')

# Build the parser
parser = yacc(debug=True)

# Parse an expression
import os

with open('src/tests.txt') as file:
    for line in file:
        lineRead = line.strip()
        if lineRead: 
            result = parser.parse(lineRead)
            print(result)
