"""
Monte Carlo simulation for the Bloom Filter.
"""

import random
import sys

import bloomdict

def main(argv: list[str]) -> int:
    query_count: int = 10000
    """Number of queries to test with for this simulation"""

    filter_elements: int = 400
    """Number of elements within the Bloom filter (u)"""

    bloom_m: int = 800
    """Number of bits taken up by the Bloom filter"""

    bloom_h: int = 1
    """Number of hash functions in the Bloom filter"""

    bloom_dict: bloomdict.BloomDict = bloomdict.BloomDict(
        bloom_m=bloom_m, bloom_h=bloom_h,
    )

    # Generate lists of insert keys and query keys
    insert_keys: list[int] = random.sample(range(filter_elements * 2), 
            k=filter_elements)
    query_keys: list[int] = random.choices(range(filter_elements * 2), 
            k=query_count)

    # Insert the keys into the filter.
    for insert_key in insert_keys:
        bloom_dict[insert_key] = "hello"

    # Get random keys out of the filter.
    for query_key in query_keys:
        try:
            bloom_dict[query_key]
        except KeyError:
            pass

    print(bloom_dict.bloom)

    print(f"TNs: {bloom_dict.bloom_tns}")
    print(f"TPs: {bloom_dict.bloom_tps}")
    print(f"FPs: {bloom_dict.bloom_fps}")
    print(f"FP rate: {bloom_dict.bloom_fps / bloom_dict.queries*100:.2f}%")

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
