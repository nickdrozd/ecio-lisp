from evalExp import eval_exp
from evalFuncs import *

from labels import *

switch = {
    EVAL_EXP : eval_exp,

    EVAL_NUM : eval_num,

    EVAL_VAR : eval_var,

    EVAL_QUOTE : eval_quote,

    EVAL_LAMBDA : eval_lambda,

    EVAL_DEF : eval_def,
    DID_DEF_VAL : did_def_val,

    EVAL_IF : eval_if,
    IF_DECIDE : if_decide,
    IF_THEN : if_then,
    IF_ELSE : if_else,

    EVAL_FUNC : eval_func,
    DID_FUNC : did_func,
    CHECK_NO_ARGS : check_no_args,
    LAST_ARG : last_arg,
    ARG_LOOP : arg_loop,
    ACC_ARG : acc_arg,
    DID_LAST_ARG : did_last_arg,

    APPLY_FUNC : apply_func,

    APPLY_PRIMITIVE : apply_primitive,
    APPLY_COMPOUND : apply_compound,

    EVAL_SEQ : eval_seq,
    EVAL_SEQ_CONT : eval_seq_cont,
    EVAL_SEQ_LAST : eval_seq_last,

    ALT_EVAL_SEQ : alt_eval_seq,
    ALT_EVAL_SEQ_END : alt_eval_seq_end,
}
