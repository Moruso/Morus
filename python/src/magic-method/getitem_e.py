import random


class A:

    def __init__(self):
        self._a = list(range(10))

    def __len__(self):
        return len(self._a)

    def __getitem__(self, item):
        return self._a[item]


class B:
    def __init__(self):
        self._b = list(range(10))

    def __len__(self):
        return len(self._b)


a = A()
b = B()

print(a[5])
print(random.choice(a))

try:
    print(b[5])
except Exception as e:
    print(e)

try:
    print(random.choice(b))
except Exception as e:
    print(e)

print([item for item in a])
print([item for item in reversed(a)])
