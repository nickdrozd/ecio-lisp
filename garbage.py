'''
    TODO:
        * garbage collection!
            * mark-sweep
            * Xstop-copyX
        * figure out a better gc trigger
            * memory limit?
'''

from mem import \
    load_memory, write_memory, next_free_address,\
    convert_str_address, convert_num_address, ROOT, PREFIX


MEM_LEN = 16

def collect_garbage_if_needed():
    free_address = next_free_address(load_memory())
    if convert_str_address(free_address) >= MEM_LEN:
        print('Collecting gargage...')
        collect_garbage()

BROKEN_HEART = '</3'

# stop and copy
def collect_garbage():
    from_space = load_memory()

    reachable_addresses = get_reachable_addresses(from_space, ROOT)

    forwarding = {
        old: convert_num_address(i)
        for i, old in enumerate(reachable_addresses)
    }

    to_space = {
        forwarding[address]:
            update_env_pointers(
                from_space[address], forwarding)
        for address in reachable_addresses
    }

    write_memory(to_space)


def update_env_pointers(old_env, forwarding):
    old_frame, old_enclosure = old_env

    new_frame = {
        key: (val if not is_function(val)
              else [forwarding[val[0]]] + val[1:])
        for key, val in old_frame.items()
    }

    new_enclosure = (forwarding[old_enclosure]
        if old_enclosure is not None else None)

    new_env = [new_frame, new_enclosure]

    return new_env


# Would this be easier or harder to understand
# if this was written recursively? (TODO)
def get_reachable_addresses(from_space, root):
    reachable_addresses = [root]

    for address in reachable_addresses:
        env = from_space[address]
        pointers = gather_pointers(env)
        for pointer in pointers:
            if pointer not in reachable_addresses:
                reachable_addresses.append(pointer)

    return reachable_addresses


def gather_pointers(env):
    frame, enclosure = env

    functions = [val for val in frame.values() if is_function(val)]

    # functions have the form [address, params, body]
    addresses = set([address for address, _, _ in functions])

    if enclosure is not None:
        addresses.add(enclosure)

    return addresses


def is_function(entry):
    try:
        address, _, _ = entry
        return address[:len(PREFIX)] == PREFIX
    except (TypeError, ValueError):
        return False
