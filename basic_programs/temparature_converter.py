def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9


def celsius_to_kelvin(celsius):
    return celsius + 273.15


def kelvin_to_celsius(kelvin):
    return kelvin - 273.15


def main():
    while True:
        print("-"*21 + "\nTemperature Converter\n" + "-"*21)
        print("1. Celsius to Fahrenheit")
        print("2. Fahrenheit to Celsius")
        print("3. Celsius to Kelvin")
        print("4. Kelvin to Celsius")
        print("5. Quit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            try:
                value = float(input("Enter Celsius: "))
                print(f"{value} °Celsius = {celsius_to_fahrenheit(value):.2f} °F")
            except ValueError:
                print("Invalid number.")
        elif choice == "2":
            try:
                value = float(input("Enter Fahrenheit: "))
                print(f"{value} °Farenhit = {fahrenheit_to_celsius(value):.2f} °C")
            except ValueError:
                print("Invalid number.")
        elif choice == "3":
            try:
                value = float(input("Enter Celsius: "))
                print(f"{value} °Celsius = {celsius_to_kelvin(value):.2f} K")
            except ValueError:
                print("Invalid number.")
        elif choice == "4":
            try:
                value = float(input("Enter Kelvin: "))
                print(f"{value} Kelvin = {kelvin_to_celsius(value):.2f} °C")
            except ValueError:
                print("Invalid number.")
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
        print()


if __name__ == "__main__":
    main()