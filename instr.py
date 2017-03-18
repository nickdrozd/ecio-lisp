import fileio

from reg import fetch, assign, CONT
from labels import EVAL_EXP

from stats import goto_stats

INSTR = 'INSTR'

NO_INSTR = '"???"'

@goto_stats
def goto(label):
    fileio.write_file(INSTR, label)

def curr_instr():
    return fileio.read_file(INSTR, NO_INSTR)

# these aren't strictly necessary, but they're very convenient.
# conceptually, we can imagine that the CONT register has some
# specialized physical connection to INSTR register
# (or PC, or whatever it really is)

def goto_eval():
    goto(EVAL_EXP)

def goto_continue():
    goto(fetch(CONT))

def set_continue(label):
    assign(CONT, label)
