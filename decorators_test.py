import time
import random


def my_decorator(deco_arg):
    def wrapper(func):
        def arg_receiver(arg):
            start = time.time()
            if isinstance(arg, int):
                func(arg)

            if isinstance(arg, str):
                summ = 0
                for char in arg:
                    summ += ord(char)
                func(summ)
            end = time.time()
            f = open(deco_arg, "a")
            f.write("Arg is \"{}\". Process length: {} sec.\n".format(arg, int(end-start)))
            f.close()
        return arg_receiver
    return wrapper


@my_decorator("save.dat")
def printer(arg1):
    time.sleep(random.randint(1, 5))
    print(arg1 ** 2)

printer(3)
printer("and")
