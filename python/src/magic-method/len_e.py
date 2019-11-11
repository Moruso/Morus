class A:

    def __init__(self):
        self._a = list(range(10))


class B:

    def __init__(self):
        self._b = list(range(10))

    def __len__(self):
        return 5


class C:

    def __init__(self):
        self._c = list(range(10))

    def __len__(self):
        return len(self._c)


a = A()
b = B()
c = C()

try:
    print(len(a))
except Exception as e:
    print(e)
print(len(b))
print(len(c))