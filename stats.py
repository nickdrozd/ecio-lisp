STATS = 1

def display_stats():
    if STATS:
        display_stack_stats()

    reset_stats()


def reset_stats():
    for counter in COUNTERS:
        COUNTERS[counter] = 0

COUNTERS = {
    'number_of_saves' : 0,
    'curr_stack_depth' : 0,
    'max_stack_depth' : 0,
}

# stack stats

def display_stack_stats():
    saves = COUNTERS['number_of_saves']
    depth = COUNTERS['max_stack_depth']

    print('Total saves:', saves)
    print('Max stack depth:', depth)

def save_stats(save):
    def save_wrapper(reg):
        save(reg)

        COUNTERS['number_of_saves'] += 1
        COUNTERS['curr_stack_depth'] += 1
        COUNTERS['max_stack_depth'] = max(
            COUNTERS['curr_stack_depth'],
            COUNTERS['max_stack_depth'])

    return save_wrapper

def restore_stats(restore):
    def restore_wrapper(reg):
        restore(reg)

        COUNTERS['curr_stack_depth'] -= 1

    return restore_wrapper