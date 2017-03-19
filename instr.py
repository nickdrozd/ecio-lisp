import fileio

from reg import fetch, assign, CONT

from stats import goto_stats

INSTR = 'INSTR'

NO_INSTR = '"???"'

DONE = 'DONE'

@goto_stats
def goto(label):
    fileio.write_file(INSTR, _convert_label(label))

def curr_instr():
    return fileio.read_file(INSTR, NO_INSTR)

# these aren't strictly necessary, but they're very convenient.
# conceptually, we can imagine that the CONT register has some
# specialized physical connection to INSTR register
# (or PC, or whatever it really is)

def goto_continue():
    goto(fetch(CONT))

def set_continue(label):
    assign(CONT, _convert_label(label))

def _convert_label(label):
    try:
        return label.__name__
    except AttributeError:
        return label
