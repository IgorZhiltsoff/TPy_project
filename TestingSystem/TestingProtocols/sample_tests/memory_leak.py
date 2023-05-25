class MyClass:
    def __init__(self):
        self.arr = list(range(10000000))


def func():
    a = MyClass()
    b = MyClass()
    a.ref = b
    b.ref = a
    return a


func()
func()
func()
func()
func()
func()
func()
func()
func()
func()
func()
func()
func()

print("I ate all your ram")
