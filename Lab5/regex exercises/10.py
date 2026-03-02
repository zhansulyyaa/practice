#Write a Python program to convert a given camel case string to snake case.

import re

txt = input()

result = re.sub(r'([A-Z])', r'_\1', txt).lower()
print(result)