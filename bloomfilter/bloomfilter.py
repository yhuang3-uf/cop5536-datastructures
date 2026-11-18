"""
Implementation of a Bloom filter.

Requires Python version 3.10 or newer.
"""

import typing

def hash_kmodm(o: typing.Any, k: int, m: int) -> int:
    """
    The `k mod m` hash function for the Bloom filter, based on Python's
    `hash` function. Can be used as a sane default hash function for Bloom
    filters.
    
    :param o: The object to hash and store into the Bloom filter.
    :param k: The multiplier `k` in the hash function
    :param m: The number of bits in the hash function `m`.
    
    :return: The hash function. Guaranteed to be within the range [0, m).
    """
    return k*hash(o) % m

class BloomFilter:
    """
    Python class implementing a Bloom filter.
    """
    
    def __init__(self, m: int, 
            hash_fns: typing.Sequence[typing.Callable[[typing.Any], int]]) -> None:
        """
        :param m: The Bloom filter will contain `m` bits.
        :param hash_fns: A `Sequence` of functions hashing the items into 
        `int` objects. These `int` objects will be taken mod `m` if not in the
        range of `[0,m)`.
        """
        self.__m: int = m
        self.filter_bits: bytearray
        """
        The Bloom filter itself. The last byte may not be completely used.
        """
        self.clear()  # Set the Bloom filter
        self.hash_fns: typing.Sequence[typing.Callable[[typing.Any], int]] = hash_fns
        """
        The hash functions that make up this Bloom filter. Should not be
        changed after class instantiation.
        """

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
        self.filter_bits = bytearray(b"\x00" * (self.m // 4 + int(bool(self.m % 4)) ))

    def get_bit(self, index: int) -> bool:
        """
        :param index: The indices of the bits to get
        """
        return bool(self.filter_bits[index // 4] & (1 << (3 - index%4)))

    def set_bit(self, index: int, value: bool) -> None:
        """
        Internal function used to set some bits within the Bloom filter.

        :param index: the index of the bit to set
        :param value: The value to set the bits to.
        """
        self.filter_bits[index // 4] |= int(value) << (3 - index%4)
    
    def __repr__(self) -> str:
        return "BloomFilter(m={}, filter_bits={})".format(
            repr(self.m),
            repr(self.filter_bits),
        )
