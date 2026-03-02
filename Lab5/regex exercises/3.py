#Write a Python program to find sequences of lowercase letters joined with a underscore.

txt = input()

result = re.findall(r'[a-z]+_[a-z]+', txt)
print(result)