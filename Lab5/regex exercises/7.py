#Write a python program to convert snake case string to camel case string.

txt = input()

words = txt.split('_')
camel = words[0] + ''.join(word.capitalize() for word in words[1:])

print(camel)