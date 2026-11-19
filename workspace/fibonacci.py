#!/usr/bin/env python3
"""Print the first 10 Fibonacci numbers."""


def fibonacci(n: int):
    """Generate the first n Fibonacci numbers.

    Parameters
    ----------
    n : int
        Number of Fibonacci numbers to generate.

    Yields
    ------
    int
        The next Fibonacci number.
    """
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


if __name__ == "__main__":
    for num in fibonacci(10):
        print(num)
