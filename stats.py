'''
    TODO:
        * add memory stats
            * gc stats
'''

import time


def display_stats(stats_flag=0):
    if stats_flag:
        divider()

        # evaluator stats
        display_stack_stats()
        display_fetch_stats()
        display_label_stats()
        display_dispatch_stats()

        divider()

        # system stats
        display_read_stats()
        display_run_time()

        divider()

    reset_stats()

def reset_stats():
    for counter in COUNTERS:
        COUNTERS[counter] = 0

def divider():
    print('-' * 10)

COUNTERS = {
    'number_of_saves': 0,
    'curr_stack_depth': 0,
    'max_stack_depth': 0,

    'fetch_count': 0,

    'labels_passed': 0,

    'syntax_checks': 0,

    'read_count': 0,
}

# stack stats

def display_stack_stats():
    saves = COUNTERS['number_of_saves']
    depth = COUNTERS['max_stack_depth']

    print('Total saves:', saves)
    print('Max stack depth:', depth)

def save_stats(save_func):
    def save_wrapper(reg):
        save_func(reg)

        COUNTERS['number_of_saves'] += 1
        COUNTERS['curr_stack_depth'] += 1
        COUNTERS['max_stack_depth'] = max(
            COUNTERS['curr_stack_depth'],
            COUNTERS['max_stack_depth'])

    return save_wrapper

def restore_stats(restore_func):
    def restore_wrapper(reg):
        restore_func(reg)

        COUNTERS['curr_stack_depth'] -= 1

    return restore_wrapper

# label stats

def display_label_stats():
    labels = COUNTERS['labels_passed']

    print('Labels passed:', labels)

def goto_stats(goto_func):
    def goto_wrapper(label):
        goto_func(label)

        COUNTERS['labels_passed'] += 1

    return goto_wrapper

# file i/o stats

def display_read_stats():
    reads = COUNTERS['read_count']

    print('Total file reads:', reads)

def read_stats(read_func):
    def read_wrapper(reg, *args, **kwargs):
        contents = read_func(reg, *args, **kwargs)
        COUNTERS['read_count'] += 1

        return contents

    return read_wrapper

# run stats

def run_stats(run_func):
    def run_wrapper(*args, **kwargs):
        start = time.time()
        run_func(*args, **kwargs)
        elapsed = time.time() - start

        COUNTERS['run_time'] = elapsed

    return run_wrapper

def display_run_time():
    run_time = COUNTERS['run_time']

    print('Run-time:', run_time)

# dispatch stats

def dispatch_stats(dispatch_func):
    def dispatch_wrapper(expr):
        COUNTERS['syntax_checks'] += 1
        return dispatch_func(expr)

    return dispatch_wrapper

def display_dispatch_stats():
    syntax_checks = COUNTERS['syntax_checks']

    print('Syntax checks:', syntax_checks)

# register stats

def fetch_stats(fetch_func):
    def fetch_wrapper(reg):
        COUNTERS['fetch_count'] += 1
        return fetch_func(reg)

    return fetch_wrapper

def display_fetch_stats():
    fetches = COUNTERS['fetch_count']

    print('Total fetches:', fetches)
