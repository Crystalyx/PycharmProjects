import re

line = "Hello how are you you are you"
it = re.findall(r"\w+", line)
re.
print(it)
dict = {}
for i in it:
    if i not in dict:
        dict[i] = 1
    else:
        dict[i] = dict[i] + 1

for e in dict:
    if dict[e] == 3:
        print(e)
