# functools 

### partial 
> 固定一部分函数的参数

~~~ python
from functools import partial

def add(a, b, c)

a = 1
b = 2
c = 3
d = 4

n_add = partial(add, a, b) # 固定a,b 两个参数

n_add(c)
n_add(d)

~~~