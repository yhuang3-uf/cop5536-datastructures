"""
Implementation of a Bloom filter.

Requires Python version 3.10 or newer.
"""

import typing

class BloomFilter:
    """
    Bloom filter
    """
    def __init__(self, m: bytes, 
            hash_fns: typing.Sequence[typing.Callable[[typing.Any], int]) -> None:
        """
        :param m: The Bloom filter will contain `m` bits.
        :param hash_fns: A `Sequence` of functions hashing the items into 
        `int` objects. These `int` objects will be taken mod `m` if not in the
        range of `[0,m)`.
        """
        self.__m = m
        self.filter
        """
        The Bloom filter itself. The last byte may not be completed used.
        """
        self.clear()  # Set the BLoom filter

    @property
    def m(self) -> int:
        """
        The Bloom filter contains `m` bits.
        """
        return self.__m

    def clear(self) -> None:
        """
        Empties the bloom filter
        """
        self.filter = bytearray(b"\x00" * (self.m // 4 + int(bool(self.m % 4)) ))

    def get_bit(self, index: int) -> bool:
        """
        :param index: The indices of the bits to get
        """
        return self.filter[index // 4] & 1 << (3 - index%4)

    def set_bit(self, index: int, value: bool) -> None:
        """
        Internal function used to set some bits within the Bloom filter.

        :param index: the index of the bit to set
        :param value: The value to set the bits to.
        """
        for index in indices:
            self.filter[index % 4]
