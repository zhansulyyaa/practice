#Print a list of all matches:

import re

txt = "The rain in Spain"
x = re.findall("ai", txt)
print(x)


#Return an empty list if no match was found:

import re

txt = "The rain in Spain"
x = re.findall("Portugal", txt)
print(x)