number = 0

while number < 5:
    print(number)
    number = number + 1



number = 0

while number < 5:
    print(number)
    if number == 3:
        break
    number = number + 1



number = 0

while number < 5:
    print(number)
    if number == 6:
        break
    number = number + 1
else:
    print('No longer < 5')



number = 0

while number < 5:
    print(number)
    if number == 3:
        break
    number = number + 1
else:
    print('No longer < 5')


number = 0

while number < 5:
    print(number)
    if number == 3:
        continue
    number = number + 1
else:
    print('No longer < 5')