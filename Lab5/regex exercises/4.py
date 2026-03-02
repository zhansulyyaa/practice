#Write a Python program to find the sequences of one upper case letter followed by lower case letters.

import re

txt = input()

result = re.findall(r'[A-Z][a-z]+', txt)
print(result)