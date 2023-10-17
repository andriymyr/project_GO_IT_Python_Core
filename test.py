import re

#text = "andriymyr@gmail"
#text = re.findall(r"[a-zA-Z][a-zA-Z._0-9]+@\w+\.+\w\w+", text)
#print (text==[])

text = input(" ")
pattern = r"[0-9]+"
print(re.match(pattern, text))