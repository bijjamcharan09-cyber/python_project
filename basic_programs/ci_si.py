def CI():
    """
    This function is used to calculate the compound interest.
    """
    principal = float(input("Enter the principal amount: "))
    rate1 = float(input("Enter the rate of interest (in rupees): "))
    rate = rate1*12
    time1 = float(input("Enter the time (in months): "))
    time = time1/12
    
    # Calculate compound interest
    amount = principal * (1 + rate / 100) ** time
    compound_interest = amount - principal
    print("-"*35)
    print(f"The compound interest is: {compound_interest:.2f}")
    print("-"*35)

def SI():
    """
    This function is used to calculate the simple interest.
    """
    principal = float(input("Enter the principal amount: "))
    rate1 = float(input("Enter the rate of interest (in rupees): "))
    rate = rate1*12
    time1 = float(input("Enter the time (in months): "))
    time = time1/12
    
    # Calculate simple interest
    simple_interest = (principal * rate * time) / 100
    print("-"*35)
    print(f"The simple interest is: {simple_interest:.2f}")
    print("-"*35)

def total_amount(principal, interest):
    """
    This function is used to calculate the total amount after adding the interest to the principal.
    """
    total = principal + interest
    return total

def main():
    print("Welcome to the Interest Calculator!")
    print("__________________\nIntrest calculator\n__________________")
    while True:
        print("1. Calculate Compound Interest")
        print("2. Calculate Simple Interest")
        print("3. Total Amount")
        print("4. Exit")

        choice = input("Enter your choice  : ")
    
        if choice == '1':
            CI()
        elif choice == '2':
            SI()
        elif choice == '3':
            principal = float(input("Enter the principal amount: "))
            interest = float(input("Enter the interest amount: "))
            total = total_amount(principal, interest)
            print("-"*35)
            print(f"The total amount is: {total:.2f}")
            print("-"*35)
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
        

if __name__ == "__main__":
    main()