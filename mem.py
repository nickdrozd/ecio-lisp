'''
    As with the stack, memory access will be implemented with
    register operations, even though conceptually memory and
    registers are distinct.
'''

from reg import fetch, assign


MEM = 'MEM'

PREFIX = '__MEM_'

# are these needed?
ROOT_INDEX = 0
ROOT = PREFIX + str(ROOT_INDEX)

def load_memory():
    return fetch(MEM)

def write_memory(data):
    assign(MEM, data)

def read_from_address(address):
    memory = load_memory()
    return memory[address]

def write_to_address(data, address):
    memory = load_memory()
    memory[address] = data
    write_memory(memory)

def write_to_free_address(data):
    address = next_free_address(load_memory())
    write_to_address(data, address)
    return address

# this is a little dramatic
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
