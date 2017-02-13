from keywords import *
from reg import fetch, EXPR
from labels import *
# from instr import goto
import instr

def eval_exp():
    expr = fetch(EXPR)
    # expr = transformMacros(expr)
    eval_label = get_eval_label(expr)
    instr.goto(eval_label)

def get_eval_label(expr):
    if isVar(expr):
        return EVAL_VAR

    if isNum(expr):
        return EVAL_NUM

    # else
    tag, *_ = expr

    keyword_groups = {
        define_keys : EVAL_DEF,
        # ass_keys : EVAL_ASS,
        lambda_keys : EVAL_LAMBDA,
        if_keys : EVAL_IF,
        # begin_keys : EVAL_BEGIN,
        quote_keys : EVAL_QUOTE
    }

    for group in keyword_groups:
        if tag in group:
            return keyword_groups[group]

    # default
    return EVAL_FUNC

def isNum(exp):
    try:
        return type(int(exp)) == int
    except:
        return False

def isVar(exp):
    return type(exp) == str
