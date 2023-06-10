class Jar:
    def __init__(self, capacity=12):
        if capacity < 0:
            raise ValueError
        self._capacity = capacity
        self._n = 0

    def __str__(self):
        return "🍪" * self._n

    def deposit(self, n):
        if self._n + n > self.capacity:
            raise ValueError
        self._n += n

    def withdraw(self, n):
        if self._n < n:
            raise ValueError
        self._n -= n

    @property
    def capacity(self):
        return self._capacity

    @property
    def size(self):
        return self._n

def main():
    jar = Jar(10)
    jar.deposit(6)
    print(jar)
    jar.withdraw(5)
    print(jar)


if __name__ == "__main__":
    main()