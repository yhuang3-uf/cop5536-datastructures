import random
import sys
import unittest

import bloomfilter

class TestBloomFilter15(unittest.TestCase):
    """
    Performs unit testing on a Bloom filter with 15 bits
    """
    def verify_last_bit_zero(self) -> None:
        """
        Verifies that the 15th bit (zero-indexed) is still zero.
        
        This is not a test, but should be called from within tests.
        """
        self.assertEqual(self.bloom.filter_bits[-1] & 0x01, 0)
    
    def setUp(self) -> None:
        self.bloom: bloomfilter.BloomFilter = bloomfilter.BloomFilter(
            m=15,
            hash_fns=[
                lambda o: bloomfilter.hash_kmodm(o, 2, 15),
                lambda o: bloomfilter.hash_kmodm(o, 7, 15),
                lambda o: bloomfilter.hash_kmodm(o, 11, 15),
                lambda o: bloomfilter.hash_kmodm(o, 13, 15),
            ],
        )
    
    def test_empty_filter(self) -> None:
        """
        Checks that the empty filter is zeroed out.
        """
        for i, filter_byte in enumerate(self.bloom.filter_bits):
            self.assertEqual(filter_byte, 0, 
                    msg=f"Expected byte {i} to be 0.")
    
    def test_m(self) -> None:
        """
        Checks that the declared `m` value is reasonable.
        """
        self.assertEqual(self.bloom.m // 4 + int(bool(self.bloom.m % 4)), 
                len(self.bloom.filter_bits))

class TestHelperFunctions(unittest.TestCase):
    """
    Performs unit testing on bloom filter helper functions
    """
    def test_rand_kmodm(self) -> None:
        """
        Tests `hash_kmodm` with random `int`s to ensure result in [0,m)
        """
        random.seed(a=1414213562, version=2)
        TEST_COUNT: int = 10
        """Number of values to test"""
        objects_to_hash: list[int] = random.choices(range(1000), k=TEST_COUNT)
        k_values: list[int] = random.choices(range(20), k=TEST_COUNT)
        m_values: list[int] = random.choices(range(1, 10), k=TEST_COUNT)
        for i in range(TEST_COUNT):
            m_value: int = m_values[i]
            hash_result: int = bloomfilter.hash_kmodm(objects_to_hash[i], k_values[i], m_value)
            self.assertTrue(0 <= hash_result < m_value,
                    msg=f"Hash result {hash_result} was not in range [0, {m_value}).")

def main(argv: list[str]) -> int:
    """
    The main function to be invoked when this file is run from the command
    line.
    """
    unittest.main()
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
