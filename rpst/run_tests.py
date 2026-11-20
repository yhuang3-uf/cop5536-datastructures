"""
Unit tests for the Radix Priority Search Tree (RPST)
"""

import doctest
import sys
import unittest

import rpst

class TestRpstBasic(unittest.TestCase):
    """
    Basic RPST tests
    """

    def setUp(self) -> None:
        # Create an RPST and insert some nodes
        self.rpst = rpst.Rpst(16)
        self.rpst.insert(rpst.OrderedPair(7,1))
        self.rpst.insert(rpst.OrderedPair(5,8))
        self.rpst.insert(rpst.OrderedPair(11,5))
        self.rpst.insert(rpst.OrderedPair(2,12))
        self.rpst.insert(rpst.OrderedPair(6,9))

    def test_search_fail(self) -> None:
        """
        Tests a failed search
        """
        self.assertFalse(rpst.OrderedPair(0,0) in self.rpst)
        self.assertFalse(rpst.OrderedPair(6,8) in self.rpst)
        self.assertFalse(rpst.OrderedPair(8,1) in self.rpst)

    def test_search_success(self) -> None:
        """
        Tests a successful search
        """
        self.assertTrue(rpst.OrderedPair(7,1) in self.rpst)
        self.assertTrue(rpst.OrderedPair(5,8) in self.rpst)
        self.assertTrue(rpst.OrderedPair(11,5) in self.rpst)
        self.assertTrue(rpst.OrderedPair(2,12) in self.rpst)
        self.assertTrue(rpst.OrderedPair(6,9) in self.rpst)

def main(argv: list[str]) -> int:
    DOCTEST_FILES: tuple[str, ...] = (
        "rpst.py",
    )
    doctest_file: str
    for doctest_file in DOCTEST_FILES:
        print(f"Running doctest for {doctest_file}...")
        doctest.testfile(doctest_file)
    unittest.main()
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
