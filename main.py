from ApiClient import BeaApiClient
from downloadBeaDatasets import readBeaDataSets
from terminalUtils import clearTerminal
from choseDataSetToDownload import *
from display import display
import json

# Initialize an ApiClient object to request BEA API without breaking request limits
APIKEY = 'A14D963C-D1A6-4F42-9AED-EC5F23EFD352'
client = BeaApiClient(apiKey=APIKEY)

beaDataSets = readBeaDataSets(client)



"""
dataset = 'NIUnderlyingDetail'
Frequency = 'AQM'
TableId = 'U20405'
TableName = TableId
Year = 'X'
urlYear = f'https://apps.bea.gov/api/data?&UserID={APIKEY}&method=GetData&datasetname={dataset}&Frequency=A&TableID={TableId}&TableName={TableName}&Year={Year}&ResultFormat=JSON'
urlQuarter = f'https://apps.bea.gov/api/data?&UserID={APIKEY}&method=GetData&datasetname={dataset}&Frequency=Q&TableID={TableId}&TableName={TableName}&Year={Year}&ResultFormat=JSON'
urlMonth = f'https://apps.bea.gov/api/data?&UserID={APIKEY}&method=GetData&datasetname={dataset}&Frequency=M&TableID={TableId}&TableName={TableName}&Year={Year}&ResultFormat=JSON'

#dataSetObjects = readBeaDataSets(client, "beaDataSets.txt")

#display(dataSetObjects)

responseYearly = client.sendRequest(urlYear)
responseQuarterly = client.sendRequest(urlQuarter)
responseMonthly = client.sendRequest(urlMonth)

writeJsonToFile(responseYearly, "PCE_Yearly.json")
writeJsonToFile(responseQuarterly, "PCE_Quarterly.json")
writeJsonToFile(responseMonthly, "PCE_Monthly.json")
"""