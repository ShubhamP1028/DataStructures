# Implement a list data structure in Python using ctypes
import ctypes
import sys

class PyList:
    def __init__(self):
        self.size = 0
        self.capacity = 1
        self._data = self._init_array(self.capacity)

    def _init_array(self, cap):
        # kinda low-level: create raw array for 'cap' items
        return (cap * ctypes.py_object)()

    def __len__(self):
        return self.size  # return the current number of elements

    def __getitem__(self, idx):
        if not 0 <= idx < self.size:
            raise IndexError("Index out of bounds")
        return self._data[idx]

    def __setitem__(self, idx, val):
        if not 0 <= idx < self.size:
            raise IndexError("Can't assign to index that's not there")
        self._data[idx] = val

    def append(self, value):
        # Add something at the end; make space if needed
        if self.size == self.capacity:
            self._resize(self.capacity * 2)
        self._data[self.size] = value
        self.size += 1

    def insert(self, pos, value):
        if not 0 <= pos <= self.size:
            raise IndexError("Insert position invalid")
        if self.size == self.capacity:
            self._resize(self.capacity * 2)
        # slide everything to the right
        for i in range(self.size, pos, -1):
            self._data[i] = self._data[i - 1]
        self._data[pos] = value
        self.size += 1

    def pop(self, idx=None):
        # kinda like list.pop(), but has a twist: shrinks when too empty
        if self.size == 0:
            raise IndexError("Can't pop from empty list")
        if idx is None:
            idx = self.size - 1  # default to last
        if not 0 <= idx < self.size:
            raise IndexError("Index for pop is off")
        popped_item = self._data[idx]
        # shift left
        for i in range(idx, self.size - 1):
            self._data[i] = self._data[i + 1]
        self.size -= 1
        if self.size < self.capacity // 4:
            self._resize(max(1, self.capacity // 2))  # never go below 1
        return popped_item

    def _resize(self, new_cap):
        # Resizing logic: make new array, copy over
        temp = self._init_array(new_cap)
        for i in range(self.size):
            temp[i] = self._data[i]
        self._data = temp
        self.capacity = new_cap

    def __contains__(self, item):
        # Linear search for item (O(n), but hey, that's fine)
        for i in range(self.size):
            if self._data[i] == item:
                return True
        return False

    def index(self, item):
        # Get first index where item appears
        for i in range(self.size):
            if self._data[i] == item:
                return i
        raise ValueError(f"{item} not found in list")

    def count(self, item):
        hits = 0
        for i in range(self.size):
            if self._data[i] == item:
                hits += 1
        return hits

    def __str__(self):
        return "[" + ", ".join(str(self._data[i]) for i in range(self.size)) + "]"

    def __repr__(self):
        return self.__str__()

# testing things out
if __name__ == "__main__":
    my_list = PyList()