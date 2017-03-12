DEFINE_KEYS = 'define', 'def'

ASS_KEYS = 'set!', 'ass!'

LAMBDA_KEYS = 'lambda', 'λ', 'fun'

IF_KEYS = 'if',

BEGIN_KEYS = 'begin', 'progn'

QUOTE_KEYS = 'quote',

QUASIQUOTE_KEYS = 'quasiquote', 'qsq'

UNQUOTE_KEYS = 'unquote', 'unq'

DEFMACRO_KEYS = 'defmacro', 'defmac'

###

def is_num(exp):
    try:
        return isinstance(int(exp), int)
    except (ValueError, TypeError):
        return False

def is_var(exp):
    return isinstance(exp, str)

def is_simple(expr):
    return is_num(expr) or is_var(expr)

def is_unquoted(expr):
    try:
        return expr[0] in UNQUOTE_KEYS
    except TypeError:
        return False
