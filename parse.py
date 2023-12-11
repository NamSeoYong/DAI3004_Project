def parse(boundingbox_arr):
    tmp = boundingbox_arr.split(";")   
    arr = [int(i) for i in tmp]
    return arr

tmp = []

with open('text/boundingbox.txt', 'r') as f:
    tmp = parse(f.read())

print(tmp)