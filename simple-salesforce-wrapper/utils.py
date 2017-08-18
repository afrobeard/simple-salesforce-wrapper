from simple_salesforce import Salesforce
from simple_salesforce.exceptions import SalesforceAuthenticationFailed
from simple_salesforce.util import getUniqueElementValueFromXmlString


def convert_lead(session, session_id, lead_id, account_id,
                 sf_instance, lead_status='Closed Won',
                 sandbox=False, proxies=None, sf_version='38.0'):
    soap_url = 'https://{sf_instance}/services/Soap/u/{sf_version}'
    domain = 'test' if sandbox else 'login'
    soap_url = soap_url.format(domain=domain, sf_version=sf_version, sf_instance=sf_instance)
    # <?xml version="1.0" encoding="utf-8"?>
    login_soap_request_body = """
    <soapenv:Envelope
                xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                xmlns:urn="urn:partner.soap.sforce.com">
      <soapenv:Header>
         <urn:SessionHeader>
            <urn:sessionId>{session_id}</urn:sessionId>
         </urn:SessionHeader>
      </soapenv:Header>
      <soapenv:Body>
         <urn:convertLead> 
            <urn:leadConverts> <!-- Zero or more repetitions -->
               <urn:convertedStatus>{lead_status}</urn:convertedStatus>
               <urn:leadId>{lead_id}</urn:leadId>
               <urn:accountId>{account_id}</urn:accountId>
               <urn:sendNotificationEmail>true</urn:sendNotificationEmail>
               <urn:doNotCreateOpportunity>true</urn:doNotCreateOpportunity>
            </urn:leadConverts>
         </urn:convertLead>
      </soapenv:Body>
    </soapenv:Envelope>
    """.format(lead_id=lead_id, account_id=account_id, session_id=session_id, lead_status=lead_status)
    login_soap_request_headers = {
        'content-type': 'text/xml',
        'charset': 'UTF-8',
        'SOAPAction': 'convertLead'
    }
    response = session.post(
        soap_url, login_soap_request_body, headers=login_soap_request_headers,
        proxies=proxies)
    if response.status_code != 200:
        except_code = getUniqueElementValueFromXmlString(
            response.content, 'sf:exceptionCode')
        except_msg = getUniqueElementValueFromXmlString(
            response.content, 'sf:exceptionMessage')
        raise SalesforceAuthenticationFailed(except_code, except_msg)
    else:
        contact_id = getUniqueElementValueFromXmlString(response.content, 'contactId')
        success = getUniqueElementValueFromXmlString(response.content, 'success')
        status_code = getUniqueElementValueFromXmlString(response.content, 'statusCode')
        if success == 'true':
            return True, contact_id
        else:
            return False, status_code

if __name__ == "__main__":
    SALESFORCE_INSTANCE = {
        "username": 'appsfapiuser@zenbusiness.com.sandbox',
        "password": 'zenbizapi1',
        "security_token": 'pgCW9I8UrLjEKP3obv9rRKUv',
        "sandbox": True
    }
    sf = Salesforce(username=SALESFORCE_INSTANCE.get("username"),
                    password=SALESFORCE_INSTANCE.get("password"),
                    security_token=SALESFORCE_INSTANCE.get("security_token"),
                    sandbox=SALESFORCE_INSTANCE.get("sandbox"))
    resp = convert_lead(sf.session, sf.session_id, sandbox=sf.sandbox, proxies=sf.proxies,
                        sf_version=sf.sf_version, sf_instance=sf.sf_instance,
                        lead_id='00Qg000000Ac6fZEAR', account_id='001g000001jOrDfAAK')
