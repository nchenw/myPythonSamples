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
print(stringIn)

