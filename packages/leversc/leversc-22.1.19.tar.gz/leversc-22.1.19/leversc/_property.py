import requests
import json

# retrieves/sets viewParams, renderParams, uiParams, etc....
def setProperty(self,propertyName,propertyStruct):    
    URL = self._leversc_url("/"+propertyName)
    response = requests.post(URL,json=propertyStruct)
    
def getProperty(self,propertyName):
    URL = self._leversc_url("/"+propertyName)
    response = requests.get(URL)
    property = response.json()
    if 'list'==type(property):
        # view and render params come as 1 element list
        property = property[0]
    return property
