import ctypes
import math  # might be useful later?

class _SetNode:
    def __init__(self, val):
        self.value = val
        self.next = None

class PySet:
    def __init__(self, iterable=None):
        self._initial_capacity = 8
        self._load_threshold = 0.66
        self.count = 0
        self.cap = self._initial_capacity
        self.buckets = self._make_table(self.cap)
        if iterable:
            for thing in iterable:
                self.add(thing)
    def _make_table(self, cap):
        # just sets up empty hash slots
        return (cap * ctypes.POINTER(_SetNode))()
    def _hash(self, val):
        return hash(val) % self.cap
    def _resize(self, new_cap):
        # grow or shrink the table
        old_buckets = self.buckets
        old_cap = self.cap
        self.buckets = self._make_table(new_cap)
        self.cap = new_cap
        self.count = 0
        for i in range(old_cap):
            node = old_buckets[i]
            while node:
                self.add(node.contents.value)
                node = node.contents.next
    def add(self, val):
        if (self.count + 1) / self.cap > self._load_threshold:
            self._resize(self.cap * 2)
        idx = self._hash(val)
        node = self.buckets[idx]
        while node:
            if node.contents.value == val:
                return  # already exists
            node = node.contents.next
        # wasn't found; stick it in
        new_node = _SetNode(val)
        new_node.next = self.buckets[idx]
        self.buckets[idx] = ctypes.pointer(new_node)
        self.count += 1
    def discard(self, val):
        idx = self._hash(val)
        node = self.buckets[idx]
        prev = None
        while node:
            if node.contents.value == val:
                if prev:
                    prev.contents.next = node.contents.next
                else:
                    self.buckets[idx] = node.contents.next
                self.count -= 1
                if self.cap > self._initial_capacity and self.count < self.cap // 4:
                    self._resize(max(self._initial_capacity, self.cap // 2))
                return
            prev = node
            node = node.contents.next

    def __contains__(self, val):
        idx = self._hash(val)
        node = self.buckets[idx]
        while node:
            if node.contents.value == val:
                return True
            node = node.contents.next
        return False
    def __len__(self):
        return self.count
    def __iter__(self):
        for i in range(self.cap):
            node = self.buckets[i]
            while node:
                yield node.contents.value
                node = node.contents.next

    def union(self, other):
        combo = PySet(self)
        for item in other:
            combo.add(item)
        return combo
    def intersection(self, other):
        result = PySet()
        for item in self:
            if item in other:
                result.add(item)
        return result
    def difference(self, other):
        result = PySet()
        for item in self:
            if item not in other:
                result.add(item)
        return result
    def symmetric_difference(self, other):
        result = PySet()
        for item in self:
            if item not in other:
                result.add(item)
        for item in other:
            if item not in self:
                result.add(item)
        return result
    def isdisjoint(self, other):
        for item in self:
            if item in other:
                return False
        return True
    def issubset(self, other):
        for item in self:
            if item not in other:
                return False
        return True
    def issuperset(self, other):
        for item in other:
            if item not in self:
                return False
        return True
    def __str__(self):
        stuff = [repr(x) for x in self]
        return "{" + ", ".join(stuff) + "}" if stuff else "set()"
    def __repr__(self):
        return self.__str__()

# Some quick playing around
if __name__ == "__main__":
    a = PySet([1, 2, 3, 4, 5])
    
