#Create a date object:
import datetime

x = datetime.datetime(2020, 5, 17)

print(x)
#The datetime() class also takes parameters for time and timezone (hour, minute, second, microsecond, tzone), but they are optional, and has a default value of 0, (None for timezone).


#The strftime() Method
#Display the name of the month:
import datetime

x = datetime.datetime(2018, 6, 1)

print(x.strftime("%B"))