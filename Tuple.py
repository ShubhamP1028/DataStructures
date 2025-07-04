import ctypes
import sys  # not really used, but I'll leave it for now just in case

class PyTuple:
    def __init__(self, *args):
        self.length = len(args)
        self._items = self._allocate(self.length)

        for i, val in enumerate(args):
            self._assign(i, val)

    def _allocate(self, count):
        # allocating ctypes array to store the values
        return (count * ctypes.py_object)()

    def _assign(self, idx, val):
        # this is used only at init time
        if not 0 <= idx < self.length:
            raise IndexError("index out of range while assigning")
        self._items[idx] = val

    def __getitem__(self, index):
        if isinstance(index, slice):
            s, e, step = index.indices(self.length)
            return tuple(self._items[i] for i in range(s, e, step))
        
        if index < 0:
            index += self.length
        if not 0 <= index < self.length:
            raise IndexError("index out of bounds")
        return self._items[index]

    def __len__(self):
        return self.length

    def __contains__(self, target):
        for i in range(self.length):
            if self._items[i] == target:
                return True
        return False

    def count(self, value):
        c = 0
        for i in range(self.length):
            if self._items[i] == value:
                c += 1
        return c

    def index(self, value, start=0, end=None):
        end = self.length if end is None else end
        for i in range(start, end):
            if self._items[i] == value:
                return i
        raise ValueError(f"{value} is not in tuple")

    def __add__(self, other):
        if not isinstance(other, PyTuple):
            raise TypeError(f"can't add PyTuple with {type(other).__name__}")
        merged = [self[i] for i in range(self.length)] + [other[i] for i in range(len(other))]
        return PyTuple(*merged)

    def __mul__(self, times):
        if not isinstance(times, int):
            raise TypeError("repeat count must be int")
        result = []
        for _ in range(times):
            for i in range(self.length):
                result.append(self._items[i])
        return PyTuple(*result)

    def __rmul__(self, times):
        return self.__mul__(times)

    def __eq__(self, other):
        if not isinstance(other, PyTuple) or len(self) != len(other):
            return False
        for i in range(self.length):
            if self._items[i] != other[i]:
                return False
        return True

    def __hash__(self):
        # Hash logic inspired by CPython tuple hashing
        acc = 0x345678
        multiplier = 1000003
        for el in self:
            h = hash(el)
            acc = (acc ^ h) * multiplier
            multiplier += 82520 + self.length + self.length
        acc += 97531
        return acc if acc != -1 else -2  # avoid -1 like Python does

    def __str__(self):
        if self.length == 1:
            return f"({self._items[0]},)"
        return "(" + ", ".join(repr(self._items[i]) for i in range(self.length)) + ")"

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        for i in range(self.length):
            yield self._items[i]

# Quick test zone
if __name__ == "__main__":
    t1 = PyTuple(1, 2, 3, "hello")