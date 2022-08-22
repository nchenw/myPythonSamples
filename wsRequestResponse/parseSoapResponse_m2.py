import requests

 
 
#response = requests.get('http://asfweb-itn01.tsl.telus.com/PortAssurance/PortAssuranceService?WSDL', verify=False)
#print(response.text)

#url='http://asfweb-itn01.tsl.telus.com/PortAssurance/PortAssuranceService?WSDL'
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
tn='7804649673'
body=body.replace('$TN$',tn)
response = requests.post(url,data=body,headers=headers, verify=False)
stringIn=response.text
print(stringIn)

#import os
#if os.path.exists("Myxml.xml"):
#  os.remove("Myxml.xml")

##print(stringIn) > Myxml.xml
#f = open("Myxml.xml", "a")
#f.write(stringIn)
#f.close()

import xml.dom.minidom
#doc = xml.dom.minidom.parse("Myxml.xml")
doc = xml.dom.minidom.parseString(stringIn)
# print out the document node and the name of the first child tag
print (doc.nodeName)
print (doc.firstChild.tagName)

temp=doc.getElementsByTagName("java:PolicyEngineType")
print(temp.length)
re_type=temp[0].firstChild.nodeValue


print('re_type='+re_type)
temp=doc.getElementsByTagName("java:Bay")
#print(bay.length)
node_bay=temp[0].firstChild.nodeValue
print('node_bay='+node_bay)
temp=doc.getElementsByTagName("java:Slot")
node_slot=temp[0].firstChild.nodeValue
print('node_slot='+node_slot)
temp=doc.getElementsByTagName("java:Port")
node_port=temp[0].firstChild.nodeValue
print('node_port='+node_port)
temp=doc.getElementsByTagName("java:Shelf")
node_shelf=temp[0].firstChild.nodeValue
print('node_shelf='+node_shelf)
temp=doc.getElementsByTagName("java:Unit")
#print(temp.length)

#node_unit=temp[0].firstChild.nodeValue
#print('node_unit='+node_unit)
if (temp[0].nodeValue != None):
	node_unit=temp[0].firstChild.nodeValue
	print('node_unit='+node_unit)

temp=doc.getElementsByTagName("java:DeviceType")
device_type=temp[0].firstChild.nodeValue
print('device_type='+device_type)




temp=doc.getElementsByTagName("java:DeviceName")
re_name=temp[1].firstChild.nodeValue
print('re_name='+re_name)


temp=doc.getElementsByTagName("java:DeviceManufacturer")
mode_code=temp[0].firstChild.nodeValue
print('mode_code='+mode_code)