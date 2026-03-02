#Write a Python program that matches a string that has an 'a' followed by zero or more 'b''s.

import re

txt = input()

if re.fullmatch(r'ab*', txt):
    print("Match")
else:
    print("No match")