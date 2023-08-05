import requests
import xml.etree.ElementTree as ET

def pyTRM(date_trm=""):
    '''
    Retorna en JSON el valor de la TRM del dia actual\n
    Puede especificar una fecha\n
    pyTRM("2021-06-1") -> retorna el valor para el 1 de junio del 2021 
    '''
    url = "https://www.superfinanciera.gov.co/SuperfinancieraWebServiceTRM/TCRMServicesWebService/TCRMServicesWebService?wsdl"
    xml = f'''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
            xmlns:act="http://action.trm.services.generic.action.superfinanciera.nexura.sc.com.co/">
            <soapenv:Header/>
            <soapenv:Body>
            <act:queryTCRM>
            <tcrmQueryAssociatedDate>{date_trm}</tcrmQueryAssociatedDate>
            </act:queryTCRM>
            </soapenv:Body>
            </soapenv:Envelope>'''
    request = requests.post(url,data=xml,headers={"Content-Type": "text/xml"})
    tree = ET.fromstring(request.text)
    id = tree.find(".//return/id").text
    unit = tree.find(".//return/unit").text
    validityFrom = tree.find(".//return/validityFrom").text
    validityTo = tree.find(".//return/validityTo").text
    value = '{0:.2f}'.format(float(tree.find(".//return/value").text))
    json_data = {}
    for variable in ["id","unit","validityFrom","validityTo","value"]:
        json_data[variable] =  eval(variable)
    return json_data