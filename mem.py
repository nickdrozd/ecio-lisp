'''
    As with the stack, memory access will be implemented with
    register operations, even though conceptually memory and
    registers are distinct.

    TODO:
        * garbage collection!
            * mark-sweep
            * Xstop-copyX
        * figure out a better gc trigger
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
    FROM_SPACE = fetch(MEM)
    TO_SPACE = {}
    moved_addresses = []

    def move_to_new_memory(from_address):
        print('moving {}'.format(from_address))
        env = FROM_SPACE[from_address]

        frame, enclosure = env
        if frame is BROKEN_HEART:
            return enclosure  # enclosure is forwarding address

        to_address = next_free_address(TO_SPACE)
        TO_SPACE[to_address] = env
        # post forwarding address
        FROM_SPACE[from_address] = [BROKEN_HEART, to_address]
        moved_addresses.append(to_address)
        return to_address

    # move root
    move_to_new_memory(ROOT)

    # iterate over new addresses
    # (this list will expand as references get copied over!)
    # for address in TO_SPACE:
    for address in moved_addresses:

    # in the worst/best case, nothing in from_space is garbage,
    # so to_space will be no longer than from_space
    # for i in range(len(FROM_SPACE)):
    #     address = convert_num_address(i)
    #     if address not in TO_SPACE:
    #         break


        print('updating address:', address)
        env = TO_SPACE[address]

        # gather all pointers
        old_addresses = [pointer for pointer in gather_pointers(env)]
        print('old_addresses:', old_addresses)
        # move over everything pointed to, gathering new pointers
        new_addresses = [
            move_to_new_memory(old_address)  # side effects!
            for old_address in old_addresses
        ]
        print('new_addresses:', new_addresses)
        # update all pointers
        updated_env = update_env(env, old_addresses, new_addresses)

        # overwrite copied env with updated env
        TO_SPACE[address] = updated_env
    print('to_space:', TO_SPACE)
    assign(MEM, TO_SPACE)


def update_env(env, old_addresses, new_addresses):
    old_frame, old_enclosure = env
    print('env:', old_frame, old_enclosure)

    forwarding = {
        old: new for old, new in
        zip(old_addresses, new_addresses)
    }

    if forwarding == {}:
        return env

    forwarding[None] = None

    print('forwarding:', forwarding)

    updated_frame = {
        key: (val if not is_function(val)
              else [forwarding[val[0]]] + [val[1:]])
        for key, val in old_frame.items()
    }

    updated_enclosure = forwarding[old_enclosure]

    return [updated_frame, updated_enclosure]

def gather_pointers(env):
    frame, _ = env
    functions = [val for val in frame.values() if is_function(val)]
    # functions have the form [address, params, body]
    addresses = [address for address, _, _ in functions]
    return addresses

def is_function(entry):
    try:
        address, _, _ = entry
        return address[:len(PREFIX)] == PREFIX
    except (TypeError, ValueError):
        return False
