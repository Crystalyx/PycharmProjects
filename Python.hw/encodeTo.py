filename = input('Enter input file name: ')
outfilename = input('Enter output file name: ')
encoding = input('Enter encoding: ')

with open(filename, 'r') as f:
    with open(outfilename, 'w', encoding=encoding) as o:
        for l in f:
            o.write(l)
