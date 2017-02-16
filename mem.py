'''
    As with the stack, memory access will be implemented with
    register operations, even though conceptually memory and
    registers are distinct.

    TODO:
        * garbage collection!
            * mark-sweep
            * stop-copy
'''

from reg import fetch, assign

MEM = 'MEM'

PREFIX = 'MEM_'

ROOT = PREFIX + '0'

def read_from_address(address):
    memory = fetch(MEM)
    return memory[address]

def write_to_free_address(data):
    address = next_free_address()
    write_to_address(data, address)
    return address

def write_to_address(data, address):
    memory = fetch(MEM)
    memory[address] = data
    assign(MEM, memory)

def next_free_address():
    memory = fetch(MEM)

    used_addresses = [
        convert_str_address(address)
        for address in memory.keys()
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
