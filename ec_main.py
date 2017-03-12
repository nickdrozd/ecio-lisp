'''
    TODO:
        * figure out import mess
'''

from reg import EXPR, ENV, FUNC, ARGL, CONT, VAL, UNEV
from reg import assign, fetch, set_empty_arglist, adjoin_arg
from stack import save, restore
from env import lookup, is_unbound,\
    define_var, define_macro, set_var, extend_env
import instr
from prim import is_primitive_func, apply_primitive_func
from keywords import is_simple, is_unquoted

# pylint: disable=wildcard-import,unused-wildcard-import
from labels import *


###

def eval_num():
    assign(VAL, fetch(EXPR))
    instr.goto_continue()

def eval_var():
    assign(VAL, lookup(EXPR))

    if is_unbound(VAL):
        instr.goto(UNBOUND)
        return

    instr.goto_continue()

def unbound():
    print('UNBOUND')
    instr.goto(DONE)

def eval_quote():
    _, text = fetch(EXPR)
    assign(VAL, text)
    instr.goto_continue()

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
    instr.goto_continue()

###

def eval_def():
    _, var, val = fetch(EXPR)
    assign(UNEV, var)
    assign(EXPR, val)
    save(UNEV)
    save(ENV)
    save(CONT)
    instr.set_continue(DID_DEF_VAL)
    instr.goto_eval()

def did_def_val():
    restore(CONT)
    restore(ENV)
    restore(UNEV)
    define_var()
    instr.goto_continue()

###

def eval_ass():
    _, var, val = fetch(EXPR)
    assign(UNEV, var)
    assign(EXPR, val)
    save(UNEV)
    save(ENV)
    save(CONT)
    instr.set_continue(DID_ASS_VAL)
    instr.goto_eval()

def did_ass_val():
    restore(CONT)
    restore(ENV)
    restore(UNEV)
    set_var()
    instr.goto_continue()

###

def eval_if():
    save(ENV)
    save(CONT)
    save(EXPR)
    _, condition, _, _ = fetch(EXPR)
    assign(EXPR, condition)
    instr.set_continue(IF_DECIDE)
    instr.goto_eval()

def if_decide():
    restore(EXPR)
    restore(CONT)
    restore(ENV)
    if fetch(VAL): # or if isTrue(fetch(VAL))
        instr.goto(IF_THEN)
    else:
        instr.goto(IF_ELSE)

def if_then():
    _, _, consequence, _ = fetch(EXPR)
    assign(EXPR, consequence)
    instr.goto_eval()

def if_else():
    _, _, _, alternative = fetch(EXPR)
    assign(EXPR, alternative)
    instr.goto_eval()

###

def eval_begin():
    _, *body = fetch(EXPR)
    assign(UNEV, body)
    save(CONT)
    instr.goto(EVAL_SEQ)

###

def eval_func():
    save(CONT)

    func, *args = fetch(EXPR)
    assign(EXPR, func)
    assign(UNEV, args)

    if is_simple(func):
        instr.goto(SIMPLE_FUNC)
        return

    save(ENV)
    save(UNEV)

    instr.set_continue(DID_FUNC)
    instr.goto_eval()

def did_func():
    restore(UNEV) # args
    restore(ENV)

    assign(FUNC, fetch(VAL))

    # cont is still/already saved
    instr.goto(CHECK_NO_ARGS)

def simple_func():
    assign(FUNC, lookup(EXPR))

    if is_unbound(FUNC):
        instr.goto(UNBOUND)
        return

    instr.goto(CHECK_NO_ARGS)

def check_no_args():
    set_empty_arglist()

    if not fetch(UNEV): # if no_args():
        instr.goto(APPLY_FUNC)
        return

    # if noCompoundArgs(): ...
    save(FUNC)
    instr.goto(ARG_LOOP)

# unev has args, func and cont are on the stack #

def arg_loop():
    first, *rest = fetch(UNEV)

    assign(EXPR, first)
    assign(UNEV, rest)

    if is_simple(first):
        instr.goto(SIMPLE_ARG)
        return

    instr.goto(COMPOUND_ARG)

def simple_arg():
    instr.set_continue(DID_SIMPLE_ARG)
    instr.goto_eval()

def did_simple_arg():
    adjoin_arg()
    if not fetch(UNEV):
        instr.goto(RESTORE_FUNC)
        return
    instr.goto(ARG_LOOP)

def compound_arg():
    save(ARGL)

    if not fetch(UNEV): # if no_remaining_args():
        instr.goto(LAST_ARG)
        return

    save(ENV)
    save(UNEV)

    instr.set_continue(ACC_ARG)
    instr.goto_eval()

def acc_arg():
    restore(UNEV)
    restore(ENV)

    restore(ARGL)
    adjoin_arg()

    instr.goto(ARG_LOOP)

def last_arg():
    instr.set_continue(DID_LAST_ARG)
    instr.goto_eval()

def did_last_arg():
    restore(ARGL)
    adjoin_arg()

    instr.goto(RESTORE_FUNC)

def restore_func():
    restore(FUNC)
    instr.goto(APPLY_FUNC)

###

def apply_func():
    if is_primitive_func():
        instr.goto(APPLY_PRIMITIVE)
    # if is_compound_func():
    else:
        instr.goto(APPLY_COMPOUND)

def apply_primitive():
    apply_primitive_func()

    restore(CONT)

    instr.goto_continue()

def apply_compound():
    # this needs to agree with eval_lambda
    env, params, body = fetch(FUNC)

    assign(UNEV, params)
    assign(ENV, env)
    extend_env()

    assign(UNEV, body)

    instr.goto(EVAL_SEQ)

###

def eval_seq():
    first, *rest = fetch(UNEV)

    assign(EXPR, first)

    # if last_exp...
    if not rest:
        instr.goto(EVAL_SEQ_LAST)
        return

    assign(UNEV, rest)

    save(UNEV)
    save(ENV)

    instr.set_continue(EVAL_SEQ_CONT)

    instr.goto_eval()

def eval_seq_cont():
    restore(ENV)
    restore(UNEV)

    instr.goto(EVAL_SEQ)

def eval_seq_last():
    restore(CONT)

    instr.goto_eval()

###

def alt_eval_seq():
    exps = fetch(UNEV)

    # if no_exps...
    if not exps:
        instr.goto(ALT_EVAL_SEQ_END)
        return

    first, *rest = fetch(UNEV)

    assign(EXPR, first)
    assign(UNEV, rest)

    save(UNEV)
    save(ENV)

    instr.set_continue(ALT_EVAL_SEQ_CONT)

    instr.goto_eval()

def alt_eval_seq_cont():
    restore(ENV)
    restore(UNEV)

    instr.goto(ALT_EVAL_SEQ)

def alt_eval_seq_end():
    restore(CONT)
    instr.goto_continue()

###

def eval_quasiquote():
    _, text = fetch(EXPR)

    if is_simple(text):
        instr.goto(EVAL_QUOTE)
        return

    assign(EXPR, text)
    assign(ARGL, ['list'])

    save(CONT)
    instr.set_continue(DID_QUASIQUOTE)

    instr.goto(QSQ_LOOP)

def qsq_loop():
    first, *rest = fetch(EXPR)

    assign(UNEV, rest)
    assign(EXPR, first)

    if is_simple(first):
        instr.goto(QSQ_SIMPLE)
        return

    if is_unquoted(first):
        instr.goto(QSQ_UNQUOTED)
        return

    instr.goto(QSQ_SUBLIST)

def qsq_simple():
    # distinguish numbers and variables?

    assign(VAL, ['quote', fetch(EXPR)])

    adjoin_arg()

    instr.goto(QSQ_CHECK_REST)

def qsq_unquoted():
    _, text = fetch(EXPR)

    assign(VAL, text)

    adjoin_arg()

    instr.goto(QSQ_CHECK_REST)

def qsq_sublist():
    save(ARGL)
    save(UNEV)
    save(CONT)

    assign(ARGL, ['list'])

    instr.set_continue(DID_QSQ_SUBLIST)

    instr.goto(QSQ_LOOP)

def did_qsq_sublist():
    assign(VAL, fetch(ARGL))

    restore(CONT)
    restore(UNEV)
    restore(ARGL)

    adjoin_arg()

    instr.goto(QSQ_CHECK_REST)

def qsq_check_rest():
    if not fetch(UNEV):
        instr.goto_continue()
        return

    assign(EXPR, fetch(UNEV))

    instr.goto(QSQ_LOOP)

def did_quasiquote():
    restore(CONT)

    assign(EXPR, fetch(ARGL))

    instr.goto_eval()

###

def eval_defmacro():
    define_macro()
    instr.goto_continue()

###

def eval_macro():
    macro, *args = fetch(EXPR)

    assign(EXPR, macro)
    assign(EXPR, lookup(EXPR))

    _, params, macro_body = fetch(EXPR)

    assign(UNEV, params)
    assign(ARGL, args)
    extend_env()

    assign(EXPR, macro_body)

    save(ENV)
    save(CONT)

    instr.set_continue(DID_MACRO)
    instr.goto_eval()

def did_macro():
    restore(CONT)
    restore(ENV)

    assign(EXPR, fetch(VAL))
    instr.goto_eval()
