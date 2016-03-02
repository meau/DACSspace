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

def makeRow(resource):
	global row
	row = []
	notes_list = get_note_types(resource)
	row.append(resource["title"].encode("utf-8"))
	row.append(resource["id_0"])
	row.append(resource["publish"])
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
	column_headings = ["title","resource", "publish"] + required_notes
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
