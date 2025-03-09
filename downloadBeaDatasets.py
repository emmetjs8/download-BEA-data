# ==========================================================
# File: downloadBeaDatasets.py
# Purpose: This file contains functions for interacting with
#          the Bureau of Economic Analysis (BEA) API, processing
#          dataset and parameter information, and handling file
#          I/O operations.
# ==========================================================
#
# Functions:
# 1. writeDataSetsToFile - Writes a list of BeaDataSet objects to a file, including metadata and dataset details.
# 2. readBeaDataSets - Reads datasets from a file and returns a list of BeaDataSet objects.
# 3. downloadBeaDatasets - Downloads the BEA datasets, processes them, and returns a list of BeaDataSet objects.
# 4. ensureResponseIsList - Ensures the response value is returned as a list, converting it if necessary.
# 5. extractParamInfo - Extracts parameter attributes from a list of parameters returned by the BEA API.
# 6. extractDataSets - Extracts dataset names and descriptions from a BEA API response.
# 7. extractValidInputs - Extracts valid input values and descriptions for a parameter in a dataset.
# 8. getFiscalQuarter - Determines the fiscal quarter of a given date.
#
# Notes:
# - This file assumes that the 'client' object has a method 'sendRequest' to interact with the BEA API.
# - The BEA datasets contain information such as parameters, descriptions, and valid input values.
# - Data is saved and read in a specific text file format for later use.

from beaData import *
from terminalUtils import clearTerminal
from datetime import datetime
import time
import math

#####################################################################
#####################################################################
# File reading and writing functions
#####################################################################
#####################################################################

def readBeaDataSets(client, filename="beaDataSets.txt"):
    """
    Reads BEA datasets from a file and returns a list of BeaDataSet objects. If the data in the file 
    is outdated (from a previous fiscal quarter), it downloads the latest datasets, writes them to the file, 
    and returns the updated list.

    Parameters:
    -----------
    client : object
        The client object used for downloading datasets from the BEA API.
    filename : str, optional
        The name of the file containing the BEA datasets (default is "beaDataSets.txt").

    Returns:
    --------
    list[BeaDataSet] or None
        A list of BeaDataSet objects if successful, or None if an error occurs.

    Notes:
    ------
    - The file format is expected to be as follows for each dataset:
        Line 1: Dataset Name (string)
        Line 2: Dataset Description (string)
        Line 3: Parameters (list in string format)
        Line 4: Parameter Descriptions (list in string format)
        Line 5: Parameters Required In Request (list in string format)
        Line 6: Parameter Default Values (list in string format)
        Line 7: Parameters Multiple Values Accepted In Request (list in string format)
        Line 8: Parameter All Values List (list in string format)
        Line 9: Parameter Inputs (list in string format)
        Line 10: Parameter Inputs Descriptions (list in string format)
        Line 11: Null character delimiter ("\0")
    """

    def parseList(line):
        """Helper to parse lists stored as strings in the file."""
        return eval(line.strip()) if line.strip() else []

    dataSetObjects = []

    try:
        with open(filename, 'r') as file:
            # Read the first line: the file's date
            dateLine = file.readline().strip()
            fileDate = datetime.strptime(dateLine, "%Y-%m-%d")
            
            # Determine fiscal quarters
            fileQuarter = getFiscalQuarter(fileDate)
            currentDate = datetime.now()
            currentQuarter = getFiscalQuarter(currentDate)

            # If the file's data is outdated, redownload the datasets
            if currentDate.year > fileDate.year or currentQuarter != fileQuarter:
                print("Data is outdated. Downloading new datasets.")
                dataSetObjects = downloadBeaDatasets(client)
                writeDataSetsToFile(dataSetObjects, filename)
                time.sleep(2)
                clearTerminal()
                return dataSetObjects
            
            # Read datasets from the file
            while True:
                dataSetName = file.readline().strip()
                if not dataSetName:  # End of file
                    break

                # Parse the dataset attributes
                dataSetDescription = file.readline().strip()
                parameters = parseList(file.readline())
                parametersDescriptions = parseList(file.readline())
                parametersRequiredInRequest = parseList(file.readline())
                parametersDefaultValues = parseList(file.readline())
                parametersMultipleValsAcceptedInRequest = parseList(file.readline())
                parametersAllValueRequest = parseList(file.readline())
                parameterInputs = parseList(file.readline())
                parameterInputsDescriptions = parseList(file.readline())

                # Skip the null character delimiter
                file.readline()

                # Create and populate a BeaDataSet object
                dataSetObject = BeaDataSet(dataSetName, dataSetDescription)
                dataSetObject.parameters = parameters
                dataSetObject.parametersDescriptions = parametersDescriptions
                dataSetObject.parametersRequiredInRequest = parametersRequiredInRequest
                dataSetObject.parametersDefaultValues = parametersDefaultValues
                dataSetObject.parametersMultipleValsAcceptedInRequest = parametersMultipleValsAcceptedInRequest
                dataSetObject.parametersAllValueRequest = parametersAllValueRequest
                dataSetObject.parameterInputs = parameterInputs
                dataSetObject.parameterInputsDescriptions = parameterInputsDescriptions

                # Add the dataset to the list
                dataSetObjects.append(dataSetObject)

            print("Data successfully loaded from file.")
            time.sleep(2)
            clearTerminal()
            return dataSetObjects

    except FileNotFoundError:
        # If the file is missing, download and save new datasets
        print(f"File '{filename}' not found. Downloading datasets.")
        dataSetObjects = downloadBeaDatasets(client)
        writeDataSetsToFile(dataSetObjects, filename)
        time.sleep(2)
        clearTerminal()
        return dataSetObjects
    except Exception as e:
        # Handle unexpected errors
        print(f"An error occurred: {e}")
        time.sleep(2)
        clearTerminal()
        return None

def getFiscalQuarter(date):
    """
    Determines the fiscal quarter of the given date.

    Parameters:
    -----------
    date : datetime
        The date for which the fiscal quarter needs to be determined.

    Returns:
    --------
    int
        The fiscal quarter (1, 2, 3, or 4) based on the month of the provided date.

    Notes:
    ------
    - The fiscal year is divided into four quarters:
        - Q1: January, February, March
        - Q2: April, May, June
        - Q3: July, August, September
        - Q4: October, November, December
    - This function assumes the fiscal year follows the standard calendar year (January to December).
    """
    # Calculate the fiscal quarter by dividing the month by 3 and rounding up
    return math.ceil(date.month / 3)

def writeDataSetsToFile(dataSetObjects, filename):
    """
    Writes the given list of BeaDataSet objects to a file, including metadata and dataset details.

    Parameters:
    -----------
    dataSetObjects : list[BeaDataSet]
        A list of BeaDataSet objects to be written to the file.
    filename : str
        The name of the file where the datasets will be written.

    Returns:
    --------
    None

    Notes:
    ------
    - The file will begin with the current date.
    - For each dataset object, the following attributes are written:
        - Name
        - Description
        - Lists of parameters and their descriptions
        - Other associated attributes
    - Each dataset is separated by a null character ("\0") to allow easy parsing later.
    """
    # Get the current date and format it as a string
    currentDate = datetime.now()
    dateString = currentDate.strftime("%Y-%m-%d") + "\n"

    # Open the file for writing
    with open(filename, 'w') as file:
        # Write the date at the top of the file
        file.write(dateString)

        # Loop through each dataset and write its attributes to the file
        for dataSetObject in dataSetObjects:
            file.write(dataSetObject.dataSetName + "\n")
            file.write(dataSetObject.dataSetDescription + "\n")
            file.write(str(dataSetObject.parameters) + "\n")
            file.write(str(dataSetObject.parametersDescriptions) + "\n")
            file.write(str(dataSetObject.parametersRequiredInRequest) + "\n")
            file.write(str(dataSetObject.parametersDefaultValues) + "\n")
            file.write(str(dataSetObject.parametersMultipleValsAcceptedInRequest) + "\n")
            file.write(str(dataSetObject.parametersAllValueRequest) + "\n")
            file.write(str(dataSetObject.parameterInputs) + "\n")
            file.write(str(dataSetObject.parameterInputsDescriptions) + "\n")
            
            # Use a null character to delimit datasets
            file.write("\0\n")

    print(f"Data successfully written to {filename}")

#####################################################################
#####################################################################
# Downloading and parsing BEA dataset functions
#####################################################################
#####################################################################

def downloadBeaDatasets(client):
    """
    Downloads the BEA datasets using the provided client object and returns a list of BeaDataSet objects.
    Each dataset contains details such as name, description, parameters, and valid inputs (See beaData.py for object description).

    Parameters:
    -----------
    client : object
        The client object used for sending requests to the BEA API.

    Returns:
    --------
    list[BeaDataSet]
        A list of BeaDataSet objects containing information about each dataset.

    Notes:
    ------
    - The function sends multiple API requests to fetch dataset names, descriptions, parameters, and valid input values.
    - The parameters for each dataset are processed and updated, and valid input values are extracted for each parameter.
    - The function also handles specific cases for certain datasets like "NIPA", "NIUnderlyingDetail", and "FixedAssets".
    """

    # URL to fetch all available datasets from the BEA API
    allDatasetsUrl = f'http://apps.bea.gov/api/data?&UserID={client.apiKey}&method=GETDATASETLIST&ResultFormat=JSON'

    # Fetch the response from the BEA API for all datasets
    beaDataSetsResponse = client.sendRequest(allDatasetsUrl)
    datasets = beaDataSetsResponse['BEAAPI']['Results']['Dataset']

    # Extract dataset names and descriptions using a helper function
    datasetsList, dataSetDescriptionList = extractDataSets(datasets)

    # List to hold the BeaDataSet objects that will be created
    dataSetObjects = []

    # Loop through each dataset, creating a BeaDataSet object for each
    for name, description in zip(datasetsList, dataSetDescriptionList):
        # Initialize a BeaDataSet object for each dataset
        dataSetObject = BeaDataSet(name, description)

        # Fetch and process the parameters for the dataset
        parameterListUrl = f'https://apps.bea.gov/api/data?&UserID={client.apiKey}&method=getparameterlist&datasetname={dataSetObject.dataSetName}&ResultFormat=JSON'
        beaParametersResponse = client.sendRequest(parameterListUrl)
        parameters = beaParametersResponse['BEAAPI']['Results']['Parameter']

        # Extract the parameters' details (descriptions, required flags, default values, etc.)
        dataSetObject.parameters, dataSetObject.parametersDescriptions, dataSetObject.parametersRequiredInRequest, \
            dataSetObject.parametersDefaultValues, dataSetObject.parametersMultipleValsAcceptedInRequest, \
                dataSetObject.parametersAllValueRequest = extractParamInfo(parameters)

        # Update the dataset's parameters list with the extracted details
        dataSetObject.updateParametersLists()

        # Fetch valid input values for each parameter in the dataset
        for paramName in dataSetObject.parameters:
            paramInputValuesUrl = f'https://apps.bea.gov/api/data?&UserID={client.apiKey}&method=GetParameterValues&datasetname={dataSetObject.dataSetName}&ParameterName={paramName}&ResultFormat=JSON'
            beaParametersInputsResponse = client.sendRequest(paramInputValuesUrl)
            inputs = beaParametersInputsResponse['BEAAPI']['Results']['ParamValue']

            # Handle specific cases for certain datasets like "NIPA", "NIUnderlyingDetail", and "FixedAssets"
            if name in ["NIPA", "NIUnderlyingDetail", "FixedAssets"] and paramName == 'Year':
                # Extract valid inputs specifically for the 'Year' parameter
                validInputs, inputDescriptions = extractValidInputs(inputs, dataSetObject.dataSetName, paramName)
                dataSetObject.parameterInputs.append(validInputs)
                dataSetObject.parameterInputsDescriptions.append(inputDescriptions)
            else:
                # Extract valid inputs and descriptions for other parameters
                validInputs, inputDescriptions = extractValidInputs(inputs, dataSetObject.dataSetName, paramName)
                dataSetObject.parameterInputs.append(validInputs)
                dataSetObject.parameterInputsDescriptions.append(inputDescriptions)
        
        # Add the populated dataset object to the datasets list
        dataSetObjects.append(dataSetObject)

    # Return the list of populated BeaDataSet objects
    return dataSetObjects

def ensureResponseIsList(value):
    """
    Ensures that the value is returned as a list.
    If the value is a dictionary, it wraps it in a list.
    If it's already a list, it returns it unchanged.
    """
    if isinstance(value, dict):
        return [value]  # Wrap the dictionary in a list
    elif isinstance(value, list):
        return value  # Return the list as it is
    return []  # Default case: return an empty list

def extractParamInfo(parameters):
    """
    Extract parameter attributes from a list of parameters.

    :param parameters: A list of parameter dictionaries.
    :return: Six lists:
        - paramNames: List of parameter names.
        - paramDescriptions: List of parameter descriptions.
        - paramRequiredInRequest: List indicating if the parameter is required.
        - paramDefaultVals: List of default values for the parameters.
        - paramMultipleValsAcceptedInRequest: List indicating if multiple values are accepted.
        - paramAllValueRequest: List indicating if the parameter accepts a command for downloading All data.
    """
    paramNames = []
    paramDescriptions = []
    paramRequiredInRequest = []
    paramDefaultVals = []
    paramMultipleValsAcceptedInRequest = []
    paramAllValueRequest = []

    for param in ensureResponseIsList(parameters):
        paramNames.append(param.get('ParameterName', 'N/A'))
        paramDescriptions.append(param.get('ParameterDescription', 'N/A'))
        paramRequiredInRequest.append(param.get('ParameterIsRequiredFlag', 'N/A'))
        paramDefaultVals.append(param.get('ParameterDefaultValue', 'N/a'))
        paramMultipleValsAcceptedInRequest.append(param.get('MultipleAcceptedFlag', 'N/a'))
        paramAllValueRequest.append(param.get('AllValue', 'N/a'))

    return (
        paramNames,
        paramDescriptions,
        paramRequiredInRequest,
        paramDefaultVals,
        paramMultipleValsAcceptedInRequest,
        paramAllValueRequest
    )

def extractDataSets(dataSets):
    """
    Extract dataset names and descriptions from a BEA API response.

    :param dataSets: A list of dataset dictionaries.
    :return: Two lists - one with dataset names and another with their descriptions.
    """
    dataSetList = []
    dataSetDescriptionList = []
    for dataSet in dataSets:
        dataSetList.append(dataSet.get('DatasetName', 'N/A'))
        dataSetDescriptionList.append(dataSet.get('DatasetDescription', 'N/A'))
    return dataSetList, dataSetDescriptionList

def extractValidInputs(inputs, dataSetName, paramName):
    """
    Extracts valid input values and their descriptions for a given parameter in a dataset.

    Handles special cases for the "Year" parameter in specific datasets ("NIPA", "NIUnderlyingDetail", "FixedAssets").
    All other parameters or datasets will go through the general input extraction process.

    Args:
        inputs (list of dict): A list of dictionaries containing valid input values and descriptions for the specified parameter.
        datasetName (str): The name of the dataset for which the parameter belongs.
        paramName (str): The name of the parameter being processed.

    Returns:
        tuple: A tuple containing lists of valid inputs and their descriptions for most datasets.
               For the "Year" parameter in specific datasets, it returns multiple year-related lists.
    """
    inputs = ensureResponseIsList(inputs)
    
    # For datasets "NIPA", "NIUnderlyingDetail", and "FixedAssets" and if the parameter is "Year"
    if dataSetName in ["NIPA", "NIUnderlyingDetail", "FixedAssets"] and paramName == "Year":
        validInputs, inputDescriptions = [], []
        inputsKeys = list(inputs[0].keys())

        # Extract valid year-related inputs
        for i in range(len(inputs)):
            tableName = inputs[i][inputsKeys[0]]
            annualYearRange = f"{inputs[i][inputsKeys[1]]}-{inputs[i][inputsKeys[2]]}"
            quarterlyYearRange = f"{inputs[i][inputsKeys[3]]}-{inputs[i][inputsKeys[4]]}"
            monthlyYearRange = f"{inputs[i][inputsKeys[5]]}-{inputs[i][inputsKeys[6]]}"
            validInputs.append({"TableName": tableName, "Annual year Range": annualYearRange,
                                "Quarterly Year Range": quarterlyYearRange, "Monthly Year Range": monthlyYearRange})
            inputDescriptions.append(f"Year ranges for annual, quarterly, and monthly data from table: {tableName}")

        return validInputs, inputDescriptions

    else:
        # Default branch for all other parameters or datasets
        validInputs, inputDescriptions = [], []
        inputsKeys = list(inputs[0].keys())

        # Extract valid input values and their descriptions
        for i in range(len(inputs)):
            validInputs.append(inputs[i][inputsKeys[0]])
            inputDescriptions.append(inputs[i][inputsKeys[1]])

        return validInputs, inputDescriptions