from reg import EXPR, ENV, FUNC, ARGL, CONT, VAL, UNEV
from reg import assign, fetch, adjoin_arg
from stack import save, restore
from env import lookup_expr, is_unbound,\
    define_var, define_macro, set_var, extend_env
from instr import goto, goto_continue, goto_eval, set_continue
from prim import is_primitive_func, apply_primitive_func
from keywords import is_simple, is_unquoted, is_splice

# pylint: disable=wildcard-import,unused-wildcard-import
from labels import *


###

def eval_num():
    assign(VAL, fetch(EXPR))
    goto_continue()

def eval_var():
    assign(VAL, lookup_expr())

    if is_unbound(VAL):
        goto(UNBOUND)
        return

    goto_continue()

def unbound():
    goto(DONE)

def eval_quote():
    _, text = fetch(EXPR)
    assign(VAL, text)
    goto_continue()

###

def eval_lambda():
    _, params, *body = fetch(EXPR)
    assign(UNEV, params)
    assign(EXPR, body)
    assign(VAL, [
        fetch(ENV),
        fetch(UNEV),
        fetch(EXPR),
    ])
    goto_continue()

###

def eval_def():
    _, var, val = fetch(EXPR)
    assign(UNEV, var)
    assign(EXPR, val)
    save(UNEV)
    save(ENV)
    save(CONT)
    set_continue(DID_DEF_VAL)
    goto_eval()

def did_def_val():
    restore(CONT)
    restore(ENV)
    restore(UNEV)
    define_var()
    goto_continue()

###

def eval_ass():
    _, var, val = fetch(EXPR)
    assign(UNEV, var)
    assign(EXPR, val)
    save(UNEV)
    save(ENV)
    save(CONT)
    set_continue(DID_ASS_VAL)
    goto_eval()

def did_ass_val():
    restore(CONT)
    restore(ENV)
    restore(UNEV)
    set_var()
    goto_continue()

###

def eval_if():
    save(ENV)
    save(CONT)
    save(EXPR)
    _, condition, _, _ = fetch(EXPR)
    assign(EXPR, condition)
    set_continue(IF_DECIDE)
    goto_eval()

def if_decide():
    restore(EXPR)
    restore(CONT)
    restore(ENV)
    if fetch(VAL): # or if isTrue(fetch(VAL))
        goto(IF_THEN)
    else:
        goto(IF_ELSE)

def if_then():
    _, _, consequence, _ = fetch(EXPR)
    assign(EXPR, consequence)
    goto_eval()

def if_else():
    _, _, _, alternative = fetch(EXPR)
    assign(EXPR, alternative)
    goto_eval()

###

def eval_begin():
    _, *body = fetch(EXPR)
    assign(UNEV, body)
    save(CONT)
    goto(EVAL_SEQ)

###

def eval_func():
    save(CONT)

    goto(MAP_EVAL)

def map_eval():
    func, *args = fetch(EXPR)

    assign(EXPR, func)
    assign(UNEV, args)

    if is_simple(func):
        goto(SIMPLE_FUNC)
        return

    save(ENV)
    save(UNEV)

    set_continue(DID_COMPOUND_FUNC)

    goto_eval()

def simple_func():
    set_continue(DID_FUNC)

    goto_eval()

def did_compound_func():
    restore(UNEV)
    restore(ENV)

    goto(DID_FUNC)

def did_func():
    result = fetch(VAL)

    assign(ARGL, [result])

    if not fetch(UNEV):
        goto(APPLY_FUNC)
        return

    goto(ARG_LOOP)

def arg_loop():
    first, *rest = fetch(UNEV)

    assign(EXPR, first)
    assign(UNEV, rest)

    if is_simple(first):
        goto(SIMPLE_ARG)
        return

    goto(COMPOUND_ARG)

def simple_arg():
    set_continue(DID_SIMPLE_ARG)

    goto_eval()

def did_simple_arg():
    adjoin_arg()

    if not fetch(UNEV):
        goto(APPLY_FUNC)
        return

    goto(ARG_LOOP)

def compound_arg():
    save(ARGL)

    # 'evlis' tail recursion
    if not fetch(UNEV): # if no_remaining_args():
        goto(LAST_ARG)
        return

    save(ENV)
    save(UNEV)

    set_continue(ACC_ARG)
    goto_eval()

def acc_arg():
    restore(UNEV)
    restore(ENV)
    restore(ARGL)

    adjoin_arg()

    goto(ARG_LOOP)

def last_arg():
    set_continue(DID_LAST_ARG)

    goto_eval()

def did_last_arg():
    restore(ARGL)

    adjoin_arg()

    goto(APPLY_FUNC)

###

def apply_func():
    func, *args = fetch(ARGL)

    assign(FUNC, func)
    assign(ARGL, args)

    if is_primitive_func():
        goto(APPLY_PRIMITIVE)
    # if is_compound_func():
    else:
        goto(APPLY_COMPOUND)

def apply_primitive():
    apply_primitive_func()

    restore(CONT)

    goto_continue()

def apply_compound():
    # this needs to agree with eval_lambda
    env, params, body = fetch(FUNC)

    assign(UNEV, params)
    assign(ENV, env)
    extend_env()

    assign(UNEV, body)

    goto(EVAL_SEQ)

###

def eval_seq():
    first, *rest = fetch(UNEV)

    assign(EXPR, first)

    # if last_exp...
    if not rest:
        goto(EVAL_SEQ_LAST)
        return

    assign(UNEV, rest)

    save(UNEV)
    save(ENV)

    set_continue(EVAL_SEQ_CONT)

    goto_eval()

def eval_seq_cont():
    restore(ENV)
    restore(UNEV)

    goto(EVAL_SEQ)

def eval_seq_last():
    restore(CONT)

    goto_eval()

###

def alt_eval_seq():
    exps = fetch(UNEV)

    # if no_exps...
    if not exps:
        goto(ALT_EVAL_SEQ_END)
        return

    first, *rest = fetch(UNEV)

    assign(EXPR, first)
    assign(UNEV, rest)

    save(UNEV)
    save(ENV)

    set_continue(ALT_EVAL_SEQ_CONT)

    goto_eval()

def alt_eval_seq_cont():
    restore(ENV)
    restore(UNEV)

    goto(ALT_EVAL_SEQ)

def alt_eval_seq_end():
    restore(CONT)
    goto_continue()

###

def eval_quasiquote():
    _, text = fetch(EXPR)

    if is_simple(text):
        goto(EVAL_QUOTE)
        return

    assign(EXPR, text)
    assign(ARGL, ['list'])

    save(CONT)
    set_continue(DID_QUASIQUOTE)

    goto(QSQ_LOOP)

def qsq_loop():
    first, *rest = fetch(EXPR)

    assign(UNEV, rest)
    assign(EXPR, first)

    if is_simple(first):
        goto(QSQ_SIMPLE)
        return

    if is_unquoted(first):
        goto(QSQ_UNQUOTED)
        return

    if is_splice(first):
        goto(QSQ_SPLICE)
        return

    goto(QSQ_SUBLIST)

def qsq_simple():
    assign(VAL, ['quote', fetch(EXPR)])

    adjoin_arg()

    goto(QSQ_CHECK_REST)

def qsq_unquoted():
    _, text = fetch(EXPR)

    assign(VAL, text)

    adjoin_arg()

    goto(QSQ_CHECK_REST)

def qsq_splice():
    _, text = fetch(EXPR)

    assign(EXPR, text)

    save(ARGL)
    save(UNEV)
    save(CONT)

    set_continue(QSQ_DID_SPLICE)

    goto_eval()

def qsq_did_splice():
    restore(CONT)
    restore(UNEV)
    restore(ARGL)

    assign(ARGL, fetch(ARGL) + fetch(VAL))

    goto(QSQ_CHECK_REST)

def qsq_sublist():
    save(ARGL)
    save(UNEV)
    save(CONT)

    assign(ARGL, ['list'])

    set_continue(DID_QSQ_SUBLIST)

    goto(QSQ_LOOP)

def did_qsq_sublist():
    assign(VAL, fetch(ARGL))

    restore(CONT)
    restore(UNEV)
    restore(ARGL)

    adjoin_arg()

    goto(QSQ_CHECK_REST)

def qsq_check_rest():
    if not fetch(UNEV):
        goto_continue()
        return

    assign(EXPR, fetch(UNEV))

    goto(QSQ_LOOP)

def did_quasiquote():
    restore(CONT)

    assign(EXPR, fetch(ARGL))

    goto_eval()

###

def eval_defmacro():
    define_macro()
    goto_continue()

###

def eval_macro():
    macro, *args = fetch(EXPR)

    assign(ARGL, args)
    assign(EXPR, macro)

    assign(EXPR, lookup_expr())

    _, params, macro_body = fetch(EXPR)

    assign(UNEV, params)
    extend_env()

    assign(EXPR, macro_body)

    save(ENV)
    save(CONT)

    set_continue(DID_MACRO)
    goto_eval()

def did_macro():
    restore(CONT)
    restore(ENV)

    assign(EXPR, fetch(VAL))
    goto_eval()
