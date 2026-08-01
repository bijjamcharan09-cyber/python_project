def largest_of_three(a, b, c):
    """Return the largest of three numeric values."""
    return a if a >= b and a >= c else (b if b >= c else c)


def smallest_of_three(a, b, c):
    """Return the smallest of three numeric values."""
    return a if a <= b and a <= c else (b if b <= c else c)

def read_number(prompt):
    """Read a number from input, raise ValueError on invalid input."""
    s = input(prompt)
    try:
        if '.' in s:
            return float(s)
        return int(s)
    except ValueError:
        raise ValueError(f"Invalid number: {s!r}")


def main():
    while True:
        try:
            print("-"*15 + "\n Enter numbers \n" + "-"*15)
            a = read_number('Enter first number: ')
            b = read_number('Enter second number: ')
            c = read_number('Enter third number: ')
        except ValueError as e:
            print('Error:', e)
            return

        smallest = smallest_of_three(a, b, c)
        largest = largest_of_three(a, b, c)
        print('Smallest number is:', smallest)
        print('Largest number is:', largest)
        choice = input("Do you want to continue (y/n):")
        if choice == 'n':
            print("Exiting...")
            break

if __name__ == '__main__':
    main()