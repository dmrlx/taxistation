import time
import random

def my_decorator(deco_arg):
    def wrapper(func):
        def arg_receiver(arg, next_arg):
            start = time.time()
            func(arg, next_arg)
            end = time.time()
            f = open(deco_arg, "a")
            f.write("I receive args: {} and {}. Process length: {} sec.\n".format(arg, next_arg, int(end-start)))
            f.close()
        return arg_receiver
    return wrapper

    pass

@my_decorator("save.dat")
def printer(arg1, arg2):
    time.sleep(random.randint(1, 5))
    print("{} + {} = {}".format(arg1, arg2, arg1+arg2))

printer(2, 3)

