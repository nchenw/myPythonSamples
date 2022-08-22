import json
import urllib3
import csv
import requests
import xml.dom.minidom
import warnings
import json

#disable warning message
import warnings
warnings.filterwarnings("ignore")

url2 = 'https://flcncapp-dv14.tsl.telus.com/telus/gem/rest/api/compasstofifa/v1/connectivityload'
jsonrequest= '{"enterpriseCustomerId":"1043413","telephoneNumber":"5874568727","locationId":"1855125","nodeName":"SWPKABU0020DS02","re_type":"DSC_Only","nodeBay":"APB1041","nodeSlot":"4","nodePort":"9","nodeShelf":"1","deviceType":"A7330_ISAM","reName":"SWPKAB01RE02","modelCode":"Alcatel Telecom"}'
request_data=json.loads(jsonrequest)
try:
	r = requests.post(url2, json=request_data,  headers={'Content-Type':'application/json'}, verify=False)
		#To print out json response
	print(r.text)
	if r.status_code != 200:
		print("Failed to send notification, (%d): %s" % (r.status_code, r.text))
except requests.exceptions.RequestException as e:  # This is the correct syntax
	print("error is " + e)