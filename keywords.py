DEFINE_KEYS = 'define', 'def'

ASS_KEYS = 'set!', 'ass!'

LAMBDA_KEYS = 'lambda', 'λ', 'fun'

IF_KEYS = 'if',

BEGIN_KEYS = 'begin', 'progn'

QUOTE_KEYS = 'quote',

QUASIQUOTE_KEYS = 'quasiquote', 'qsq'
UNQUOTE_KEYS = 'unquote', 'unq'
SPLICE_KEYS = 'splice', 'spl'

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

###

def has_tag(expr, tag_keys):
    try:
        return expr[0] in tag_keys
    except TypeError:
        return False

def is_unquoted(expr):
    return has_tag(expr, UNQUOTE_KEYS)

def is_splice(expr):
    return has_tag(expr, SPLICE_KEYS)
