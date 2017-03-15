# pylint: skip-file
from reg import EXPR, ENV, FUNC, ARGL, CONT, VAL, UNEV

from reg import assign, fetch, adjoin_arg
from stack import save, restore
from instr import goto, set_continue, goto_continue

from keywords import keyword_dispatch, is_simple, is_unquoted, is_splice

from env import lookup_expr, is_unbound,\
    define_var, define_macro, set_var, extend_env
from prim import is_primitive_func, apply_primitive_func


def EVAL_EXPR():
    save(CONT)
    save(ENV)

    set_continue(DID_ANALYSIS)

    goto(ANALYZE)

def ANALYZE():
    expr = fetch(EXPR)
    label = keyword_dispatch(expr)
    goto(label)

def DID_ANALYSIS():
    restore(ENV)
    restore(CONT)

    assign(EXPR, fetch(VAL))

    goto(EXECUTE)

def EXECUTE():
    label, expr = fetch(EXPR)

    assign(EXPR, expr)

    goto(label)

###

def ANALYZE_NUM():
    num = fetch(EXPR)

    assign(VAL, ['EXECUTE_NUM', num])

    goto_continue()

def EXECUTE_NUM():
    num = fetch(EXPR)

    assign(VAL, num)

    goto_continue()

###

def ANALYZE_QUOTE():
    text = fetch(EXPR)

    assign(VAL, ['EXECUTE_QUOTE', text])

    goto_continue()

def EXECUTE_QUOTE():
    text = fetch(EXPR)

    assign(VAL, text)

    goto_continue()

###

def ANALYZE_VAR():
    var = fetch(EXPR)

    assign(VAL, ['EXECUTE_VAR', var])

    goto_continue()

def EXECUTE_VAR():
    assign(VAL, lookup_expr())

    goto_continue()

###

def ANALYZE_LAMBDA():
    _, params, *body = fetch(EXPR)

    assign(EXPR, body)
    assign(UNEV, params)

    save(CONT)
    save(UNEV)

    set_continue(DID_LAMBDA_BODY)

    goto(ANALYZE_SEQUENCE)

def DID_LAMBDA_BODY():
    restore(UNEV)
    restore(CONT)

    params, body = fetch(UNEV), fetch(VAL)

    assign(VAL, ['EXECUTE_LAMBDA', [params, body]])

    goto_continue()

def EXECUTE_LAMBDA():
    params, body = fetch(EXPR)
    env = fetch(ENV)

    assign(VAL, [env, params, body])

    goto_continue()

###

def ANALYZE_BEGIN():
    _, *exprs = fetch(EXPR)

    assign(EXPR, exprs)

    goto(ANALYZE_SEQUENCE)

###

def ANALYZE_SEQUENCE():
    save(CONT)

    set_continue(DID_SEQ_MAP)

    goto(MAP_ANALYZE)

def DID_SEQ_MAP():
    restore(CONT)

    first, *rest = fetch(ARGL)

    assign(EXPR, first)
    assign(UNEV, rest)

    goto(SEQ_LOOP)

def SEQ_LOOP():
    # first, *rest in EXPR, UNEV
    if not fetch(UNEV):
        goto(DID_SEQ_ANALYSIS)
        return

    first = fetch(EXPR)
    second, *rest = fetch(UNEV)

    assign(UNEV, rest)

    assign(EXPR, ['EXECUTE_SEQ', [first, second]])

    goto(SEQ_LOOP)

def DID_SEQ_ANALYSIS():
    assign(VAL, fetch(EXPR))

    goto_continue()

def EXECUTE_SEQ():
    first, last = fetch(EXPR)

    assign(EXPR, first)
    assign(UNEV, last)

    if not fetch(EXPR):
        goto(EXECUTE)
        return

    save(CONT)
    save(ENV)
    save(UNEV)

    set_continue(DID_FIRST_EXPR)

    goto(EXECUTE)

def DID_FIRST_EXPR():
    restore(UNEV)
    restore(ENV)
    restore(CONT)

    assign(EXPR, fetch(UNEV))

    goto(EXECUTE)

###

def ANALYZE_DEF():
    _, var, val = fetch(EXPR)

    assign(EXPR, val)
    assign(UNEV, var)

    save(CONT)
    save(UNEV)

    set_continue(DID_DEF_VAL_ANALYSIS)

    goto(ANALYZE)

def DID_DEF_VAL_ANALYSIS():
    restore(UNEV)
    restore(CONT)

    var, val = fetch(UNEV), fetch(VAL)

    assign(VAL, ['EXECUTE_DEF', [var, val]])

    goto_continue()

def EXECUTE_DEF():
    var, val = fetch(EXPR)

    assign(UNEV, var)
    assign(EXPR, val)

    save(CONT)
    save(ENV)
    save(UNEV)

    set_continue(DID_DEF_VAL_EXECUTION)

    goto(EXECUTE)

def DID_DEF_VAL_EXECUTION():
    restore(UNEV)
    restore(ENV)
    restore(CONT)

    define_var()

    goto_continue()

###

def ANALYZE_ASS():
    _, var, val = fetch(EXPR)

    assign(EXPR, val)
    assign(UNEV, var)

    save(CONT)
    save(UNEV)

    set_continue(DID_ASS_VAL_ANALYSIS)

    goto(ANALYZE)

def DID_ASS_VAL_ANALYSIS():
    restore(UNEV)
    restore(CONT)

    var, val = fetch(UNEV), fetch(VAL)

    assign(VAL, ['EXECUTE_ASS', [var, val]])

    goto_continue()

def EXECUTE_ASS():
    var, val = fetch(EXPR)

    assign(UNEV, var)
    assign(EXPR, val)

    save(CONT)
    save(ENV)
    save(UNEV)

    set_continue(DID_ASS_VAL_EXECUTION)

    goto(EXECUTE)

def DID_ASS_VAL_EXECUTION():
    restore(UNEV)
    restore(ENV)
    restore(CONT)

    set_var()

    goto_continue()

###

def ANALYZE_IF():
    _, *exprs = fetch(EXPR)

    assign(EXPR, exprs)

    save(CONT)

    set_continue(DID_ANAL_IF)

    goto(MAP_ANALYZE)

def DID_ANAL_IF():
    restore(CONT)

    assign(VAL, ['EXECUTE_IF', fetch(VAL)])

    goto_continue()

def EXECUTE_IF():
    test, *alternatives = fetch(EXPR)

    assign(EXPR, test)
    assign(UNEV, alternatives)

    save(CONT)
    save(ENV)
    save(UNEV)

    set_continue(IF_DECIDE)

    goto(EXECUTE)

def IF_DECIDE():
    restore(UNEV)
    restore(ENV)
    restore(CONT)

    # use python's truthiness
    if fetch(VAL):
        goto(IF_THEN)
        return

    goto(IF_ELSE)

def IF_THEN():
    consequence, _ = fetch(UNEV)

    assign(EXPR, consequence)

    goto(EXECUTE)

def IF_ELSE():
    _, alternative = fetch(UNEV)

    assign(EXPR, alternative)

    goto(EXECUTE)

###

def ANALYZE_CALL():
    save(CONT)

    set_continue(DID_CALL_ANALYSIS)

    goto(MAP_ANALYZE)

def DID_CALL_ANALYSIS():
    restore(CONT)

    assign(VAL, ['EXECUTE_CALL', fetch(VAL)])

    goto_continue()

def EXECUTE_CALL():
    save(CONT)

    set_continue(APPLY_FUNC)

    goto(MAP_EXECUTE)

def APPLY_FUNC():
    restore(CONT)

    func, *args = fetch(VAL)

    assign(FUNC, func)
    assign(ARGL, args)

    if is_primitive_func():
        goto(APPLY_PRIMITIVE)
    else:
        goto(APPLY_COMPOUND)

def APPLY_PRIMITIVE():
    apply_primitive_func()

    goto_continue()

def APPLY_COMPOUND():
    env, params, body = fetch(FUNC)

    assign(EXPR, body)
    assign(UNEV, params)
    assign(ENV, env)

    extend_env()

    goto(EXECUTE)

###

def MAP_ANALYZE():
    save(CONT)

    # assume nonempty list
    first, *rest = fetch(EXPR)

    assign(EXPR, first)
    assign(UNEV, rest)

    if is_simple(first):
        goto(SIMPLE_FIRST_ANALYZE)
        return

    save(UNEV)

    set_continue(DID_COMPOUND_FIRST_ANALYZE)

    goto(ANALYZE)

def SIMPLE_FIRST_ANALYZE():
    set_continue(DID_FIRST_ANALYZE)

    goto(ANALYZE)

def DID_COMPOUND_FIRST_ANALYZE():
    restore(UNEV)

    goto(DID_FIRST_ANALYZE)

def DID_FIRST_ANALYZE():
    result = fetch(VAL)

    assign(ARGL, [result])

    if not fetch(UNEV):
        goto(DID_MAP_ANALYZE)
        return

    goto(ARG_LOOP_ANALYZE)

def ARG_LOOP_ANALYZE():
    first, *rest = fetch(UNEV)

    assign(EXPR, first)
    assign(UNEV, rest)

    if is_simple(first):
        goto(SIMPLE_ARG_ANALYZE)
        return

    goto(COMPOUND_ARG_ANALYZE)

def SIMPLE_ARG_ANALYZE():
    set_continue(DID_SIMPLE_ARG_ANALYZE)

    goto(ANALYZE)

def DID_SIMPLE_ARG_ANALYZE():
    adjoin_arg()

    if not fetch(UNEV):
        goto(DID_MAP_ANALYZE)
        return

    goto(ARG_LOOP_ANALYZE)

def COMPOUND_ARG_ANALYZE():
    save(ARGL)

    if not fetch(UNEV):
        goto(LAST_ARG_ANALYZE)
        return

    save(UNEV)

    set_continue(ACC_ARG_ANALYZE)

    goto(ANALYZE)

def ACC_ARG_ANALYZE():
    restore(UNEV)
    restore(ARGL)

    adjoin_arg()

    goto(ARG_LOOP_ANALYZE)

def LAST_ARG_ANALYZE():
    set_continue(DID_LAST_ARG_ANALYZE)

    goto(ANALYZE)

def DID_LAST_ARG_ANALYZE():
    restore(ARGL)

    adjoin_arg()

    goto(DID_MAP_ANALYZE)

def DID_MAP_ANALYZE():
    restore(CONT)

    assign(VAL, (fetch(ARGL)))

    goto_continue()


###

def MAP_EXECUTE():
    save(CONT)

    # assume nonempty list
    first, *rest = fetch(EXPR)

    assign(EXPR, first)
    assign(UNEV, rest)

    _, expr = fetch(EXPR)

    if is_simple(expr):
        goto(SIMPLE_FIRST)
        return

    save(UNEV)

    set_continue(DID_COMPOUND_FIRST)

    goto(EXECUTE)

def SIMPLE_FIRST():
    set_continue(DID_FIRST)

    goto(EXECUTE)

def DID_COMPOUND_FIRST():
    restore(UNEV)

    goto(DID_FIRST)

def DID_FIRST():
    result = fetch(VAL)

    assign(ARGL, [result])

    if not fetch(UNEV):
        goto(DID_MAP_EXECUTE)
        return

    goto(ARG_LOOP)

def ARG_LOOP():
    first, *rest = fetch(UNEV)

    assign(EXPR, first)
    assign(UNEV, rest)

    _, expr = fetch(EXPR)

    if is_simple(expr):
        goto(SIMPLE_ARG)
        return

    goto(COMPOUND_ARG)

def SIMPLE_ARG():
    set_continue(DID_SIMPLE_ARG)

    goto(EXECUTE)

def DID_SIMPLE_ARG():
    adjoin_arg()

    if not fetch(UNEV):
        goto(DID_MAP_EXECUTE)
        return

    goto(ARG_LOOP)

def COMPOUND_ARG():
    save(ARGL)

    if not fetch(UNEV):
        goto(LAST_ARG)
        return

    save(ENV)
    save(UNEV)

    set_continue(ACC_ARG)

    goto(EXECUTE)

def ACC_ARG():
    restore(UNEV)
    restore(ENV)
    restore(ARGL)

    adjoin_arg()

    goto(ARG_LOOP)

def LAST_ARG():
    set_continue(DID_LAST_ARG)

    goto(EXECUTE)

def DID_LAST_ARG():
    restore(ARGL)

    adjoin_arg()

    goto(DID_MAP_EXECUTE)

def DID_MAP_EXECUTE():
    restore(CONT)

    assign(VAL, fetch(ARGL))

    goto_continue()



























































