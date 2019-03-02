from urllib.request import urlopen as uo

path = 'ftp://shannon.usu.edu.ru/python/hw2/home.html'

full_names = []
counts = {}
unique_count = 0
count = 0

with uo(path) as site:
    for i in site:
        line = i.decode('cp1251')
        hrf = line.find('href')
        if hrf != -1:
            # print(str[hrf:-1])
            start = line[hrf:-1].find('>') + 1
            name_start = line[hrf:-1][start:]
            name_end_index = name_start.find('<')
            full_name = name_start[0: name_end_index]
            full_names.append(full_name)
            count = count + 1
            name = full_name.split(' ')[1]
            if counts.keys().__contains__(name):
                counts[name] = counts[name] + 1
            else:
                counts[name] = 1
                unique_count = unique_count + 1
            # print(name)

names = counts.keys()
names = sorted(names)
for name in names:
    print(name, counts[name])
print(count, 'people')
print(unique_count, ' unique names')
