'''
    As with the stack, memory access will be implemented with
    register operations, even though conceptually memory and
    registers are distinct.

    TODO:
        * figure out addressing
            * can numbers be used as dict keys in json?
'''

from reg import fetch, assign

MEM = 'MEM'

def read_from_address(address):
    memory = fetch(MEM)
    return memory[str(address)]

def write_to_address(data, address):
    memory = fetch(MEM)
    memory[str(address)] = data
    assign(MEM, memory)

def next_free_address():
    memory = fetch(MEM)
    used_addresses = [int(address) for address in memory.keys()]

    if len(used_addresses) == 0:
        return 0

    # if every address from 0 through n are used,
    # n + 1 is the next address
    address_cap = max(used_addresses) + 1

    # get the first available address if there is one
    for address in range(address_cap):
        if address not in used_addresses:
            return address

    return address_cap
