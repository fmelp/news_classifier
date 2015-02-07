import sys
import urllib2
import json 
import csv

#api_key = 'd18dab77eed984e5982cc2973fedd9a02c342411'
#api_key = '87feec954e195b43fa85db60bfa2ad51a899e479'
api_key = '9814112249d7c0d6f22b778837e86f6789f2ff73'
request = 'http://access.alchemyapi.com/calls/url/URLGetCombinedData?apikey=%s&url=%s&extract=title,pub-date,entity,keyword,text&outputMode=json'
textRequest = 'http://access.alchemyapi.com/calls/url/URLGetText?apikey=%s&url=%s&outputMode=json'

def get_text(url) : 
	try : entities = urllib2.urlopen(textRequest%(api_key, url))
	except urllib2.HTTPError : sys.stderr.write('BAD REQUEST\n'); return None
	try : response = json.loads(entities.read())
	except ValueError : sys.stderr.write('JSON ERROR\n'); return None
	print url, response['status']
	if response['status'] == 'OK' : 
		txt = response['text'].encode('ascii', 'ignore').split('\n')
		return ' '.join(['<p>%s</p>'%l.strip() for l in txt if not(l.strip() == '')])
	return None

def get_fields(url) : 
	try : data = urllib2.urlopen(request%(api_key, url))
	except urllib2.HTTPError : sys.stderr.write('BAD REQUEST\n'); return None
	#print data.read()
	try : response = json.loads(data.read())
	except ValueError : sys.stderr.write('JSON ERROR\n'); return None
	if response['status'] == 'OK' : 
		title = response['title'].encode('ascii', 'ignore')
		date = response['publicationDate']['date'].encode('ascii', 'ignore')
		entities = json.dumps(response['entities'])
		keywords = json.dumps(response['keywords'])
		return title, date, entities, keywords
	return None

output = csv.writer(open('gun-violence-urls-and-entitites.csv', 'w'))
output.writerow(['url', 'city', 'state', 'title', 'date', 'text', 'entities', 'keywords'])

for url in sys.stdin : 
	url, state, city = url.strip().split('\t')
	#sys.stderr.write(url+'\n')
	txt = get_text(url)
	#print txt
	if txt : 
		fields = get_fields(url)
		if fields : 
			title, date, entities, kws = fields
			output.writerow([url, city, state, title, date, txt, entities, kws])
		else : 
			output.writerow([url, city, state, "NA", "NA", txt, "NA", "NA"])


