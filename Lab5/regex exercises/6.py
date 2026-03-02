#Write a Python program to replace all occurrences of space, comma, or dot with a colon.

import re

txt = input()

result = re.sub(r'[ ,.]', ':', txt)
print(result)