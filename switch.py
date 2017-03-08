# pylint: disable=wildcard-import,unused-wildcard-import

from labels import *

from eval_exp import eval_exp
from ec_main import *


SWITCH = {
    EVAL_EXP : eval_exp,

    EVAL_NUM : eval_num,

    EVAL_VAR : eval_var,

    EVAL_QUOTE : eval_quote,

    EVAL_QUASIQUOTE : eval_quasiquote,
    QUASIQUOTE_LOOP : quasiquote_loop,

    EVAL_LAMBDA : eval_lambda,

    EVAL_DEF : eval_def,
    DID_DEF_VAL : did_def_val,

    EVAL_ASS : eval_ass,
    DID_ASS_VAL : did_ass_val,

    EVAL_IF : eval_if,
    IF_DECIDE : if_decide,
    IF_THEN : if_then,
    IF_ELSE : if_else,

    EVAL_FUNC : eval_func,
    DID_FUNC : did_func,
    SIMPLE_FUNC : simple_func,
    CHECK_NO_ARGS : check_no_args,
    LAST_ARG : last_arg,
    ARG_LOOP : arg_loop,
    ACC_ARG : acc_arg,
    DID_LAST_ARG : did_last_arg,
    COMPOUND_ARG : compound_arg,
    SIMPLE_ARG : simple_arg,
    DID_SIMPLE_ARG : did_simple_arg,
    RESTORE_FUNC : restore_func,

    EVAL_BEGIN : eval_begin,

    APPLY_FUNC : apply_func,

    APPLY_PRIMITIVE : apply_primitive,
    APPLY_COMPOUND : apply_compound,

    EVAL_SEQ : eval_seq,
    EVAL_SEQ_CONT : eval_seq_cont,
    EVAL_SEQ_LAST : eval_seq_last,

    ALT_EVAL_SEQ : alt_eval_seq,
    ALT_EVAL_SEQ_CONT : alt_eval_seq_cont,
    ALT_EVAL_SEQ_END : alt_eval_seq_end,
}
