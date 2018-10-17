class Class(object):
    classhennsuu = 0

    def __init__(self):
        self.instancehensuu = 1

    def prpr(self):
        print(self.classhennsuu, self.instancehensuu)


def main():
    c = Class()
    c.prpr()

    print(c.classhennsuu, c.instancehensuu)

    print(Class.classhennsuu)

if __name__ == "__main__":
    main()