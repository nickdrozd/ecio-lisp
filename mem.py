'''
    As with the stack, memory access will be implemented with
    register operations, even though conceptually memory and
    registers are distinct.

    TODO:
        * garbage collection!
            * mark-sweep
            * Xstop-copyX
        * figure out a better gc trigger
            * memory limit?
'''

from reg import fetch, assign


MEM = 'MEM'

PREFIX = '__MEM_'

ROOT_INDEX = 0

ROOT = PREFIX + str(ROOT_INDEX)

MEM_LEN = 16

def read_from_address(address):
    memory = fetch(MEM)
    return memory[address]

def write_to_free_address(data):
    address = next_free_address(fetch(MEM))
    write_to_address(data, address)
    return address

def write_to_address(data, address):
    memory = fetch(MEM)
    memory[address] = data
    assign(MEM, memory)

def next_free_address(memory_space):
    used_addresses = [
        convert_str_address(address)
        for address in memory_space.keys()
    ]

    if len(used_addresses) == 0:
        return convert_num_address(0)

    # if every address from 0 through n are used,
    # n + 1 is the next address
    address_cap = max(used_addresses) + 1

    # get the first available address if there is one
    for address in range(address_cap):
        if address not in used_addresses:
            return convert_num_address(address)

    return convert_num_address(address_cap)

def convert_num_address(num_address):
    return PREFIX + str(num_address)

def convert_str_address(str_address):
    return int(str_address[len(PREFIX):])

# garbage collection

# it would be nice to have this stuff in a separate file,
# but there's some weird import circularity

def collect_garbage_if_needed():
    free_address = next_free_address(fetch(MEM))
    if convert_str_address(free_address) >= MEM_LEN:
        print('Collecting gargage...')
        collect_garbage()

BROKEN_HEART = '</3'

# stop and copy
def collect_garbage():
    from_space = fetch(MEM)

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

    assign(MEM, to_space)


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
