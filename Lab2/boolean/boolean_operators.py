#1
sum1 = 100 + 50     
sum2 = sum1 + 250    
sum3 = sum2 + sum2   

#2
x = 12
y = 5

print(x / y)

#3
numbers = [1, 2, 3, 4, 5]

if (count := len(numbers)) > 3:
    print(f"List has {count} elements")

#4
x = ["apple", "banana"]
y = ["apple", "banana"]
z = x

print(x is z)
print(x is y)
print(x == y)

#5
print(6 ^ 3)