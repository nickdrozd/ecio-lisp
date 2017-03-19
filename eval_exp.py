# pylint: disable=wildcard-import,unused-wildcard-import
from reg import fetch, EXPR
from instr import goto

from keywords import *
from env import is_macro


def eval_exp():
    expr = fetch(EXPR)
    # expr = transform_macros(expr)
    eval_label = get_eval_label(expr)
    goto(eval_label)

def get_eval_label(expr):
    if is_var(expr):
        return 'EVAL_VAR'

    if is_num(expr):
        return 'EVAL_NUM'

    # else
    tag, *_ = expr

    keyword_groups = {
        DEFINE_KEYS : 'EVAL_DEF',
        ASS_KEYS : 'EVAL_ASS',
        LAMBDA_KEYS : 'EVAL_LAMBDA',
        IF_KEYS : 'EVAL_IF',
        BEGIN_KEYS : 'EVAL_BEGIN',
        QUOTE_KEYS : 'EVAL_QUOTE',
        QUASIQUOTE_KEYS : 'EVAL_QUASIQUOTE',
        DEFMACRO_KEYS : 'EVAL_DEFMACRO',
    }

    for group in keyword_groups:
        if tag in group:
            return keyword_groups[group]

    if is_macro(tag):
        return 'EVAL_MACRO'

    # default
    return 'EVAL_FUNC'
