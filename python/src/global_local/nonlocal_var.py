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

