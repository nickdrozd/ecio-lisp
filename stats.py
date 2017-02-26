'''
    TODO:
        * add memory stats
            * gc stats
'''

STATS = 1

def display_stats():
    if STATS:
        display_stack_stats()
        display_label_stats()
        display_fetch_stats()

    reset_stats()


def reset_stats():
    for counter in COUNTERS:
        COUNTERS[counter] = 0

COUNTERS = {
    'number_of_saves': 0,
    'curr_stack_depth': 0,
    'max_stack_depth': 0,

    'labels_passed': 0,

    'fetch_count': 0,
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

def display_fetch_stats():
    fetches = COUNTERS['fetch_count']

    print('Total fetches:', fetches)

def fetch_stats(fetch_func):
    def fetch_wrapper(reg):
        fetched = fetch_func(reg)

        COUNTERS['fetch_count'] += 1

        return fetched

    return fetch_wrapper






