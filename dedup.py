import json
import datetime

records = json.load(open('aggregated-data.json')) 

deduped = []

def can_merge(this, that): 
	count = 0 
	#shooter
	thisSD = this['shooter-details'] 
	if (len(thisSD) > 0):
		thisSN1 = thisSD[0] 
		thisSN2 = thisSN1['name']
		thatSD = that['shooter-details'] 
		if (len(thatSD) > 0):
			thatSN1 = thatSD[0] 
			thatSN2 = thatSN1['name']
			if (thisSN2 == "unknown" or thatSN2 == "unknown"): 
				count = count + 1 
			elif (thisSN2 == thatSN2):
				count = count + 1 
	
	#victim
	thisVD = this['victim-details']
	if (len(thisVD) > 0):
		thisVN1 = thisVD[0] 
		thisVN2 = thisVN1['name'] 
		thatVD = that['victim-details'] 
		if (len(thatVD) > 0):
			thatVN1 = thatVD[0] 
			thatVN2 = thatVN1['name'] 

			if (thisVN2 == thatVN2): 
				count = count + 1 

	#date 
	thisD = this['shooting-details'] 
	thisT = thisD['time'] 
	thisDate = thisT['date'] 
	thatD = that['shooting-details'] 
	thatT = thatD['time'] 
	thatDate = thatT['date'] 
	if (thisDate == thatDate): 
		count = count + 1 
	if (count >= 2): 
		return True 
	else: 
		return False 

deduped.append(records[0]) 

for this_record in records: 
	merged = False 
	for that_record in deduped: 
       #update fields in deduped with new information added by this_record
  		if can_merge(this_record, that_record): 
  			merged = True
       		thisD = this_record['shooting-details'] 
       		thisT = thisD['time'] 
       		thisDate = thisT['date'] 
       		thatD = that_record['shooting-details'] 
       		thatT = thatD['time'] 
       		thatDate = thatT['date'] 
       		thisDateSplit = thisDate.split('/') 
       		thatDateSplit = thatDate.split('/')
       		
       		dateThis = None
       		dateThat = None

       		try: 
       			dateThis = datetime.date(int(thisDateSplit[2]), int(thisDateSplit[0]), int(thisDateSplit[1])) 
       			dateThat = datetime.date(int(thatDateSplit[2]), int(thatDateSplit[0]), int(thatDateSplit[1]))
       		except Exception: 
       			continue 

       		if (dateThis > dateThat): 
       			print "herehreredws"
       			that_record['article'] = this_record['article'] 
       			that_record['shooter-details'] = this_record['shooter-details']
       			that_record['shooting-details'] = this_record['shooting-details']


	if (not merged) : 
		deduped.append(this_record)


json.dump(deduped, open('deduped-data.json', 'w'))
