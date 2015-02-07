import json 

records = json.load(open('deduped-data.json')) 

cityToOcc = {} 

for record in records:
	try:
		city = str(record['shooting-details']['location']['city']).lower()
		detail = record['shooting-details']['details']
		detail = [str(x) for x in detail]
	except:
		continue
	else: 
		if ('The incident was a case of domestic violence.' in detail): 
			if (city in cityToOcc):
				cityToOcc[city] = cityToOcc[city] + 1 
			else:
				cityToOcc[city] = 1

for key in cityToOcc: 
	print ("[ '" + key + "', " + str(cityToOcc[key]) + "],")