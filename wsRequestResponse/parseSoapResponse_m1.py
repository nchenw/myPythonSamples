import requests
 
 
#response = requests.get('http://asfweb-itn01.tsl.telus.com/PortAssurance/PortAssuranceService?WSDL', verify=False)
#print(response.text)

#url='http://asfweb-itn01.tsl.telus.com/PortAssurance/PortAssuranceService?WSDL'
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
               <Value>20012697590</Value>
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


response = requests.post(url,data=body, auth=('APP_TOCP', 'soaorgid'), verify=False)
stringIn=response.text
#print(stringIn)

import xml.dom.minidom
 
doc = xml.dom.minidom.parseString(stringIn)
 
#print (doc.nodeName)
#print (doc.firstChild.tagName)
#https://docs.python.org/2/library/xml.dom.html
x=doc.getElementsByTagName("CharacteristicValue") 
print(x.length)
#print(x[0].nodeName) 
#print(x[0].childNodes)

#for y in x[1].childNodes:
#	print(y.nodeName)
#	if (y.nodeName =='Characteristic'):
#		for z in y.childNodes:
#			print(z.nodeName) 
#	print(y.firstChild.nodeValue)

#y=doc.getElementsByTagName("Value") 
#print(x.length)

i=0
isuuid=False
isaccesstype=False
uuid=x.length
accesstype=x.length

while i < x.length:
	print('i=',i)
	for y in x[i].childNodes:
		if (y.nodeName =='Characteristic'):
			for z in y.childNodes:
				print('z.nodname=',z.nodeName) 
				
				namev=z.firstChild.nodeValue
				print('node namev =', namev)
				if (namev=='telusChrgBlnceGrpRefId'):
					print('isuuid=True')
					isuuid=i
				if (namev=='telusAccessNetworkTechnologyType'):
					print('isaccesstype=True')
					isaccesstype=i
	i+=1
	
for y in x[isuuid].childNodes:
	if (y.nodeName =='Value'):
		uuid=y.firstChild.nodeValue
		print("uuid=", uuid)
		
for y in x[isaccesstype].childNodes:
	if (y.nodeName =='Value'):
		accesstype=y.firstChild.nodeValue
		print("accesstype=", accesstype)


