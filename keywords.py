'''
    It would be nice if this module didn't need to import anything,
    since it defines (part of) the syntax of the language, and that
    and that seems like something that should be completely abstract.
    But macros make it possible to alter the syntax at run-time,
    meaning that keyword dispatch has to be cognizant of the mutable
    state of the machine!

    ###

    Is it "cheating" to include keyword_dispatch? It would be trivial
    to unroll it into a big ugly list of branch-if statements, so it
    doesn't really add any expressive power. Still, to mollify the
    skeptic, keyword_dispatch can be imagined as a piece of specialized
    hardware. Further, it can be stipulated that its use is relatively
    expensive, thereby gaining some advantage for analyze-interpretation.
'''

from env import is_macro

from stats import dispatch_stats


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


@dispatch_stats
def keyword_dispatch(expr):
    if is_var(expr):
        return 'EVAL_VAR'

    if is_num(expr):
        return 'EVAL_NUM'

    # else
    tag, *_ = expr

    keyword_groups = {
        DEFINE_KEYS: 'EVAL_DEF',
        ASS_KEYS: 'EVAL_ASS',
        LAMBDA_KEYS: 'EVAL_LAMBDA',
        IF_KEYS: 'EVAL_IF',
        BEGIN_KEYS: 'EVAL_BEGIN',
        QUOTE_KEYS: 'EVAL_QUOTE',
        QUASIQUOTE_KEYS: 'EVAL_QUASIQUOTE',
        DEFMACRO_KEYS: 'EVAL_DEFMACRO',
    }

    for group in keyword_groups:
        if tag in group:
            return keyword_groups[group]

    if is_macro(tag):
        return 'EVAL_MACRO'

    # default
    return 'EVAL_FUNC'


def is_num(exp):
    try:
        return isinstance(int(exp), int)
    except (ValueError, TypeError):
        return False


def is_var(exp):
    return isinstance(exp, str)


def is_simple(expr):
    return is_num(expr) or is_var(expr) or expr == []


def has_tag(expr, tag_keys):
    try:
        return expr[0] in tag_keys
    except (TypeError, IndexError):
        return False


def is_unquoted(expr):
    return has_tag(expr, UNQUOTE_KEYS)


def is_splice(expr):
    return has_tag(expr, SPLICE_KEYS)
