#!/usr/bin/env python3

import chevron
import os
import json

info = {'categories': []}

mapTemplate = ''
with open('template/map.html.mustache', 'r') as f:
	mapTemplate = f.read()

for category in os.listdir('maps'):
	print('Found a category:', category)

	categoryDict = None
	with open(f'maps/{category}/{category}.json', 'r') as f:
		categoryDict = json.load(f)
	categoryDict['id'] = category
	categoryDict['maps'] = []

	for map in [f.name for f in os.scandir('maps/' + category) if f.is_dir()]:
		print('Found a map:', map)

		mapDict = dict()
		path = f'maps/{category}/{map}'
		j = None
		with open(f'{path}/{map}.json') as f:
			j = json.load(f)

		mapDict['name'] = map
		mapDict['author'] = j['author']
		mapDict['description'] = j['description']
		mapDict['path'] = path
		mapDict['tags'] = [{'tag': tag} for tag in j['tags']]

		with open(f'{path}/index.html', 'w') as f:
			html = chevron.render(mapTemplate, mapDict)
			print(len(html))
			f.write(html)

		categoryDict['maps'].append(mapDict)

	info['categories'].append(categoryDict)

print(info)

with open('template/index.html.mustache', 'r') as indexTemplate, open('index.html', 'w') as f:
	f.write(chevron.render(indexTemplate, info))
