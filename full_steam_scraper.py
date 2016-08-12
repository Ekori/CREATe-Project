from collections import defaultdict
#from six.moves import urllib
#import urllib.error
#import urllib.request
import time
import urllib2
import json

def resolve_redirects(url):
    try:
        return urllib2.urlopen(url).geturl()
    except:
#        if e.code == 429:
         time.sleep(5);
         return resolve_redirects(url)
#        raise

def readFile(filename):

        with open(filename) as json_file:
            json_data = json.load(json_file)
        return json_data

def api(param):
	#print param
	info = ""	
	page = urllib2.urlopen(resolve_redirects('http://store.steampowered.com/api/appdetails?appids='+str(param)))
	js = json.load(page)
	for i in js.keys():
		if(js[i]['success']==True):
			if('developers' in js[i]['data'].keys()):
				info += js[i]['data']['developers'][0] + '\t'
			else:
				info += 'none\t'
			if('publishers' in js[i]['data'].keys()):
				info += js[i]['data']['publishers'][0] + '\t'
			else:
				info += 'none\t'
			if('genres' in js[i]['data'].keys()):
				info += js[i]['data']['genres'][0]['description'] + '\t'
			else:
				info += 'none\t'
			if('release_date' in js[i]['data'].keys()):
				info += js[i]['data']['release_date']['date'] + '\t'
			else:
				info += 'none\t'
			if('drm_notice' in js[i]['data'].keys()):
				info += js[i]['data']['drm_notice'] + '\t'
			else:
				info += 'none\t'
			if('dlc' in js[i]['data'].keys()):
				info += "DLC \t"
			else:
				info += 'none\t'
			if('price_overview' in js[i]['data'].keys()):
				info +=  str(js[i]['data']['price_overview']['initial']) + '\t'
			else:
				if(js[i]['data']['is_free']==True):
					info += str(0) + '\t'
				else:
					info += "none\t"
			if('screenshots' in js[i]['data'].keys()):
				info += js[i]['data']['screenshots'][0]['path_thumbnail']
			else:
				info += 'none'
	return info	
		
with open('gametitles.txt') as f:
    content = f.readlines()

js = readFile('appid_to_name.json')

app = defaultdict(set)
for i in js.keys():
	for j in js[i]:
		for x in js[i][j]:
			for y in js[i][j][x]:
				app[y['name']] = y['appid']

out = open('gametitles_to_appid.txt', 'w')
out2 = open('all_games_info.json', 'w')
j = 1
for i in content:
	print j 
	if(i!='\n'):
		c = i[:-1]
		if(app[str(c)]):
		#	print c
			out.write(c + ' ' + str(app[str(c)])+'\n')
			s = api(str(app[str(c)]))
			try:
				out2.write(c + '\t' + str(app[str(c)]) + '\t' + s + '\n')
			except UnicodeEncodeError:
				print "Encoding error in title"
	j += 1
out.close()		
out2.close()

