#!/usr/bin/python2
import json
import os
import urllib

# Base url for all rest requests
author = ""
server = "https://aur.archlinux.org/"
query = "rpc.php?type=msearch&arg=" + author
base_url = server + query

values = json.load(urllib.urlopen(base_url))

for result in values['results']:
	name = result['Name']
	os.system("cower -df %s" % name)

