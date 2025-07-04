# implementing a dictionary data structure in python using ctypes

import ctypes
import math  # I think I added this just in case... not actually used

# Node to hold key-value pairs; supports chaining for collisions
class _DictEntry:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.next = None  # linked list pointer for collision chains

class PyDict:
    def __init__(self):
        self._default_cap = 8
        self._max_load = 0.66
        self.count = 0
        self.cap = self._default_cap
        self.slots = self._new_table(self.cap)  # array of pointers to entries
    def _new_table(self, cap):
        return (cap * ctypes.POINTER(_DictEntry))()
    def _hash(self, key):
        return hash(key) % self.cap
    def _rehash(self, new_cap):
        old_slots = self.slots
        old_cap = self.cap
        self.slots = self._new_table(new_cap)
        self.cap = new_cap
        self.count = 0  # will recount as we re-add

        for i in range(old_cap):
            node = old_slots[i]
            while node:
                self[node.key] = node.val  # triggers insert
                node = node.next

    def __setitem__(self, key, val):
        if (self.count + 1) / self.cap > self._max_load:
            self._rehash(self.cap * 2)

        idx = self._hash(key)
        node = self.slots[idx]

        while node:
            if node.key == key:
                node.val = val
                return
            node = node.next

        # Not found — create a new entry and shove it in front
        new_node = _DictEntry(key, val)
        new_node.next = self.slots[idx]
        self.slots[idx] = ctypes.pointer(new_node)
        self.count += 1

    def __getitem__(self, key):
        idx = self._hash(key)
        node = self.slots[idx]

        while node:
            if node.key == key:
                return node.val
            node = node.next

        raise KeyError(f"{key} not in dictionary")

    def __delitem__(self, key):
        idx = self._hash(key)
        node = self.slots[idx]
        prev = None

        while node:
            if node.key == key:
                if prev:
                    prev.next = node.next
                else:
                    self.slots[idx] = node.next
                self.count -= 1
                if self.cap > self._default_cap and self.count < self.cap // 4:
                    self._rehash(max(self._default_cap, self.cap // 2))
                return
            prev = node
            node = node.next

        raise KeyError(f"{key} not found for deletion")

    def __contains__(self, key):
        try:
            _ = self[key]
            return True
        except KeyError:
            return False

    def __len__(self):
        return self.count

    def keys(self):
        result = []
        for i in range(self.cap):
            node = self.slots[i]
            while node:
                result.append(node.key)
                node = node.next
        return result

    def values(self):
        result = []
        for i in range(self.cap):
            node = self.slots[i]
            while node:
                result.append(node.val)
                node = node.next
        return result

    def items(self):
        pairs = []
        for i in range(self.cap):
            node = self.slots[i]
            while node:
                pairs.append((node.key, node.val))
                node = node.next
        return pairs

    def __str__(self):
        elements = []
        for i in range(self.cap):
            node = self.slots[i]
            while node:
                elements.append(f"{node.key!r}: {node.val!r}")
                node = node.next
        return "{" + ", ".join(elements) + "}"

# quick check
if __name__ == "__main__":
    mydict = PyDict()
    
