import fileio


from typing import Any, Dict, List, Union
MEM = 'MEM'

EMPTY_MEM = {}

PREFIX = '__MEM_'

# are these needed?
ROOT_INDEX = 0
ROOT = PREFIX + str(ROOT_INDEX)


def load_memory() -> Dict[str, Any]:
    return fileio.read_file(MEM, default=EMPTY_MEM)


def write_memory(data: Dict[str, Any]) -> None:
    fileio.write_file(MEM, data)


def read_from_address(address: str) -> Any:
    memory = load_memory()
    return memory[address]


def write_to_address(data: Any, address: str) -> None:
    memory = load_memory()
    memory[address] = data
    write_memory(memory)


def write_to_free_address(data: Union[List[Union[Dict[str, List[Any]], str]], List[Union[Dict[str, int], str]], List[Union[Dict[str, List[int]], str]], List[Union[Dict[str, Union[int, List[int]]], str]], List[Union[Dict[str, Union[str, int, List[int]]], str]]]) -> str:
    address = next_free_address(load_memory())
    write_to_address(data, address)
    return address


def clear_memory() -> None:
    write_memory(EMPTY_MEM)


# this is a little dramatic
def next_free_address(memory_space: Dict[str, Any]) -> str:
    used_addresses = [
        convert_str_address(address)
        for address in memory_space.keys()
    ]

    if not used_addresses:
        return convert_num_address(0)

    # if every address from 0 through n are used,
    # n + 1 is the next address
    address_cap = max(used_addresses) + 1

    # get the first available address if there is one
    for address in range(address_cap):
        if address not in used_addresses:
            return convert_num_address(address)

    return convert_num_address(address_cap)


def convert_num_address(num_address: int) -> str:
    return PREFIX + str(num_address)


def convert_str_address(str_address: str) -> int:
    return int(str_address[len(PREFIX):])
