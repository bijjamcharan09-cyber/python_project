def check_even_odd(number):
    try:
        if number % 2 == 0:
            return "Even"
        else:
            return "Odd"
    except Exception as e:
        print("Error occured",e)

def get_number():
    return int(input("Enter a number: "))


def display_result(number, result):
    print(f"\n{number} is an {result} number.")


def main():
    try:
        while True:
            number = get_number()

            result = check_even_odd(number)

            display_result(number, result)

            choice = input("\nDo you want to continue? (y/n): ").lower()

            if choice == "n":
                print("Program exited.")
                break
    except EOFError:
        print("\nInput terminated.")
    except Exception as e:
        print("An unexpected error occurred:", e)

if __name__ == "__main__":
    main()