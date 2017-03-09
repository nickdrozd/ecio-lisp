# pylint: disable=wildcard-import,unused-wildcard-import
from keywords import *
from reg import fetch, EXPR
from labels import EVAL_VAR, EVAL_NUM, EVAL_DEF,\
                   EVAL_ASS, EVAL_LAMBDA, EVAL_IF,\
                   EVAL_QUOTE, EVAL_QUASIQUOTE,\
                   EVAL_BEGIN, EVAL_FUNC
import instr
# from instr import goto

def eval_exp():
    expr = fetch(EXPR)
    # expr = transform_macros(expr)
    eval_label = get_eval_label(expr)
    instr.goto(eval_label)
    # goto(eval_label)

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
        QUOTE_KEYS : EVAL_QUOTE,
        QUASIQUOTE_KEYS : EVAL_QUASIQUOTE,
    }

    for group in keyword_groups:
        if tag in group:
            return keyword_groups[group]

    # default
    return EVAL_FUNC
