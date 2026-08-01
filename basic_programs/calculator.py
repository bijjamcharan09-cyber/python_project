def add(a, b):
	return a + b

def subtract(a, b):
	return a - b

def multiply(a, b):
	return a * b

def divide(a, b):
	if b == 0:
		return "Error! Cannot divide by zero."
	return a / b

def exponent(a,b):
	if b==0:
		result=1
		return result
	else:
		return a**b

def display_menu():
	print("\n----- Calculator -----")
	print("1. Addition")
	print("2. Subtraction")
	print("3. Multiplication")
	print("4. Division")
	print("5. Exponent")
	print("6. Exit")

def main():
	while True:
		display_menu()

		choice = input("Enter your choice (1-6): ")  

		if choice == "6":  
			print("Thank you for using Calculator!")  
			break  

		if choice not in ["1", "2", "3", "4", "5"]:  
			print("Invalid choice. Please try again.")  
			continue  

		try:  
			num1 = float(input("Enter first number: "))  
			num2 = float(input("Enter second number: "))  
		except ValueError:  
			print("Please enter valid numbers.")  
			continue  

		if choice == "1":  
			result = add(num1, num2) 
			print("-"*15) 
			print(f"Result = {result}") 
			print("-"*15)  

		elif choice == "2":  
			result = subtract(num1, num2)  
			print("-"*15) 
			print(f"Result = {result}")  
			print("-"*15) 

		elif choice == "3":  
			result = multiply(num1, num2)  
			print("-"*15) 
			print(f"Result = {result}")  
			print("-"*15) 

		elif choice == "4":  
			result = divide(num1, num2) 
			print("-"*15)  
			print(f"Result = {result}")
			print("-"*15)   

		elif choice == "5":  
			result = exponent(num1,num2)  
			print("-"*20) 
			print (f"Exponentiation = {result}")
			print("-"*20) 

if __name__ == "__main__":
	main()