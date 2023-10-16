import re

text = "andriymyr@gmail"
text = re.findall(r"[a-zA-Z][a-zA-Z._0-9]+@\w+\.+\w\w+", text)
print (text==[])