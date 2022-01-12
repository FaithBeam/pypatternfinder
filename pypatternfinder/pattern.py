from copy import deepcopy
from typing import Tuple, Optional


class Byte:
    def __init__(self):
        self.n1 = Nibble()
        self.n2 = Nibble()


class Nibble:
    def __init__(self):
        self.wildcard: Optional[bool] = None
        self.data: Optional[int] = None


class Signature:
    def __init__(self):
        self.name: Optional[str] = None
        self.pattern: Optional[list[Byte]] = None
        self.found_offset = -1

    def __str__(self):
        return self.name


def __format_pattern(pattern: str) -> str:
    result = ""
    for ch in pattern:
        if "0" <= ch <= "9" or "A" <= ch <= "F" or "a" <= ch <= "f" or ch == "?":
            result = "".join([result, ch])
    return result


def __hex_ch_to_int(ch: str) -> int:
    if "0" <= ch <= "9":
        return ord(ch) - ord("0")
    if "A" <= ch <= "F":
        return ord(ch) - ord("A") + 10
    if "a" <= ch <= "f":
        return ord(ch) - ord("a") + 10
    return -1


def __match_byte(b, p: Byte) -> bool:
    if not p.n1.wildcard:
        n1 = b >> 4
        if n1 != p.n1.data:
            return False
    if not p.n2.wildcard:
        n2 = b & 0xF
        if n2 != p.n2.data:
            return False
    return True


def transform(pattern: str) -> list[Byte]:
    pattern = __format_pattern(pattern)
    length = len(pattern)
    if length == 0:
        return []
    result = []
    if length % 2 != 0:
        pattern += "?"
        length += 1
    j = 0
    new_byte = Byte()
    for ch in pattern:
        if ch == "?":
            if j == 0:
                new_byte.n1.wildcard = True
            else:
                new_byte.n2.wildcard = True
        else:
            if j == 0:
                new_byte.n1.wildcard = False
                new_byte.n1.data = __hex_ch_to_int(ch) & 0xF
            else:
                new_byte.n2.wildcard = False
                new_byte.n2.data = __hex_ch_to_int(ch) & 0xF

        j += 1
        if j == 2:
            j = 0
            result.append(deepcopy(new_byte))

    return result


def find(data: bytearray, pattern: list[Byte], offset=0) -> Tuple[bool, int]:
    if data is None or pattern is None:
        return False, -1
    pattern_size = len(pattern)
    pos = 0
    for i in range(offset, len(data)):
        if __match_byte(data[i], pattern[pos]):
            pos += 1
            if pos == pattern_size:
                return True, i - pattern_size + 1
        else:
            i -= pos
            pos = 0

    return False, -1


def find_all(data: bytearray, pattern: list[Byte]) -> Tuple[bool, list[int]]:
    offsets_found = []
    size = len(data)
    pos = 0
    while size > pos:
        result, offset = find(data, pattern, pos)
        if result:
            offsets_found.append(offset)
            pos = offset + len(pattern)
        else:
            break
    if len(offsets_found) > 0:
        return True, offsets_found
    else:
        return False, []


def scan(data: bytearray, signatures: list[Signature]):
    found = []
    for s in signatures:
        result, offset = find(data, s.pattern)
        if result:
            s.found_offset = offset
            found.append(s)
    return found
