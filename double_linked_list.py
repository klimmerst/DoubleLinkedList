import weakref
from typing import Any, Optional
from linked_list import Node, LinkedList


class DoubleNode(Node):
    def __init__(
            self, data: Any, next_node: Optional["Node"] = None, prev_node: Optional["Node"] = None
    ):
        super().__init__(data, next_node)
        self.prev_node = prev_node

    @property
    def prev_node(self):
        return self._prev_node()

    @prev_node.setter
    def prev_node(self, value):
        if value is not None and not isinstance(value, Node):
            raise ValueError
        if value is None:
            self._prev_node = None
        else:
            self._prev_node = weakref.ref(value)


class DoubleLinkedList(LinkedList):
    def __init__(self):
        super().__init__()
        self.tail = None

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise TypeError("There should be an integer")

        if item >= len(self) or item < 0:
            raise IndexError

        node = self._search_from_start_or_end(item)
        return node.data

    def __setitem__(self, key, value):
        if not isinstance(key, int):
            raise TypeError("There should be an integer")

        if key >= len(self) or key < 0:
            raise IndexError

        node = self._search_from_start_or_end(key)
        node.data = value

    def append(self, data):
        new_node = DoubleNode(data)

        if len(self) == 0:
            self.head = new_node
        else:
            self.tail.next_node = new_node
            new_node.prev_node = self.tail

        self.tail = new_node
        self._size += 1

    def insert(self, data: Any, index=0):
        if not isinstance(index, int):
            raise TypeError("There should be an integer")

        if index < 0 or index > len(self):
            raise IndexError('List index out of range')

        new_node = DoubleNode(data)

        if index == 0:
            if len(self) == 0:
                self.tail = new_node
            else:
                new_node.next_node = self.head
                self.head.prev_node = new_node
            self.head = new_node

        elif index == len(self):
            new_node.prev_node = self.tail
            self.tail.next_node = new_node
            self.tail = new_node

        else:
            node = self._search_from_start_or_end(index)
            new_node.next_node = node.next_node
            new_node.prev_node = node
            node.next_node.prev_node = new_node
            node.next_node = new_node

        self._size += 1

    def delete(self, index: int):

        if not isinstance(index, int):
            raise TypeError("There should be an integer")

        if index < 0 or index >= len(self):
            raise IndexError('List index out of range')

        if index == 0:
            if len(self) == 0:
                raise IndexError("There's nothing to delete")
            elif len(self) == 1:
                self.head = None
                self.tail = None
            else:
                self.head = self.head.next_node
                self.head.prev_node = None

        elif index == len(self) - 1:
            self.tail = self.tail.prev_node
            self.tail.next_node = None

        else:
            node = self._search_from_start_or_end(index)
            node.next_node = node.next_node.next_node
            node.next_node.prev_node = node

        self._size -= 1

    def _search_from_start_or_end(self, index):
        if not isinstance(index, int):
            raise TypeError("There should be an integer")

        if index < 0 or index >= len(self):
            raise IndexError('List index out of range')

        if index == 0:
            return self.head
        elif index == len(self) - 1:
            return self.tail

        mid = len(self) // 2

        if index <= mid:
            for i, node in enumerate(self._node_iter()):
                if i == index:
                    return node
        else:
            for i, node in enumerate(self._node_iter_revert()):
                if len(self) - 1 - i == index:
                    return node

    def _node_iter_revert(self):
        current_node = self.tail
        while current_node is not None:
            yield current_node
            current_node = current_node.prev_node

    def index(self, data: Any, start='left'):

        if start == 'left':
            for i, node in enumerate(self._node_iter()):
                if node.data == data:
                    return i
            raise IndexError("There's no such data")

        elif start == 'right':
            index = len(self) - 1
            for node in self._node_iter_revert():
                if node.data == data:
                    return index
                index -= 1
            raise IndexError("There's no such data")

        raise ValueError('Arg "start" can be only "left" or "right"')
