name = input("Enter your name: ")

weight = int(input ("Enter your weight in pounds:"))


height = int(input ("Enter your height in inches:"))

BMI = (weight * 703) / (height * height )

print(BMI)

if BMI > 0 :
    if(BMI< 18.5):
        print(name + ", You are underweight minimal")
    elif (BMI<= 24.9):
        print(name + ", You are Normal weight")
    elif (BMI<= 29.9):
        print(name + ", You are Overweight")
    elif (BMI<= 34.9):
        print(name + ", You are Obese High")
    elif (BMI<= 39.9):
        print(name + ", Severely Obese Very High")
    else:
        print(name + ", Severely Obese Very High")

else:
    print("Enter valid input")