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

#DACS Required Notes to check for
required_notes = ["scopecontent", "accessrestrict"]

def get_note_types(resource):
	note_types = []
	for note in resource["notes"]:
		if note["jsonmodel_type"] == ("note_multipart" or "note_singlepart"):
			note_types.append(note["type"])
		else:
			note_types.append(note["jsonmodel_type"])
	return note_types
	
def get_extent_number(resource):
	extent_number = []
	for extent in resource["extents"]:
		if extent["number"]:
			extent_number.append(extent["number"])
		else:
			extent_number.append("false")
	return " , ".join(extent_number)
	
def get_language(resource):
	d = resource
	if 'language' in d:
		return 'language'
	else:
		return "false"

def get_date_types(resource):
	date_types = []
	for date in resource["dates"]:
		if date["date_type"]:
			date_types.append("true")
		else:
			date_types.append("false")
	return date_types

def get_agent_roles(resource):
	agent_roles = []
	for agent in resource["linked_agents"]:
		if agent["role"]:
			agent_roles.append("true")
		else:
			agent_roles.append("false")
	return " , ".join(agent_roles)
	
def makeRow(resource):
	global row
	row = []
	date_list = get_date_types(resource)
	extent_list = get_extent_number(resource)
	agent_list = get_agent_roles(resource)
	notes_list = get_note_types(resource)
	row.append(resource["title"].encode("utf-8"))
	row.append(resource["id_0"])
	row.append(resource["publish"])
	
	if "true" in date_list:
		row.append("true")
	else:
		row.append("false")
		
	if "true" in agent_list:
		row.append("true")
	else:
		row.append("false")
		
	
	# row.append(date_list)
	
	####get text in cell
	# if "creator" in agent_list:
		# row.append(agent_list)
	# else:
		# row.append("false")
		
	
	# for extent_number in extent_list:
		# if extent_list:
			# if extent_number in extent_list:
				# row.append(extent_number)
			# else:
				# row.append("false")
		# else:
			# row.append("false")	
		
			
	# for date_types in date_list:
		# if date_list:
			# if date_types in date_list:
				# row.append("true")
			# else:
				# row.append("false")
		# else:
			# row.append("false")
	
	
	## if 'language' in get_language(resource):
		# row.append(resource.get("language"))
	# else:
		# row.append("false")
	
	if 'language' in get_language(resource):
		row.append("true")
	else:
		row.append("false")
		
	if resource["repository"]:
		row.append("true")
	else:
		row.append("false")
				
	for note in required_notes:
		if notes_list:
			if note in notes_list:
				row.append("true")
			else:
				row.append("false")
		else:
			row.append("false")
	print row
	return row

def main():
	print "Creating a csv"
	writer = csv.writer(open(spreadsheet, "w"))
	column_headings = ["title","resource", "publish", "date", "creator", "language", "repository"] + required_notes
	writer.writerow(column_headings)

	print "Getting a list of resources"
	resourceIds = requests.get(repositoryBaseURL + "/resources?all_ids=true", headers=headers)
	print "Writing rows"
	for resourceId in resourceIds.json():
		resource = (requests.get(repositoryBaseURL + "/resources/" + str(resourceId), headers=headers)).json()
		makeRow(resource)
		writer.writerow(row)
	spreadsheet.close()

main()
