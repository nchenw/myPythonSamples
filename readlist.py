#Input: serviceIds.csv, its first column has serviceId 
#Output: the serviceId information will be inserted or updated in migration_copper_details of the env of the url1/2
 
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

 
#Read serviceId from input file

def main():
	i=0
	with open('testdataList.csv') as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		for row in readCSV:
			if(i>0):
				cid =row[0]
				jsonstring='{"enterpriseCustomerId":"'+cid+'",'
				serviceId=row[1]
				jsonstring=jsonstring+'"telephoneNumber":"'+serviceId+'",'
				fms_addressId=row[3]
				fms_region=row[4]
				fms_region=fms_region[-3:]
				fms_addressId=fms_addressId.rjust(9,'0')
				resourceId=row[2]
				print('i=',i)
				loc=get_location_id(fms_addressId, fms_region)
				if (loc!=None):
					jsonstring=jsonstring+'"locationId":"'+loc+'"'					
					s1=get_device_conf(serviceId) 
					s2=get_access_conf(resourceId)
					#Now add those unknown to value null
					otherjstr='"equipmentListCode":"'+row[8]+'","equipmentTypeCode":"'+row[7]+'","mediarMediafAccId":"","picCode":"00000","picReasonCode":"00"'
					jsonstring=jsonstring+s1+','+s2+','+ otherjstr+'}'				
					print('jsonstring=', jsonstring)
					status=load_connectivity(jsonstring)
			i+=1
			
def get_location_id(fms_id, fms_region_id):
	url = 'https://ams-addr-mgmt-it01.paas-app-east-np.tsl.telus.com/v1/resource/address/fms/'
	#002622333/201'
	url=url+fms_id +'/'+fms_region_id
	print(url)
	x = requests.get(url, verify=False)
	#print(x.text)
	loc=json.loads(x.text)

	address =loc.get('Addresses') 
	##print(address[0]['addressId'])
	#print(address[0]['referenceIds']['LPDS_ID'])
	location_id=address[0]['referenceIds']['LPDS_ID']
	return location_id

def get_device_conf(tn):
	url='http://ncrpr.tsl.telus.com:80/PortAssurance/PortAssuranceService?WSDL'
	headers = {'content-type': 'text/xml'}
	body="""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:dto="http://telus/com/portservices/dto" xmlns:java="java:com.netcracker.solutions.customers.telus.mm.integration.portservices.dto">
	<soapenv:Header/>
	<soapenv:Body>
		<dto:searchAssignmentInfo>
		<dto:serviceID>$TN$</dto:serviceID>  
			<dto:customerInfoDTO>
			</dto:customerInfoDTO>
			<dto:ispInfoDTO>
			</dto:ispInfoDTO>
			<dto:checkPendingOrder>false</dto:checkPendingOrder>
		</dto:searchAssignmentInfo>
	</soapenv:Body>
	</soapenv:Envelope>"""
	#tn='4032939046'
	#tn='7804649673'
	#jsonString='"telephoneNumber":"'+tn+'"'
	jsonString=''
	#print('jsonString=' +jsonString)
	body=body.replace('$TN$',tn)
	response = requests.post(url,data=body,headers=headers, verify=False)
	stringIn=response.text

	doc = xml.dom.minidom.parseString(stringIn)
	temp=doc.getElementsByTagName("java:DeviceName")
	nodeName=temp[0].firstChild.nodeValue
	nodeName='"nodeName":"'+nodeName+'"'
	jsonString=jsonString+','+ nodeName



	temp=doc.getElementsByTagName("java:PolicyEngineType")
	re_type=temp[0].firstChild.nodeValue
	if re_type=='DSC_Only':
		re_type='DSC'
	re_type='"reType":"'+re_type+'"'
	jsonString=jsonString+','+ re_type

	temp=doc.getElementsByTagName("java:Bay")
	node_bay=temp[0].firstChild.nodeValue
	node_bay='"nodeBay":"'+node_bay+'"'
	jsonString=jsonString+','+ node_bay



	temp=doc.getElementsByTagName("java:Slot")
	node_slot=temp[0].firstChild.nodeValue
	node_slot='"nodeSlot":"'+node_slot+'"'
	jsonString=jsonString+','+ node_slot

	temp=doc.getElementsByTagName("java:Port")
	node_port=temp[0].firstChild.nodeValue
	node_port='"nodePort":"'+node_port+'"'
	jsonString=jsonString+','+node_port

	temp=doc.getElementsByTagName("java:Shelf")
	node_shelf=temp[0].firstChild.nodeValue
	node_shelf='"nodeShelf":"'+node_shelf+'"'
	jsonString=jsonString+','+ node_shelf


	temp=doc.getElementsByTagName("java:Unit")
	if (temp[0].nodeValue != None):
		node_unit=temp[0].firstChild.nodeValue
		print('node_unit=' , node_unit)
		node_unit='"nodeUnit":"'+node_unit+'"'
	else:
		node_unit='"nodeUnit":""'
	jsonString=jsonString+','+node_unit

	temp=doc.getElementsByTagName("java:DeviceType")
	device_type=temp[0].firstChild.nodeValue
	device_type='"deviceType":"'+device_type+'"'
	jsonString=jsonString+','+device_type



	temp=doc.getElementsByTagName("java:DeviceName")
	re_name=temp[1].firstChild.nodeValue
	re_name='"reName":"'+re_name+'"'
	jsonString=jsonString+','+re_name

	temp=doc.getElementsByTagName("java:DeviceManufacturer")
	mode_code=temp[0].firstChild.nodeValue
	mode_code='"modelCode":"'+mode_code+'"'
	jsonString=jsonString+','+mode_code

	#print('jsonString=' +jsonString)
	return jsonString

def get_access_conf(resourceId):
	url='https://soa-mp-kidcoss-pr.tsl.telus.com:443/SMO/InventoryMgmt/RetrieveServiceConfiguration_v1_1_vs0?WSDL'
	headers = {'content-type': 'text/xml'}
	body="""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ret="http://www.ibm.com/xmlns/prod/websphere/fabric/2008/12/telecom/operations/inventory/types/schema/RetrieveServiceConfiguration" xmlns:v3="http://www.ibm.com/telecom/common/schema/mtosi/v2_0">
	   <soapenv:Header/>
	   <soapenv:Body>
		  <ret:retrieveServiceConfiguration>
			 <sourceCriteria>
				<CharacteristicValue>
				   <Characteristic>
					  <Name>telusServiceInstanceReferenceId</Name>
				   </Characteristic>
				   <Value>$RSID$</Value>
				</CharacteristicValue>
				<CharacteristicValue>
				   <Characteristic>
					  <Name>telusSourceSystem</Name>
				   </Characteristic>
				   <Value>compass</Value>
				</CharacteristicValue>
				<Specification>
				   <Name>WSIR</Name>
				   <Type>Directory</Type>
				   <Category>Resource Facing Service</Category>
				</Specification>
			 </sourceCriteria>
			 <targetCriteria>
				<CharacteristicValue>
				   <Characteristic>
					  <Name>returnStaticIPInfo</Name>
				   </Characteristic>
				   <Value>true</Value>
				</CharacteristicValue>
				<CharacteristicValue>
				   <Characteristic>
					  <Name>returnChargingBalanceGroupInfo</Name>
				   </Characteristic>
				   <Value>true</Value>
				</CharacteristicValue>
		   </targetCriteria>
		  </ret:retrieveServiceConfiguration>
	   </soapenv:Body>
	</soapenv:Envelope>"""

	#resourceId='20012697590'
	body=body.replace('$RSID$',resourceId)
	response = requests.post(url,data=body, auth=('APP_TOCP', 'soaorgid'), verify=False)
	stringIn=response.text

	jsonString=''
	doc = xml.dom.minidom.parseString(stringIn)
	x=doc.getElementsByTagName("CharacteristicValue") 

	i=0
	isuuid=-1
	isaccesstype=-1
	while i < x.length:
		for y in x[i].childNodes:
			if (y.nodeName =='Characteristic'):
				for z in y.childNodes:
					namev=z.firstChild.nodeValue
					if (namev=='telusChrgBlnceGrpRefId'):
						isuuid=i
					if (namev=='telusAccessNetworkTechnologyType'):
						isaccesstype=i
		i+=1
	if (isuuid>0):	
		for y in x[isuuid].childNodes:
			if (y.nodeName =='Value'):
				uuid=y.firstChild.nodeValue 
				if(uuid !=None):
					jsonString=jsonString +'"wsirUuid" : "'+uuid+'",'
	else:
		jsonString=jsonString +'"wsirUuid" : "",'
	if(isaccesstype>0):		
		for y in x[isaccesstype].childNodes:
			if (y.nodeName =='Value'):
				accesstype=y.firstChild.nodeValue
				#jsonString=jsonString+'"equipmentTypeCode" : "'+accesstype+'"'
				if(accesstype !=None):
					jsonString=jsonString+'"accessTechnologyType":"'+accesstype+'"'
	else:
		jsonString=jsonString+'"accessTechnologyType":""'
	return jsonString
	
def load_connectivity(jsonrequest):
	url2 = 'https://flcncapp-dv14.tsl.telus.com/telus/gem/rest/api/compasstofifa/v1/connectivityload'
	#url2 = 'https://flcncapp-itn03.tsl.telus.com/telus/gem/rest/api/compasstofifa/v1/connectivityload'
	request_data=json.loads(jsonrequest)
	try:
		r = requests.post(url2, json=request_data,  headers={'Content-Type':'application/json'}, verify=False)
			#To print out json response
		print(r.text)
		if r.status_code != 200:
			print("Failed to send notification, (%d): %s" % (r.status_code, r.text))
	except requests.exceptions.RequestException as e:  # This is the correct syntax
		print("error is " + e)
	return r.status_code
			
if __name__ == "__main__":
    main()
		
