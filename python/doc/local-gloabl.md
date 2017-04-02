# 关于python global, nonlocal 和 local 的区别
先来看看官方文档的解释:
In Python, variables that are only referenced inside a function are implicitly global. If a variable is assigned a value anywhere within the function’s body, it’s assumed to be a local unless explicitly declared as global.

> 以上内容来之[官方文档](https://docs.python.org/3/faq/programming.html?highlight=global#what-are-the-rules-for-local-and-global-variables-in-python)

在python 2.x中变量分为 global 和local, 在 python 3.x中多了nonlocal
> 以下例子中的id命令是用查看变量在内存中的位置, 你运行完看到的结果可能和我的不一样

### 局部变量 local
: 定义在函数内部的变量称为局部变量(Local Variable),它的作用域仅限于函数内部， 离开该函数后就是无效的，再使用就会报错.

~~~ python
def my_local_test():
    local_var = 'this is a local var'
    print("Within the function: {}".format(local_var))

my_local_test()
~~~

运行结果
~~~ bash    
Within the function: this is a local var
~~~
我们给刚才的代码函数外加上一个print, 函数就会报错.

~~~ python
def my_local_test():
    local_var = 'this is a local var'
    print("Within the function: {}".format(local_var))

my_local_test()
print("Without the function: {}".format(local_var))
~~~

运行结果
~~~ bash
Within the function: this is a local varTraceback (most recent call last):
  File "E:\GIT\Morus\python\doc\local_var.py", line 6, in <module>

    print("Without the function: {}".format(local_var))
NameError: name 'local_var' is not defined
~~~
> 报错 提示 变量local_var 没有定义

### 全局变量 global
: 在所有函数外部定义的变量称为全局变量（Global Variable），它的作用域默认是整个程序

~~~python
global_var = "this is a global var"
def my_local_test():
    print("Within the function: {}".format(global_var))

my_local_test()

print("Without the function: {}".format(global_var))

~~~

运行结果
~~~bash
Within the function: this is a global var
Without the function: this is a global var
~~~

> 全局变量可以在函数内被调用. 但是局部变量离开函数后就是无效的.


### 全局变量和局部变量同时存在
~~~python
same_var = "this is a global var"
print("Without the function: {}, id: {}".format(same_var, id(same_var)))
def my_local_test():
    same_var = 'this is a local var'
    print("Within the function: {}, id: {}".format(same_var, id(same_var)))

my_local_test()
print("Without the function: {}, id: {}".format(same_var, id(same_var)))
~~~

运行结果
~~~bash
Without the function: this is a global var, id: 39004624
Within the function: this is a local var, id: 39003000
Without the function: this is a global var, id: 39004624
~~~
> 虽然变量名一样, 但是最后一次的输出说明外层的变量并没有被修改

如果想在函数内修改全局变量就得使用 global 关键字
~~~python
same_var = "this is a global var"
print("Without the function: {}, id: {}".format(same_var, id(same_var)))
def my_local_test():
    global same_var 
    same_var = 'this is a local var'
    print("Within the function: {}, id: {}".format(same_var, id(same_var)))

my_local_test()
print("Without the function: {}, id: {}".format(same_var, id(same_var)))
~~~

运行结果
~~~bash
Without the function: this is a global var, id: 46606800
Within the function: this is a local var, id: 46605176
Without the function: this is a local var, id: 46605176
~~~
> 可以看到my_local_test函数修改了函数外定义的变量same_var

注意: 一旦函数内不适用global去引用全局变量. 那么函数内不能创建同名变量, 全局变量也不能被修改, 否则会报错
~~~python
same_var = "this is a global var"

print("Without the function: {}, id: {}".format(same_var, id(same_var)))

def my_local_test():
    print("Within the function: {}, id: {}".format(same_var, id(same_var)))
    same_var = 'this is a local var'
    print("Within the function: {}, id: {}".format(same_var, id(same_var)))

my_local_test()
print("Without the function: {}, id: {}".format(same_var, id(same_var)))
~~~

运行结果
~~~bash
Without the function: this is a global var, id: 40966608Traceback (most recent call last):
  File "E:\myproject\morus\python\src\global_local\global_local_var.py", line 10, in <module>
    my_local_test()
  File "E:\myproject\morus\python\src\global_local\global_local_var.py", line 6, in my_local_test
    print("Within the function: {}, id: {}".format(same_var, id(same_var)))
UnboundLocalError: local variable 'same_var' referenced before assignment
~~~
>上个例子中,定义same_var之前先引用了全局的same_var这样函数内就不能定义同名变量

### global nonlocal local
: 来个大集合, 实例解析..

[global_nonlocal_local_example.py](../src/global_local/global_nonlocal_local_example.py)
~~~python
#!/usr/bin/python3.5

def scope_test():

    def do_local():
        print("\tfunction do_local(")
        # print("\t\tbefore_change_spam:{}, id:{}".format(spam, id(spam)))
        spam = "local_spam"
        print("\t\tafter_change_spam: {}, id: {}".format(spam, id(spam)))
        print("\t)# do_local end ")

    def do_nonlocal():
        print("\tfunction do_nonlocal(")
        nonlocal spam
        print("\t\tbefore_change_spam:{}, id:{}".format(spam, id(spam)))
        spam = "nonlocal_spam"
        print("\t\tafter_change_spam:{}, id:{}".format(spam, id(spam)))
        print("\t)# do_nonlocal end")

    def do_global():
        print("\tfunction do_global(")
        global spam
        print("\t\tbefore_change_spam:{}, id:{}".format(spam, id(spam)))
        spam = "global_spam"
        print("\t\tafter_change_spam:{}, id:{}".format(spam, id(spam)))

    print("function scope_test(")
    spam = "test_scope_spam"
    print("\t>> scope_test_spam:{}, id:{}".format(spam, id(spam)))
    do_local()
    print("\t>> scope_test_spam:{}, id:{}".format(spam, id(spam)))
    do_nonlocal()
    print("\t>> scope_test_spam:{}, id:{}".format(spam, id(spam)))
    do_global()
    print("\t>> scope_test_spam:{}, id:{}".format(spam, id(spam)))
    print(") # scope_test end")

def main():
    print("\tfunction main(")
    print("\t\tmain_spam:{}, id:{}".format(spam, id(spam)))
    print("\t)# main end")

spam = 'begin_spam'
main()
print("global_spam:{}, id:{}".format(spam, id(spam)))
scope_test()
print("global_spam:{}, id:{}".format(spam, id(spam)))

~~~

运行结果
~~~bash
    function main(
        main_spam:begin_spam, id:460245727856
    )# main end
global_spam:begin_spam, id:460245727856
function scope_test(
    >> scope_test_spam:test_scope_spam, id:460245382960
    function do_local(
        after_change_spam: local_spam, id: 460245542832
    )# do_local end 
    >> scope_test_spam:test_scope_spam, id:460245382960
    function do_nonlocal(
        before_change_spam:test_scope_spam, id:460245382960
        after_change_spam:nonlocal_spam, id:460245381552
    )# do_nonlocal end
    >> scope_test_spam:nonlocal_spam, id:460245381552
    function do_global(
        before_change_spam:begin_spam, id:460245727856
        after_change_spam:global_spam, id:460245382832
    >> scope_test_spam:nonlocal_spam, id:460245381552
) # scope_test end
global_spam:global_spam, id:460245382832
~~~

>* 先说这个例子中main函数的作用就是为了证明: main函数的局部变量也是全局变量(main的特殊性).
>* 我们先定义了一个全局变量 `spam='begin_spam'`, 然后函数scope_test定义了自己的局部变量`spam='test_scope_spam'`, scope_test函数中的do_local函数同样定义了自己的局部变量`spam='local_spam'`从输出的结果和id我们发现这3个变量是相互独立的.
>* do_nonlocal函数, 使用了nonlocal关键字修改了spam, 发现scop_test的局部变量spam也被修改了. 但是全局的spam并没有变化
>* do_global函数, 使用了global关键字修改了spam, 我们发现scop_test的spam并没有变化.而全局的spam被修改了

结论: 函数要想修改全局变量就得使用global关键字, 想修改上层函数就得使用nonlocal

### nonlocal
: 我们回头再看nonlocal, python3新增的功能

1. 我们看看上层函数包不包括main即当上层变量是全局变量的时候能否使用
~~~python
def scop_test():
    nonlocal spam
    spame = "scop_test_spam"

spam = 'global_spam'
~~~

运行结果
~~~bash
File "E:\myproject\morus\python\src\global_local\nonlocal_var.py", line 2
    nonlocal spam
SyntaxError: no binding for nonlocal 'spam' found
~~~

> 看来上层函数不包括main, 如果上层函数没有定义这个变量就会报错.

2. 来看看上层是上一层, 还是上多层.

[nonlocal_var](../src/global_local/nonlocal_var.py)
~~~python
def scop_test():
    print("function scop_test(")

    def do_nonlocal():
        print("\tfunction do_nonlocal(")

        def do_nonlocal_inner():
            print("\t\tfunction do_nonlocal(")
            nonlocal spam_a
            nonlocal spam_b
            nonlocal spam_c
            print("\t\t\tbefore_change_spam_a:{}, id:{}".format(spam_a, id(spam_a)))
            spam_a = "nonlocal_inner_spam_a"
            print("\t\t\tafter_change_spam_a:{}, id:{}".format(spam_a, id(spam_a)))
            print()
            print("\t\t\tbefore_change_spam_b:{}, id:{}".format(spam_b, id(spam_b)))
            spam_b = "nonlocal_inner_spam_b"
            print("\t\t\tafter_change_spam_a:{}, id:{}".format(spam_b, id(spam_b)))
            print()
            print("\t\t\tbefore_change_spam_c:{}, id:{}".format(spam_c, id(spam_c)))
            spam_c = "nonlocal_inner_spam_c"
            print("\t\t\tafter_change_spam_c:{}, id:{}".format(spam_c, id(spam_c)))

            print("\t\t) #end do_nonlocal_inner")
            print()

        spam_b = "nonlocal_spam_b"
        print("\t\tdo_nonlocal_spam_b:{}, id:{}".format(spam_b, id(spam_b)))

        nonlocal spam_c
        spam_c = "nonlocal_spam_c"
        print("\t\tdo_nonlocal_spam_c:{}, id:{}".format(spam_c, id(spam_c)))

        do_nonlocal_inner()

        print("\t\tend_do_nonlocal_spam_b:{}, id:{}".format(spam_b, id(spam_b)))
        print("\t\tend_do_nonlocal_spam_c:{}, id:{}".format(spam_c, id(spam_c)))
        print("\t) #end do_nonlocal")

    spam_a = "scop_spam_a"
    spam_b = "scop_spam_b"
    spam_c = "scop_spam_c"
    print("\tscop_test_spam_a:{}, id:{}".format(spam_a, id(spam_a)))
    print("\tscop_test_spam_b:{}, id:{}".format(spam_b, id(spam_b)))
    print("\tscop_test_spam_c:{}, id:{}".format(spam_c, id(spam_c)))
    do_nonlocal()
    print("\tend_scop_test_spam_a:{}, id:{}".format(spam_a, id(spam_a)))
    print("\tend_scop_test_spam_b:{}, id:{}".format(spam_b, id(spam_b)))
    print("\tend_scop_test_spam_c:{}, id:{}".format(spam_c, id(spam_c)))
    print(") #end scop_test")

scop_test()
~~~

运行结果
~~~bash
function scop_test(
    scop_test_spam_a:scop_spam_a, id:1033610113072
    scop_test_spam_b:scop_spam_b, id:1033610113136
    scop_test_spam_c:scop_spam_c, id:1033610113200
    function do_nonlocal(
        do_nonlocal_spam_b:nonlocal_spam_b, id:1033609969520
        do_nonlocal_spam_c:nonlocal_spam_c, id:1033609969584
        function do_nonlocal(
            before_change_spam_a:scop_spam_a, id:1033610113072
            after_change_spam_a:nonlocal_inner_spam_a, id:1033609970576

            before_change_spam_b:nonlocal_spam_b, id:1033609969520
            after_change_spam_a:nonlocal_inner_spam_b, id:1033609970648

            before_change_spam_c:nonlocal_spam_c, id:1033609969584
            after_change_spam_c:nonlocal_inner_spam_c, id:1033609970720
        ) #end do_nonlocal_inner

        end_do_nonlocal_spam_b:nonlocal_inner_spam_b, id:1033609970648
        end_do_nonlocal_spam_c:nonlocal_inner_spam_c, id:1033609970720
    ) #end do_nonlocal
    end_scop_test_spam_a:nonlocal_inner_spam_a, id:1033609970576
    end_scop_test_spam_b:scop_spam_b, id:1033610113136
    end_scop_test_spam_c:nonlocal_inner_spam_c, id:1033609970720
) #end scop_test
~~~
>* 通过spam_a我们发现, 如果上层函数没有这个变量, 他会去上上层去找. 
>* 通过spam_b我们发现, 如果上层函数和上上层函数同时存在, 只会找上层函数的.这个很好理解上层函数局部变量替换了上上层函数的同名变量
>* 通过spam_c我们发现, 如果上层函数也使用了nonlocal, 我们就可以穿透到上上层. 
