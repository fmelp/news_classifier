import json 

records = json.load(open('deduped-data.json')) 

ageToOcc = {"1-10": 0, "10-20": 0, "20-30": 0, "30-40": 0, "40-50": 0, "50+": 0}  

for record in records: 
	try: 
		age = int(record['shooter-details'][0]['age']) 
	except: 
		continue 
	else: 
		if 0 < age and age < 10:
			ageToOcc["1-10"] = ageToOcc["1-10"] + 1
		elif 10 <= age and age < 20:
			ageToOcc["10-20"] = ageToOcc["10-20"] + 1
		elif 20 <= age and age < 30:
			ageToOcc["20-30"] = ageToOcc["20-30"] + 1
		elif 30 <= age and age < 40:
			ageToOcc["30-40"] = ageToOcc["30-40"] + 1
		elif 40 <= age and age < 50:
			ageToOcc["40-50"] = ageToOcc["40-50"] + 1
		elif age >= 50:
			ageToOcc["50+"] = ageToOcc["50+"] + 1


for key in ageToOcc: 
	#gunToShots[key] = gunToShots[gun] / gunToOcc[gun] 
	print "['" + key + "', " + str(ageToOcc[key]) + "],"  

