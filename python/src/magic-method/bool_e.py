class A:
    pass


class B:

    def __bool__(self):
        return False


class C:

    def __len__(self):
        return 0


class D:

    def __len__(self):
        return 1


a = A()
b = B()
c = C()
d = D()

print(bool(a))  # 默认返回True
print(bool(b))  # 实现了__bool__
print(bool(c))  # 实现了len 返回0
print(bool(d))  # 实现了len 返回非0
