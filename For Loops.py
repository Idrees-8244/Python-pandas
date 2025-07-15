# For loops


integers = [1,2,3,4,5]

for numbers in integers:
    print(numbers)



integers = [1,2,3,4,5]

for numbers in integers:
    print('yep!')



integers = [1,2,3,4,5]

for sami in integers:
    print(sami + sami)



ice_cream_dict = {'name': ' Md Sami', ' weekly working' : 6, 'hours' 'loves coding': ['python', 'SQL' ]}

for cream in ice_cream_dict.values():
    print(cream)




ice_cream_dict = {'name': ' Md Sami', ' weekly working' : 6, 'hours' 'loves coding': ['python', 'SQL' ]}

for key, value in ice_cream_dict.items():
    print(key, '-<', value)



# Nested For Loops


colleges = ['veda' ,'success','aurora']
school = ['Hyd','vikas','madina']
for one in colleges:
    for two in school:
        print(one,'topped with', two)