#List comprehension vs generator expression:
# List comprehension - creates a list
list_comp = [x * x for x in range(5)]
print(list_comp)
# Generator expression - creates a generator
gen_exp = (x * x for x in range(5))
print(gen_exp)
print(list(gen_exp))


#Using a generator expression with sum:
# Calculate sum of squares without creating a list
total = sum(x * x for x in range(10))
print(total)