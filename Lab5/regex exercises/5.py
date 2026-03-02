#Write a Python program that matches a string that has an 'a' followed by anything, ending in 'b'.

txt = input()

if re.fullmatch(r'a.*b', txt):
    print("Match")
else:
    print("No match")