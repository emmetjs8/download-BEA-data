from terminalUtils import *
import textwrap
from tabulate import tabulate
import time

def printHeader(headerTitle):
    terminalWidth, terminalHeight = terminalDimensions()

    print("*" * terminalWidth)
    print("*" + f"{headerTitle}".center(terminalWidth - 2) + "*")
    print("*" * terminalWidth)

def mainMenu():
    clearTerminal()

    optionsToDisplay = {"1": "Search Available Datasets",
                        "2": "Download PCE Data",
                        "3": "Download CPI Data"}

    while True:
        printHeader("BEA API Search Application")

        # Print options
        print("Options: ")
        for key in optionsToDisplay:
            print(f"\t{key}) {optionsToDisplay[key]}")
        print()

        # Get input
        optionInput = input("Enter a number: ").strip()

        # Error handle input
        for key in optionsToDisplay:
            if optionInput == key:
                clearTerminal()
                return optionsToDisplay[key]
            else:
                pass
        
        print("Incorrect input. Enter a number associated with an option.")
        print("Try again.")
        time.sleep(3)
        clearTerminal()

# Dataset table page

def searchDataSetsMenu(dataSetObjects):
    """
    Prompts the user to choose a dataset from the list of available datasets.

    Parameters:
    -----------
    dataSetObjects : list
        A list of BeaDataSet objects, each containing a name and description.

    Returns:
    --------
    BeaDataSet
        The chosen BeaDataSet object.
    """
    # List to save all dataset options and their descriptions
    dataSets, dataSetDescriptions = ["Dataset:"], ["Description:"]

    # Get all datasets and their descriptions
    for dataSetObject in dataSetObjects:
        dataSets.append(dataSetObject.dataSetName.strip())
        dataSetDescriptions.append(dataSetObject.dataSetDescription)

    # Loop until a valid dataset is chosen
    while True:
        printHeader("Search Available Datasets")

        # Prepare the data for printing in the correct format (transposed)
        printDataSetTable(dataSets, dataSetDescriptions)
        print()

        # Prompt for user input to select a dataset
        userInput = input("Please choose a dataset: ").lower().strip()

        # Search for a matching dataset name
        for dataSetObject in dataSetObjects:
            validDataSetName = dataSetObject.dataSetName.lower().strip()

            # Check if the user's input matches any dataset name and return that dataset object
            if userInput == validDataSetName:
                clearTerminal()
                return dataSetObject

        # If no match found, display an error message and prompt the user again
        print("Invalid input. Please input a dataset name from the table.")
        print("Try again.")
        time.sleep(3)
        clearTerminal()

def formatDataSetTableLine(dataset, description, terminalWidth, datasetColumnWidth):
    # Calculate space for the middle separator
    separator = " | "
    separatorWidth = len(separator)
    
    # Allocate space for dataset and description
    descriptionWidth = terminalWidth - datasetColumnWidth - separatorWidth - 2  # Remaining space

    # Format the line
    line = (
        "*" +
        f" {dataset}".ljust(datasetColumnWidth) +  # Dataset column, left-aligned
        separator +
        f"{description}".ljust(descriptionWidth) +  # Description column, left-aligned
        "*"
    )
    
    return line

def printDataSetTable(dataSets, dataSetDescriptions):
    # Get terminal dimensions
    terminalWidth, terminalHeight = terminalDimensions()
    terminalHeight = terminalHeight - 3  # Adjust for header/footer or margins

    # Max length for dataset column
    datasetMaxLength = max(len(ds) for ds in dataSets)

    # Adjust column sizes to fit the terminal
    maxColumnWidth = (terminalWidth - 4) // 2  # Give some space for separators
    datasetColumnWidth = min(datasetMaxLength, maxColumnWidth) + 4

    # Print each dataset and description row
    for i in range(len(dataSets)):
        print(formatDataSetTableLine(dataSets[i], dataSetDescriptions[i], terminalWidth, datasetColumnWidth))
    print("*" * terminalWidth)

# Function to call

def display(dataSetObjects):
    mainMenuChoice = mainMenu()

    if mainMenuChoice == "Search Available Datasets":
        dataSetObject = searchDataSetsMenu(dataSetObjects)
    
