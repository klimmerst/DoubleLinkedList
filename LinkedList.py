from typing import Any, Optional


class Node:
    def __init__(self, data: Any, next_node: Optional["Node"] = None):
        self.data = data
        self.next_node = next_node

    def __str__(self):
        return f"({self.data})"

    def __repr__(self):
        return f"Node({self.data}, {repr(self.next_node)})"  # работает, только почему когда next_node None нет ошибки?

    @property
    def next_node(self):
        return self._next_node

    @next_node.setter
    def next_node(self, value):
        if value is not None and not isinstance(value, Node):
            raise ValueError

        self._next_node = value


class LinkedList:
    def __init__(self):
        self.head = None
        self._size = 0

    def __str__(self):
        return "->".join(str(node) for node in self._node_iter())

    def __repr__(self):

        return repr(self.head)

    def __len__(self):
        return self._size

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise TypeError

        if item >= len(self) or item < 0:
            raise IndexError

        for i, node in enumerate(self._node_iter()):
            if i == item:
                return node.data

    def __setitem__(self, key, value):
        if not isinstance(key, int):
            raise TypeError

        if key >= len(self) or key < 0:
            raise IndexError

        for i, node in enumerate(self._node_iter()):
            if i == key:
                node.data = value

    def __delitem__(self, key):
        self.delete(key)

    def __iter__(self):
        for node in self._node_iter():
            yield node.data

    def _node_iter(self):
        current_node = self.head
        while current_node is not None:
            yield current_node
            current_node = current_node.next_node

    def append(self, data: Any):
        new_node = Node(data)

        for current_node in self._node_iter():
            if current_node.next_node is None:  # tail!
                current_node.next_node = new_node
                break
        else:
            self.head = new_node

        self._size += 1

    def insert(self, data, index=0):
        if index < 0 or index > len(self):
            raise ValueError

        new_node = Node(data)
        self._size += 1
        if index == 0:
            new_node.next_node = self.head
            self.head = new_node
        else:
            for i, node in enumerate(self._node_iter()):
                if i == index - 1:
                    new_node.next_node = node.next_node
                    node.next_node = new_node

    def clear(self):
        self._size = 0
        self.head = None

    def index(self, data: Any):
        for i, node in enumerate(self._node_iter()):
            if node.data == data:
                return i

        raise ValueError

    def delete(self, index: int):
        if index < 0 or index >= len(self):
            raise ValueError

        if index == 0:
            if len(self) == 0:
                raise IndexError("There's nothing to delete")
            self.head = self.head.next_node
        else:
            for i, node in enumerate(self._node_iter()):
                if i == index - 1:
                    node.next_node = node.next_node.next_node
        self._size -= 1
