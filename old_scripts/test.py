

import json

filename = 'test.json'

with open(filename) as json_data:
    d = json.load(json_data)
    a = d['57690']
    x = a['data']


for i in x:
	print (str(i) + " " + str(x[i]))
#	print (a[i])
