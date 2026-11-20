"""
Radix Priority Search Trees
"""

import dataclasses
import functools
import typing

class OrderedPair:
    """
    For RPSTs, the ordered pairs must be positive integers.
    """
    def __init__(self, x: int, y: int) -> None:
        self.__x: int = x
        self.__y: int = y

    @property
    def x(self) -> int:
        """x-coordinate of the ordered pair"""
        return self.__x
    @property
    def y(self) -> int:
        """y-coordinate of the ordered pair"""
        return self.__y

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"OrderedPair({self.x}, {self.y})"


@dataclasses.dataclass(frozen=True)
class Interval:
    """
    Represents the interval `[start, end)`. `start` and `end` must be integers.

    Even though the interval only accepts integers, you can check if any
    `float` is in the interval. Example:
    ```python
    >>> import rpst
    >>> rpst_interval = rpst.Interval(0,11)
    >>> 11 in rpst_interval
    False
    >>> 10 in rpst_interval
    True
    >>> 0.5 in rpst_interval
    True
    >>> -0.125 in rpst_interval
    False
    >>> 0 in rpst_interval
    True
    >>> rpst_interval.midpoint()
    5
    >>> rpst_interval.left_half()
    Interval(start=0, end=5)
    >>> len(rpst_interval)
    11

    ```
    """
    start: int
    """The start index of this interval"""
    end: int
    """The end index of this interval"""

    def midpoint(self) -> int:
        """
        Gets the integer midpoint of the interval (rounded down)
        """
        return (self.start + self.end) // 2

    def left_half(self) -> Interval:
        """
        :return: The `Interval` representing the left half of the interval
        :raises ValueError: If the interval is too small.
        """
        return Interval(self.start, self.midpoint())

    def right_half(self) -> Interval:
        """
        :return: The `Interval` representing the right half of the interval
        """
        return Interval(self.midpoint(), self.end)

    def __contains__(self, number) -> bool:
        return self.start <= number < self.end

    def __len__(self) -> int:
        return self.end - self.start


@dataclasses.dataclass(repr=False)
class RpstNode:
    """
    A node within the RPST
    """
    pair: OrderedPair
    """The ordered pair associated with this `RpstNode`"""
    left_child: typing.Optional[RpstNode] = None
    """The left child of this `RpstNode`"""
    right_child: typing.Optional[RpstNode] = None
    """The right child of this `RpstNode`"""

    def __repr__(self) -> str:
        return f"RpstNode(pair={repr(self.pair)})"

class Rpst:
    """
    Radix Priority Search Tree (RPST). RPSTs always start empty.
    """

    def __init__(self, x_limit: int) -> None:
        """
        :param x_limit: Also known as `k`, the maximum x-value within the RPST
        must be in the interval `[0, x_limit)`.
        """
        self.root: typing.Optional[RpstNode] = None
        """
        Root node of the RPST.
        """
        self.__x_limit: int = x_limit

    @property
    def x_limit(self) -> int:
        """
        Also known as `k`, the maximum x-value within the RPST
        must be in the interval `[0, x_limit)`.
        """
        return self.__x_limit

    def contains(self, pair: OrderedPair) -> bool:
        """
        Checks whether the given `OrderedPair` is in this RPST. You can also
        use the `in` operator.

        :param pair: The `OrderedPair` object to check for.
        :return: `True` if `pair` is in the `Rpst`, otherwise `False`.
        """
        try:
            self.search_node(pair)
            return True
        except KeyError:
            return False

    def insert(self, pair: OrderedPair, 
            subtree_root: typing.Optional[tuple[RpstNode, RpstNode, int, int]] = None) -> None:
        """
        :param pair: The ordered pair to insert into the RPST
        :param subtree_root: This parameter should not normally be specified,
        but allows for insertion into a subtree rather than at the root. This
        parameter should contain `(subtree_root_parent, subtree_root_node)`. 
        This parameter will be ignored if the tree is empty. Note that this
        node always has a parent because only the root node does not have a
        parent.
        :raises ValueError: If an `OrderedPair` with this x-value already
        exists within the RPST.
        """
        if pair.x < 0 or pair.x >= self.x_limit:
            raise ValueError(("Insertion failed - the x-value in ordered " + 
                    "pair {} is not within the allowable range of " + 
                    "[0, {})").format(
                pair, self.x_limit
            ))
        node_to_insert: RpstNode = RpstNode(pair)
        if self.root is None:
            # Create a new node at the root with the ordered pair.
            self.root = node_to_insert
            return
        current_parent: typing.Optional[RpstNode] = None
        """The parent of the node we are at within the tree"""
        current_node: RpstNode = self.root
        """The node we are at within the tree"""
        current_interval: Interval = Interval(0, self.x_limit)
        if subtree_root is not None:
            current_parent, current_node = subtree_root[:2]
            current_interval = Interval(*subtree_root[2:])
        while True:
            # We'll need to go down the tree. To choose the direction, we need
            # to use the x value.
            if pair.x == current_node.pair.x:
                raise ValueError(
                    ("Trying to insert ordered pair {}, but a " + 
                    "pair with the same x-value, {}, already exists.").format(
                        pair, current_node.pair
                    )
                )
            assert len(current_interval) > 0, \
                    "Logic error: cannot have interval of size 0"
            if pair.y <= current_node.pair.y:
                # Let's insert here.

                # Attach the parent pointer to the new node.
                if current_parent is None:
                    # We are the root node, we need to fix the root pointer.
                    self.root = node_to_insert
                else:
                    # Not the root node, we need to redirect the parent's
                    # pointer to the node to insert
                    
                    # We use the property that the x-values are unique to
                    # identify the node.
                    if current_parent.left_child is not None and \
                            current_parent.left_child.pair.x == current_node.pair.x:
                        # We are the left child of the parent.
                        current_parent.left_child = node_to_insert
                    else:
                        # We are the right child of the parent.
                        current_parent.right_child = node_to_insert

                # We also need to attach the children of the current node to
                # the newly-inserted node.
                node_to_insert.left_child = current_node.left_child
                node_to_insert.right_child = current_node.right_child

                # Now, we figure out where the displaced node needs to go.
                # Note `current_node` is the one that got kicked out, since
                # we just put `pair` (the node to be inserted) in.
                if current_node.pair.x < current_interval.midpoint():
                    # The displaced node belongs on the left.
                    left_child: typing.Optional[RpstNode] = node_to_insert.left_child
                    if left_child is None:
                        # Simple insert and we're done.
                        node_to_insert.left_child = current_node
                    else:
                        # Use our insert algorithm
                        self.insert(current_node.pair, (node_to_insert, left_child, 
                                current_interval.left_half().start, 
                                current_interval.left_half().end))
                else:
                    # The displaced node belongs on the right.
                    right_child: typing.Optional[RpstNode] = node_to_insert.right_child
                    if right_child is None:
                        # Simple insert and we're done.
                        node_to_insert.right_child = current_node
                    else:
                        # Use our insert algorithm
                        self.insert(current_node.pair, (node_to_insert, right_child, 
                                current_interval.right_half().start, 
                                current_interval.right_half().end))
                break
            elif pair.x < current_interval.midpoint():
                left_child = current_node.left_child
                if left_child is None:
                    # We can insert here!
                    current_node.left_child = node_to_insert
                    break
                else:
                    # Go left and try again
                    current_interval = current_interval.left_half()
                    current_node = left_child
                    current_parent = current_node
            else:
                right_child = current_node.right_child
                if right_child is None:
                    # We can insert here!
                    current_node.right_child = RpstNode(pair)
                    break
                else:
                    # Go right and try again
                    current_interval = current_interval.right_half()
                    current_node = right_child
                    current_parent = current_node

    def remove(self, pair: OrderedPair) -> OrderedPair:
        """
        Removes and returns the given pair from the RPST, if it exists.

        **Note:** Not implemeneted yet.

        :param pair: The pair to remove from the RPST.
        :raises KeyError: If the given pair does not exist.
        """
        # TODO Implement remove()
        raise NotImplementedError("remove() not implemeneted yet")

    def search_node(self, query_pair: OrderedPair) -> RpstNode:
        """
        Searches for the node containing the given ordered pair.

        :param query_pair: The pair to search through the tree with.
        :return: The matching `RpstNode` 
        :raises KeyError: If the matching node was not found in the free.
        """
        current_node: typing.Optional[RpstNode] = self.root
        current_interval: Interval = Interval(0, self.x_limit)
        while current_node is not None:
            if current_node.pair == query_pair:
                # We found our node!
                return current_node
            if query_pair.y < current_node.pair.y:
                # Not in the tree, we are done.
                break
            if query_pair.x < current_interval.midpoint():
                # Go left
                current_interval = current_interval.left_half()
                current_node = current_node.left_child
            else:
                # Go right
                current_interval = current_interval.right_half()
                current_node = current_node.right_child

        # We fell off the tree without finding a suitable node.
        raise KeyError(query_pair)

    def __contains__(self, pair) -> bool:
        return self.contains(pair)


