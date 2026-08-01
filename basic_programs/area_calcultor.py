import math

def area_circle(radius):
	return math.pi * radius * radius

def area_rectangle(length, width):
	return length * width

def area_triangle(base, height):
	return 0.5 * base * height

def area_square(side):
	return side * side

def get_positive(prompt):
	while True:
		try:
			v = float(input(prompt))
			if v > 0:
				return v
		except ValueError:
			pass
		print('Enter a number greater than 0.')

def main():
	while True:
		print("-"*15 + "\nArea Calculator\n" + "-"*15)
		print("1. circle")
		print("2. Rectangle")
		print("3. Triangle")
		print("4. Square")
		print("5. Exit")
		choice = input("Enter your choice (1-5):")
		if choice == "1":
			radius = int(input("Enter Radius of circle:"))
			result = area_circle(radius)
			print("Area of Circle = ",result)
		elif choice == "2":
			length = int(input("Enter length of Rectangle:"))
			width = int(input("Enter width of Rectangle:"))
			result = area_rectangle(length, width)
			print("Area of Rectangle = ",result)
		elif choice == "3":
			base = int(input("Enter base of Triangle:"))
			height = int(input("Enter height of Triangle:"))
			result = area_triangle(base, height)
			print("Area of Triangle = ",result)
		elif choice == "4":
			side = int(input("Enter the side of Square:"))
			result = area_square(side)
			print("Area of Square = ",result)
		elif choice == "5":
			print("Exiting...")
			break
		else:
			print("Enter valid choice!")
if __name__ == '__main__':
	main()