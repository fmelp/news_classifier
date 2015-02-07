import sys
import csv
import json
import pickle
from datetime import datetime

output = csv.writer(open('gun-article-info.csv', 'w'))

headers = ['url', 'city', 'state', 'text', 'title', 'date', 'people', 'cities', 'states']

output.writerow(headers)

colors = {'Person' : '#6495ED'}

for row in csv.DictReader(open(sys.argv[1])) : 
	text = row['text']
	if not(row['entities'] == 'NA' or row['keywords'] == 'NA'):
		entities = json.loads(row['entities'])
		datestr = ''
		if not(row['date'] == '') : 
			date = datetime.strptime(row['date'], '%Y%m%dT%H%M%S')
			datestr = '%s/%s/%s'%(date.month, date.day, date.year)
		for e in entities:
			text = text.replace('%s'%e['text'], '<span class=%s>%s</span>'%(e['type'],e['text']))
		for e in json.loads(row['keywords']):
			text = text.replace(' %s '%e['text'], ' <span class=Keyword>%s</span> '%(e['text']))
		output.writerow([row['url'], row['city'], row['state'], text, row['title'], datestr,
			', '.join([e['text'].encode('ascii', 'ignore') for e in entities if e['type'] == 'Person']),
			', '.join([e['text'].encode('ascii', 'ignore') for e in entities if e['type'] == 'City']),
			', '.join([e['text'].encode('ascii', 'ignore') for e in entities if e['type'] == 'StateOrCounty'])])

