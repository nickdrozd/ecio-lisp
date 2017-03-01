from keywords import *
from reg import fetch, EXPR
from labels import *
# from instr import goto
import instr

def eval_exp():
    expr = fetch(EXPR)
    # expr = transform_macros(expr)
    eval_label = get_eval_label(expr)
    instr.goto(eval_label)

def get_eval_label(expr):
    if is_var(expr):
        return EVAL_VAR

    if is_num(expr):
        return EVAL_NUM

    # else
    tag, *_ = expr

    keyword_groups = {
        DEFINE_KEYS : EVAL_DEF,
        ASS_KEYS : EVAL_ASS,
        LAMBDA_KEYS : EVAL_LAMBDA,
        IF_KEYS : EVAL_IF,
        BEGIN_KEYS : EVAL_BEGIN,
        QUOTE_KEYS : EVAL_QUOTE
    }

    for group in keyword_groups:
        if tag in group:
            return keyword_groups[group]

    # default
    return EVAL_FUNC

def is_num(exp):
    try:
        return isinstance(int(exp), int)
    except (ValueError, TypeError):
        return False

def is_var(exp):
    return isinstance(exp, str)

def expr_is_simple():
    expr = fetch(EXPR)
    return is_num(expr) or is_var(expr)
