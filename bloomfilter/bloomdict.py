"""
A Python dict with a Bloom filter in front of it. Not performant - primarily
used for measurement.
"""
import collections

import bloomfilter

class BloomDict(collections.UserDict):
    """
    A dictionary with a bloom filter in front of it.

    This is not meant to be performant - items are never removed from the
    Bloom filter and the Bloom filter is never recreated.

    Intentionally not typed for simplicity.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        :param bloom_m: (keyword argument) The size in bits of the bloom 
        filter. Defaults to 1009.
        :param bloom_h: (keyword argument) The number of hash functions in 
        the bloom filter. Defaults to 5.
        """
        # Bloom filter parameters
        bloom_m: int = 1009
        if "bloom_m" in kwargs:
            bloom_m = kwargs["bloom_m"]
        bloom_h: int = 5
        if "bloom_h" in kwargs:
            bloom_h = kwargs["bloom_h"]
        self.bloom = bloomfilter.BloomFilter(bloom_m, 
                bloomfilter.sane_hash_list(bloom_h, bloom_m))
        """
        The bloom filter
        """
        self.bloom_tns: int = 0
        """Number rejected by the bloom filter"""
        self.bloom_tps: int = 0
        """Number passed by bloom filter and also in dict"""
        self.bloom_fps: int = 0
        """Number passed by bloom filter but not in dict"""
        self.queries: int = 0
        """Total number of get queries"""

        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        self.queries += 1
        if not self.bloom.get(key):
            self.bloom_tns += 1
            raise KeyError(key)
        if key in self.data:
            self.bloom_tps += 1
        else:
            self.bloom_fps += 1
        return self.data[key]

    def __setitem__(self, key, value):
        if key not in self.data:
            # This is an insert. Also insert into bloom filter.
            self.bloom.insert(key)
        self.data[key] = value
