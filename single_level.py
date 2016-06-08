#!/usr/bin/env python

import os, requests, json, ConfigParser, csv
from codecs import encode

config = ConfigParser.ConfigParser()
config.read("local_settings.cfg")

dictionary = {"baseURL": config.get("ArchivesSpace", "baseURL"), "repository":config.get("ArchivesSpace", "repository"), "user": config.get("ArchivesSpace", "user"), "password": config.get("ArchivesSpace", "password")}
repositoryBaseURL = "{baseURL}/repositories/{repository}".format(**dictionary)
resourceURL = "{baseURL}".format(**dictionary)

# authenticates the session
auth = requests.post("{baseURL}/users/{user}/login?password={password}&expiring=false".format(**dictionary)).json()
headers = {"X-ArchivesSpace-Session":auth["session"]}

spreadsheet = os.path.join(config.get("Destinations", "directory"), config.get("Destinations", "filename"))

	notes = resource["notes"]
	content_list = []
	for note in notes:
		try:
				if note["jsonmodel_type"] == "note_singlepart":
					content_list.append(note["content"].encode('utf-8'))
				else:
					content_list.append(note["subnotes"][0]["content"].encode('utf-8'))
		except:
			pass
	return ", ".join(content_list)

def get_values(resource, array, value):
	value_types = []
	for item in resource[array]:
		if item[value]:
			value_types.append(item[value])
		else:
			value_types.append("false")
	return ", ".join(value_types)

def get_single_value(resource, key):
	d = resource
	if key in d:
		return d.get(key)
	else:
		return "false"

def makeRow(resource):
	global row
	row = []
	publish = get_single_value(resource, "publish")
	title = get_single_value(resource, "title")
	resourceId = get_single_value(resource, "id_0")
	extent = get_values(resource, "extents", "number")
	date = get_values(resource, "dates", "date_type")
	agent = get_values(resource, "linked_agents", "role")
	language = get_single_value(resource, "language")
	repository = get_single_value(resource, "repository")
	required_values = title, resourceId, extent, date, language
	required_notes = scope, access

	for item in required_values:
		if item != "false": 
			row.append(item.encode('utf-8'))
		else:
			row.append("false")	

	if repository:
		response = requests.get(repositoryBaseURL, headers=headers).json()
		row.append(response["name"])
	else:
		row.append("false")			

	if "creator" in agent:
		creator_list = []
		for item in resource["linked_agents"]:
			response = requests.get(resourceURL + item["ref"], headers=headers).json()
			for item in response["names"]:
				creator_list.append(item["sort_name"])
		row.append(", ".join(creator_list).encode('utf-8'))
	else:
		row.append("false")
							
	for item in required_notes:
		if item:
			row.append(item)
		else:
			row.append("false")
	
	print row

def main():
	print "Creating a csv"
	writer = csv.writer(open(spreadsheet, "wb"))
	column_headings = ["title", "resource", "extent", "date", "language", "repository", "creator", "scope", "restrictions"]
	writer.writerow(column_headings)

	print "Getting a list of resources"
	resourceIds = requests.get(repositoryBaseURL + "/resources?all_ids=true", headers=headers)
	print "Writing rows"
	for resourceId in resourceIds.json():
			resource = (requests.get(repositoryBaseURL + "/resources/" + str(resourceId), headers=headers)).json()
			if resource["publish"]:
				makeRow(resource)
				writer.writerow(row)
	spreadsheet.close()

main()
