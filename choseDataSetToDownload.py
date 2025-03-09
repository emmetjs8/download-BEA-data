import os
import time
from tabulate import tabulate
import textwrap
from terminalUtils import clearTerminal

def chooseDataSet(dataSetObjects):
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
    dataSets, dataSetDescriptions = [], []

    # Get all datasets and their descriptions
    for dataSetObject in dataSetObjects:
        dataSets.append(dataSetObject.dataSetName)
        dataSetDescriptions.append(dataSetObject.dataSetDescription)

    # Loop until a valid dataset is chosen
    while True:
        # Prepare the data for printing in the correct format (transposed)
        printTable(list(zip(dataSets, dataSetDescriptions)), ["Dataset", "Description"])

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

def chooseDataSetParameters(dataSetObject):
    """
    Need to:
        Get parameter
            Check if patameter is required
        Get parameter description
        Get Default parameter
            Display option to input default
        Get All Values input
            Display option to input all values
        Check is multiple values accepted
            Display option to input multiple values
        Get Valid Inputs
            Option to search all valid inputs if large enough
        Get Valid Inputs description
    """
    # Lists for display
    parameters = dataSetObject.parameters
    parameterDescriptions = dataSetObject.parametersDescriptions
    parametersRequired = dataSetObject.parametersRequiredInRequest
    parameterDefaultValues = dataSetObject.parametersDefaultValues
    multipleInputsValid = dataSetObject.parametersMultipleValsAcceptedInRequest
    allValuesInputValid = dataSetObject.parametersAllValueRequest
    validInputs = dataSetObject.parameterInputs
    validInputsDescriptions = dataSetObject.parameterInputsDescriptions

    numParams = len(parameters)

    for i in range(numParams):
        param = parameters[i]
        paramDescription = parameterDescriptions[i]
        paramRequired = parametersRequired[i]
        multInputsValid = multipleInputsValid[i]
        allValueInputValid = allValuesInputValid[i]
        inputs = validInputs[i]
        inputsDescription = validInputsDescriptions[i]
        
        printParam(dataSetObject.dataSetName, param, paramDescription,
                            multInputsValid, allValueInputValid, inputs, inputsDescription)

        print("-"*100)
        print(f"Parameter: {parameters[i]}")
        print(f"\tDescription: {parameterDescriptions[i]}")
        print(f"\tRequired: {parametersRequired[i]}")
        print(f"\tDefualt Value: {parameterDefaultValues[i]}")
        print(f"\tMultiple Inputs: {multipleInputsValid[i]}")
        print(f"\tAll Value Input: {allValuesInputValid[i]}")
        print(f"\tNumber of valid inputs: {len(validInputs[i])}")
    print("-"*100)

def printParam(dataset, parameter, description, multInputs, allValueInput, validInputs, validInputsDescriptions):
    clearTerminal()
    # Get terminal size
    terminalWidth = os.get_terminal_size().columns

    # Print the header
    print("*"*terminalWidth)
    print(f"{dataset} Dataset Parameter Input".center(terminalWidth))
    print("*"*terminalWidth)

    # Print the main body
    print(f"\tParameter: {parameter}")
    print(f"\t\t-{description}".ljust(terminalWidth - 2))

    time.sleep(5)
    

def printTable(data, headers):
    """
    Prints a table to the terminal with headers and data, adjusting to fit the terminal screen size.

    Parameters:
    -----------
    data : list[list]
        A list of lists where each inner list represents a row in the table.
    headers : list[str]
        A list of strings to be used as headers for the columns.

    Returns:
    --------
    None

    Notes:
    ------
    The table is adjusted to fit within the width of the terminal screen.
    """
    # Get terminal size
    terminalWidth = os.get_terminal_size().columns

    # Wrap text for each cell to fit within the terminal width
    def wrap_cell(content, width):
        return "\n".join(textwrap.wrap(str(content), width)) if width > 0 else content

    # Calculate maximum column width
    num_columns = len(headers)
    max_column_width = max(10, (terminalWidth - (num_columns + 1) * 3) // num_columns)

    # Wrap headers and data
    wrapped_headers = [wrap_cell(header, max_column_width) for header in headers]
    wrapped_data = [[wrap_cell(cell, max_column_width) for cell in row] for row in data]

    # Format the table using tabulate
    table = tabulate(wrapped_data, headers=wrapped_headers, tablefmt="grid", stralign="left", numalign="center")

    # Print the table
    print(table)
