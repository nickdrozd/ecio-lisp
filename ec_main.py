from reg import EXPR, ENV, FUNC, ARGL, CONT, VAL, UNEV
from reg import assign, fetch, adjoin_arg
from stack import save, restore
from env import lookup_expr, is_unbound,\
    define_var, define_macro, set_var, extend_env
from instr import goto, goto_continue, set_continue
from prim import is_primitive_func, apply_primitive_func
from keywords import keyword_dispatch, is_simple, is_unquoted, is_splice

# pylint: disable=invalid-name

###

def EVAL_EXPR():
    expr = fetch(EXPR)
    eval_label = keyword_dispatch(expr)
    goto(eval_label)

###

def EVAL_NUM():
    assign(VAL, fetch(EXPR))
    goto_continue()

def EVAL_VAR():
    assign(VAL, lookup_expr())

    if is_unbound(VAL):
        goto(UNBOUND)
        return

    goto_continue()

def UNBOUND():
    goto('DONE')

def EVAL_QUOTE():
    _, text = fetch(EXPR)
    assign(VAL, text)
    goto_continue()

###

def EVAL_LAMBDA():
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

def EVAL_DEF():
    _, var, val = fetch(EXPR)
    assign(UNEV, var)
    assign(EXPR, val)
    save(UNEV)
    save(ENV)
    save(CONT)
    set_continue(DID_DEF_VAL)
    goto(EVAL_EXPR)

def DID_DEF_VAL():
    restore(CONT)
    restore(ENV)
    restore(UNEV)
    define_var()
    goto_continue()

###

def EVAL_ASS():
    _, var, val = fetch(EXPR)
    assign(UNEV, var)
    assign(EXPR, val)
    save(UNEV)
    save(ENV)
    save(CONT)
    set_continue(DID_ASS_VAL)
    goto(EVAL_EXPR)

def DID_ASS_VAL():
    restore(CONT)
    restore(ENV)
    restore(UNEV)
    set_var()
    goto_continue()

###

def EVAL_IF():
    save(ENV)
    save(CONT)
    save(EXPR)
    _, condition, _, _ = fetch(EXPR)
    assign(EXPR, condition)
    set_continue(IF_DECIDE)
    goto(EVAL_EXPR)

def IF_DECIDE():
    restore(EXPR)
    restore(CONT)
    restore(ENV)
    if fetch(VAL):  # or if isTrue(fetch(VAL))
        goto(IF_THEN)
    else:
        goto(IF_ELSE)

def IF_THEN():
    _, _, consequence, _ = fetch(EXPR)
    assign(EXPR, consequence)
    goto(EVAL_EXPR)

def IF_ELSE():
    _, _, _, alternative = fetch(EXPR)
    assign(EXPR, alternative)
    goto(EVAL_EXPR)

###

def EVAL_BEGIN():
    _, *body = fetch(EXPR)
    assign(UNEV, body)
    save(CONT)
    goto(EVAL_SEQ)

###

def EVAL_FUNC():
    save(CONT)

    goto(MAP_EVAL)

def MAP_EVAL():
    func, *args = fetch(EXPR)

    assign(EXPR, func)
    assign(UNEV, args)

    if is_simple(func):
        goto(SIMPLE_FUNC)
        return

    save(ENV)
    save(UNEV)

    set_continue(DID_COMPOUND_FUNC)

    goto(EVAL_EXPR)

def SIMPLE_FUNC():
    set_continue(DID_FUNC)

    goto(EVAL_EXPR)

def DID_COMPOUND_FUNC():
    restore(UNEV)
    restore(ENV)

    goto(DID_FUNC)

def DID_FUNC():
    result = fetch(VAL)

    assign(ARGL, [result])

    if not fetch(UNEV):
        goto(APPLY_FUNC)
        return

    goto(ARG_LOOP)

def ARG_LOOP():
    first, *rest = fetch(UNEV)

    assign(EXPR, first)
    assign(UNEV, rest)

    if is_simple(first):
        goto(SIMPLE_ARG)
        return

    goto(COMPOUND_ARG)

def SIMPLE_ARG():
    set_continue(DID_SIMPLE_ARG)

    goto(EVAL_EXPR)

def DID_SIMPLE_ARG():
    adjoin_arg()

    if not fetch(UNEV):
        goto(APPLY_FUNC)
        return

    goto(ARG_LOOP)

def COMPOUND_ARG():
    save(ARGL)

    # 'evlis' tail recursion
    if not fetch(UNEV):  # if no_remaining_args():
        goto(LAST_ARG)
        return

    save(ENV)
    save(UNEV)

    set_continue(ACC_ARG)
    goto(EVAL_EXPR)

def ACC_ARG():
    restore(UNEV)
    restore(ENV)
    restore(ARGL)

    adjoin_arg()

    goto(ARG_LOOP)

def LAST_ARG():
    set_continue(DID_LAST_ARG)

    goto(EVAL_EXPR)

def DID_LAST_ARG():
    restore(ARGL)

    adjoin_arg()

    goto(APPLY_FUNC)

###

def APPLY_FUNC():
    func, *args = fetch(ARGL)

    assign(FUNC, func)
    assign(ARGL, args)

    if is_primitive_func():
        goto(APPLY_PRIMITIVE)
    # if is_compound_func():
    else:
        goto(APPLY_COMPOUND)

def APPLY_PRIMITIVE():
    apply_primitive_func()

    restore(CONT)

    goto_continue()

def APPLY_COMPOUND():
    # this needs to agree with eval_lambda
    env, params, body = fetch(FUNC)

    assign(UNEV, params)
    assign(ENV, env)
    extend_env()

    assign(UNEV, body)

    goto(EVAL_SEQ)

###

def EVAL_SEQ():
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

    goto(EVAL_EXPR)

def EVAL_SEQ_CONT():
    restore(ENV)
    restore(UNEV)

    goto(EVAL_SEQ)

def EVAL_SEQ_LAST():
    restore(CONT)

    goto(EVAL_EXPR)

###

def ALT_EVAL_SEQ():
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

    goto(EVAL_EXPR)

def ALT_EVAL_SEQ_CONT():
    restore(ENV)
    restore(UNEV)

    goto(ALT_EVAL_SEQ)

def ALT_EVAL_SEQ_END():
    restore(CONT)
    goto_continue()

###

def EVAL_QUASIQUOTE():
    _, text = fetch(EXPR)

    if is_simple(text):
        goto(EVAL_QUOTE)
        return

    assign(EXPR, text)
    assign(ARGL, ['list'])

    save(CONT)
    set_continue(DID_QUASIQUOTE)

    goto(QSQ_LOOP)

def QSQ_LOOP():
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

def QSQ_SIMPLE():
    assign(VAL, ['quote', fetch(EXPR)])

    adjoin_arg()

    goto(QSQ_CHECK_REST)

def QSQ_UNQUOTED():
    _, text = fetch(EXPR)

    assign(VAL, text)

    adjoin_arg()

    goto(QSQ_CHECK_REST)

def QSQ_SPLICE():
    _, text = fetch(EXPR)

    assign(EXPR, text)

    save(ARGL)
    save(UNEV)
    save(CONT)

    set_continue(QSQ_DID_SPLICE)

    goto(EVAL_EXPR)

def QSQ_DID_SPLICE():
    restore(CONT)
    restore(UNEV)
    restore(ARGL)

    assign(ARGL, fetch(ARGL) + fetch(VAL))

    goto(QSQ_CHECK_REST)

def QSQ_SUBLIST():
    save(ARGL)
    save(UNEV)
    save(CONT)

    assign(ARGL, ['list'])

    set_continue(DID_QSQ_SUBLIST)

    goto(QSQ_LOOP)

def DID_QSQ_SUBLIST():
    assign(VAL, fetch(ARGL))

    restore(CONT)
    restore(UNEV)
    restore(ARGL)

    adjoin_arg()

    goto(QSQ_CHECK_REST)

def QSQ_CHECK_REST():
    if not fetch(UNEV):
        goto_continue()
        return

    assign(EXPR, fetch(UNEV))

    goto(QSQ_LOOP)

def DID_QUASIQUOTE():
    restore(CONT)

    assign(EXPR, fetch(ARGL))

    goto(EVAL_EXPR)

###

def EVAL_DEFMACRO():
    define_macro()
    goto_continue()

###

def EVAL_MACRO():
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
    goto(EVAL_EXPR)

def DID_MACRO():
    restore(CONT)
    restore(ENV)

    assign(EXPR, fetch(VAL))
    goto(EVAL_EXPR)
