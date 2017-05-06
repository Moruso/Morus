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

spam = 'begin_spam'
print("global_spam:{}, id:{}".format(spam, id(spam)))
scope_test()
print("global_spam:{}, id:{}".format(spam, id(spam)))

