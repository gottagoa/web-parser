import time

def func1(x):
    print(x**2)
    time.sleep(3)
    print('func1 завершен')

def func2(x):
    print(x**2)
    time.sleep(3)
    print('func2 завершен')

def main():
    func1(4)
    func2(4)

main()




