import json 

records = json.load(open('deduped-data.json')) 

cityToOcc = {} 

for record in records:
	try:
		city = str(record['shooting-details']['location']['city']).lower()
	except:
		continue
	else: 
		if (city in cityToOcc): 
			cityToOcc[city] = cityToOcc[city] + 1 
		else:
			cityToOcc[city] = 1

for key in cityToOcc: 
	print ("[ '" + key + "', " + str(cityToOcc[key]) + "],")




