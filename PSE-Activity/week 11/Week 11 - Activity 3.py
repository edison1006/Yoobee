import doctest
def add(a, b):
    """
    Adds two numbers and returns the result.

    >>> add(2, 3)
    5
    >>> add(-1, 1)
    0
    >>> add(-1, -1)
    -2
    """
    return a + b

def subtract(a, b):
    """
    Subtracts b from a and returns the result.

    >>> subtract(5, 3)
    2
    >>> subtract(3, 5)
    -2
    >>> subtract(-1, -2)
    1
    """
    return a - b

def times(a, b):
    """
    Multiplies two numbers and returns the result.

    >>> times(2, 3)
    6
    >>> times(1, -1)
    -1
    >>> times(-1, -1)
    1
    """
    return a * b

def divide(a, b):
    """
    Divides a by b and returns the result.

    >>> divide(6, 3)
    2.0
    >>> divide(-6, 3)
    -2.0
    >>> divide(-6, -3)
    2.0
    >>> divide(1, 0)
    Traceback (most recent call last):
    ...
    ValueError: Cannot divide by zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def modulus(a, b):
    """
    Returns the remainder of dividing a by b.

    >>> modulus(10, 3)
    1
    >>> modulus(7, 7)
    0
    >>> modulus(8, -3)
    -1
    >>> modulus(5, 0)
    Traceback (most recent call last):
    ...
    ValueError: Cannot take modulus with zero divisor
    """
    if b == 0:
        raise ValueError("Cannot take modulus with zero divisor")
    return a % b

if __name__ == "__main__":
    print("Running doctests for Week11_Activity1...\n")
    doctest.testmod(verbose=True)
