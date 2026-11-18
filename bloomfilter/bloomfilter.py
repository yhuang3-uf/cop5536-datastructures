"""
Implementation of a Bloom filter. Requires Python version 3.10 or newer.

The most important functions are `BloomFilter.get()`, `BloomFilter.insert()`,
and `BloomFilter.clear()`. Their use is demonstrated in the "Usage Example"
section below.

## Usage Example
```python
>>> import bloomfilter
>>> bloom = bloomfilter.BloomFilter(17, bloomfilter.sane_hash_list(h=5, m=15))
>>> bloom.insert(0)
>>> bloom.get(0)
True
>>> bloom.get(1)
False
>>> bloom.clear()
>>> bloom.get(0)
False

```
"""

import math
import typing

def hash_kmodm(o: typing.Any, k: int, m: int) -> int:
    """
    The `k mod m` hash function for the Bloom filter, based on Python's
    `hash` function.

    :param o: The object to hash and store into the Bloom filter.
    :param k: The multiplier `k` in the hash function
    :param m: The number of bits in the hash function `m`.
    
    :return: The hash function. Guaranteed to be within the range [0, m).
    """
    return k*hash(o) % m

def sane_hash_list(h: int, m: int) -> list[typing.Callable[[typing.Any], int]]:
    """
    A sane default hash family for the Bloom filter.

    :param h: The number of hash functions `h` to generate.
    :param m: The number of bits the hash function should return (`m`).
    :return: A list of hash functions that can be passed directly into
    `BloomFilter`.

    :raises ValueError: If too many hash functions were requested for the
    given `m`. If this error occurs, you may need to manually generate the
    hash functions rather than using the default. Or, a different `m` 
    should be chosen (ideally, `m` should not have many prime factors).
    """
    hash_function_list: list[typing.Callable[[typing.Any], int]] = []
    for coprime_candidate in range(1, m):
        if math.gcd(h, coprime_candidate) == 1:
            hash_function_list.append(
                    lambda o: hash_kmodm(o, coprime_candidate, m))
        if len(hash_function_list) == h:
            # We have enough hash functions, so we are done.
            break
    else:
        raise ValueError(("There are only {} integers less than {} coprime " + 
                "to {}, but {} functions were requested").format(
            len(hash_function_list),
            m, m, h,
        ))
    return hash_function_list

class BloomFilter:
    """
    Python class implementing a Bloom filter.

    This is a *probabilistic* rather than a deterministic data structure.

    Implemented magic functions:

     * `__repr__()`
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
        self.filter_bits = bytearray(b"\x00" * (self.m // 8 + int(bool(self.m % 8)) ))

    def get(self, o: typing.Any) -> bool:
        """
        Get a value from the Bloom filter.

        :param o: The value to check the presence of within the Bloom filter.

        :return: If True, object may be in Bloom filter. If False, object 
        is not in Bloom filter.
        """
        for hash_fn_index in self.hash_fn_indices(o):
            if not self.get_bit(hash_fn_index):
                # One of the bits are False. We are not in Bloom filter.
                return False

        # All values are True. We might be in Bloom filter.
        return True

    def hash_fn_indices(self, o: typing.Any) -> set[int]:
        """
        Gets the indices associated with the hash values for the current
        hash function.

        :param o: The object to hash.
        :return: Set of values containing the indices associated with the
        output of the hash functions for the given `o`
        """
        hash_fn_indices_set: set[int] = set()
        for hash_fn in self.hash_fns:
            hash_fn_indices_set.add(hash_fn(o) % self.m)
        return hash_fn_indices_set

    def get_bit(self, index: int) -> bool:
        """
        :param index: The indices of the bits to get
        """
        return bool(self.filter_bits[index // 8] & (1 << (7 - index%8)))

    def insert(self, o: typing.Any) -> None:
        """
        Insert an object into the Bloom filter. 

        The Bloom filter never "fills up" logically, so insertion never fails.

        :param o: The object to insert into the Bloom Filter.
        """
        for hash_fn_index in self.hash_fn_indices(o):
            self.set_bit(hash_fn_index, True)

    def set_bit(self, index: int, value: bool) -> None:
        """
        Internal function used to set some bits within the Bloom filter.

        :param index: the index of the bit to set
        :param value: The value to set the bits to.
        """
        self.filter_bits[index // 8] |= int(value) << (7 - index%8)
    
    def __repr__(self) -> str:
        return "BloomFilter(m={}, filter_bits={})".format(
            repr(self.m),
            repr(self.filter_bits),
        )
