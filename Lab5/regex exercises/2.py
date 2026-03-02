#Write a Python program that matches a string that has an 'a' followed by two to three 'b'.

import re

txt = input()

if re.fullmatch(r'ab{2,3}', txt):
    print("Match")
else:
    print("No match")