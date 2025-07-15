def first_func(): 
    print("we did it")

first_func()


def number_sq(number):
    print(number**2)
    
number_sq(5)


def number_sq_cust(number,power):
    print(number**power)

number_sq_cust(5,3)



def number_agrs(*number):
    print(number[0]*number[1])

number_agrs(5,6,1,2,8)


agrs_tuple = (5,6,1,2,8)

def number_agrs(*number):
    print(number[0]*number[1])

number_agrs(*agrs_tuple)



def number_sq_cust(number,power):
    print(number**power)

number_sq_cust(power = 5,number = 3)



