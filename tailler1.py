import sys

operators = {
    "+" : "tk_mas",
    "-" : "tk_menos",
    "*" : "tk_mult",
    "/" : "tk_div",
    "%" : "tk_mod",
    "=" : "tk_asig",
    "<" : "tk_menor",
    ">" : "tk_mayor",
    "!" : "tk_neg",
    ":" : "tk_dosp",
    ";" : "tk_pyc",
    "," : "tk_coma",
    "." : "tk_punto",
    "(" : "tk_par_izq",
    ")" : "tk_par_der",
    "<=" : "tk_menor_igual",
    ">=" : "tk_mayor_igual",
    "==" : "tk_igual",
    "&&" : "tk_y",
    "||" : "tk_o",
    "!=" : "tk_dif",
}

keywords = [
    "funcion_principal",
    "fin_principal",
    "leer",
    "imprimir",
    "booleano",
    "caracter",
    "entero",
    "real",
    "cadena",
    "si",
    "entonces",
    "fin_si",
    "si_no",
    "mientras",
    "hacer",
    "fin_mientras",
    "para",
    "fin_para",
    "seleccionar",
    "entre",
    "caso",
    "romper",
    "defecto",
    "fin_seleccionar",
    "estructura",
    "fin_estructura",
    "funcion",
    "fin_funcion",
    "retornar",
    "falso",
    "verdadero"
]

act_ch = ' '
act_col = 0
act_line = 1
input_file = None
line = ""

def print_with_syntax(key, value, y, x):
    if (value):
        print("<" + key + "," + value + "," + str(y) + "," + str(x) + ">")
    else:
        print("<" + key + "," + str(y) + "," + str(x) + ">")
    return True

def isError(y, x):
    if (ord(act_ch) < 0 or ord(act_ch) > 127):
        print(">>> Error lexico (linea: " + str(y) + ", posicion: " + str(x) + ")")
        exit(1)

def get_next_char(isComment=False):
    global act_ch, act_col, act_line, line

    act_ch = line[act_col]
    act_col += 1

    if not isComment:
        isError(act_line, act_col)
    if (act_ch == '\n'):
        act_line += 1
        act_col = 0
        try:
            line = input()
            line += '\n'
        except:
            act_ch = ""
    return (act_ch)

def check_div_or_cmt(line, col):
    get_next_char()

    # Check division
    if act_ch != '*' and act_ch != '/':
        return operators['/'], None, line, col


    # Check Simple comment
    if act_ch == '/':
        while get_next_char(True) != '\n' and len(act_ch) != 0:
            continue
        if len(act_ch) == 0:
            return None
        get_next_char()
        return parse_next_char()

    # Check multiple comments
    while (True):
        if act_ch == '*':
            if get_next_char() == '/':
                get_next_char()
                return parse_next_char()
        if len(act_ch) == 0:
            #ERROR
            pass
        get_next_char(True)

def check_next_char(isThis, ifTrue, ifFalse, line, col):
    if get_next_char() == isThis:
        get_next_char()
        return operators[ifTrue], None, line, col
    if ifFalse == None:
        pass
        # Error
    return operators[ifFalse], None, line, col

def check_char(line, col):
    res = get_next_char()
    if get_next_char() != "'":
        #Error
        pass

    get_next_char()
    return "tk_caracter", "'" + res + "'", line, col

def check_string(line, col):
    res = '"'

    while get_next_char() != '"':
        if len(act_ch) == 0:
            #Error
            pass
        if act_ch == '\n':
            #Error
            pass
        res += act_ch

    res += act_ch
    get_next_char()
    return "tk_cadena", res, line, col

def check_int_float(line, col):
    res = ""

    while act_ch.isdigit():
        res += act_ch
        get_next_char()

    if act_ch != '.':
        return "tk_entero", res, line, col

    res += act_ch
    get_next_char()
    while act_ch.isdigit():
        res += act_ch
        get_next_char()
    return "tk_real", res, line, col

def check_keywords(gline, col):
    res = ""
    while act_ch.isalnum() or act_ch == '_':
        res += act_ch
        get_next_char()

    if res in keywords:
        return res, None, gline, col
    return "id", res, gline, col


def parse_next_char():
    while act_ch.isspace():
        get_next_char()

    tmp_line = act_line
    tmp_col = act_col

    # Check end
    if len(act_ch) == 0 :
        return (None)

    # Check Comment
    if act_ch == '/' : return check_div_or_cmt(tmp_line, tmp_col)

    # Check Double Operators
    if act_ch == '<' : return check_next_char('=', '<=', '<', tmp_line, tmp_col)
    if act_ch == '>' : return check_next_char('=', '>=', '>', tmp_line, tmp_col)
    if act_ch == '=' : return check_next_char('=', '==', '=', tmp_line, tmp_col)
    if act_ch == '!' : return check_next_char('=', '!=', None, tmp_line, tmp_col)
    if act_ch == '&' : return check_next_char('&', '&&', None, tmp_line, tmp_col)
    if act_ch == '|' : return check_next_char('|', '||', None, tmp_line, tmp_col)

    # Check Char
    if act_ch == "'" : return check_char(tmp_line, tmp_col)

    # Check String
    if act_ch == '"' : return check_string(tmp_line, tmp_col)

    #Check Simple Operators
    if act_ch in operators:
        ret = operators[act_ch]
        get_next_char()
        return ret, None, tmp_line, tmp_col

    # Check int/float
    if act_ch.isdigit() : return check_int_float(tmp_line, tmp_col)

    #Check keywords
    return check_keywords(tmp_line, tmp_col)
    #Manque ERROR, bool ?

try:
    line = input()
    line += '\n'
except:
    exit(1)

while (True):
    ret = parse_next_char()
    if (ret == None):
        break

    key = ret[0]
    value = ret[1]
    aline = ret[2]
    col = ret[3]
    print_with_syntax(key, value, aline, col)
