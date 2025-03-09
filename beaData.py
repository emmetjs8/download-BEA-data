import shutil
import textwrap
from tabulate import tabulate

class BeaDataSet:
    def __init__(self, dataSetName, dataSetDescription):
        self.dataSetName = dataSetName
        self.dataSetDescription = dataSetDescription

        self.parameters = []
        self.parametersDescriptions = []
        self.parametersRequiredInRequest = []
        self.parametersDefaultValues = []
        self.parametersMultipleValsAcceptedInRequest = []
        self.parametersAllValueRequest = []

        self.parameterInputs = []
        self.parameterInputsDescriptions = []

        self.urlParamInputs = {}

    def updateParametersLists(self):
        """
        Updates parameters lists by:
        - Converting '0'/'1' strings to False/True booleans in `parametersRequiredInRequest` 
          and `parametersMultipleValsAcceptedInRequest`.
        - Replacing empty strings ('') with 'N/a' in `parametersDefaultValues` 
          and `parametersAllValueRequest`.
        """
        # Update boolean values for required parameters and multiple values accepted
        for i in range(len(self.parametersRequiredInRequest)):
            self.parametersRequiredInRequest[i] = self.parametersRequiredInRequest[i] == '1'
            self.parametersMultipleValsAcceptedInRequest[i] = self.parametersMultipleValsAcceptedInRequest[i] == '1'

        # Replace empty strings with 'N/a' in default values and "AllValue" requests
        for i in range(len(self.parametersAllValueRequest)):
            if self.parametersAllValueRequest[i] == '':
                self.parametersAllValueRequest[i] = 'N/a'
            if self.parametersDefaultValues[i] == '':
                self.parametersDefaultValues[i] = 'N/a'
    
    def displayParameterInputs(self, parameter):
        """
        Displays valid inputs and descriptions for a given parameter using tabulate.

        :param parameter: The name of the parameter to display valid inputs for.
        """
        try:
            # Find the index of the parameter
            index = self.parameters.index(parameter)

            # Check if the parameter is "Year" (and handle separately if necessary)
            if parameter == "Year":
                # If "Year", you may handle it differently, for now, just pass
                print("Displaying Year-related inputs is not implemented yet.")
                pass
            else:
                # Fetch valid inputs and descriptions for the parameter
                validInputs = self.parameterInputs[index]
                validDescriptions = self.parameterInputsDescriptions[index]

                # Prepare the data for tabulation
                table_data = []
                for i in range(len(validInputs)):
                    table_data.append([validInputs[i], validDescriptions[i]])

                # Table headers
                headers = ["Valid Input", "Description"]

                # Print the table using tabulate
                print(f"\nValid Inputs and Descriptions for '{parameter}' parameter:")
                print(tabulate(table_data, headers=headers, tablefmt="grid"))

        except ValueError:
            print(f"Parameter '{parameter}' not found in the dataset.")

    def printDatasetDetails(self):
        """
        Prints the details for each parameter in the dataset in a tabular format using tabulate.
        Long descriptions are wrapped to fit within the table, and the table is adjusted to the terminal width.
        """
        # Get terminal width
        terminal_width = shutil.get_terminal_size().columns

        # Define column proportions
        col_proportions = [0.2, 0.4, 0.1, 0.1, 0.1, 0.1]  # proportion of terminal width for each column

        # Calculate the maximum width for each column based on proportions
        column_widths = [int(terminal_width * prop) for prop in col_proportions]
        
        # Wrap long descriptions based on column width
        table_data = []
        for i in range(len(self.parameters)):
            # Wrap the description to fit in the calculated column width
            wrapped_description = textwrap.fill(self.parametersDescriptions[i], width=column_widths[1] - 2)  # Leave space for padding
            table_data.append([
                self.parameters[i],
                wrapped_description,
                "Yes" if self.parametersRequiredInRequest[i] else "No",
                self.parametersDefaultValues[i],
                "Yes" if self.parametersMultipleValsAcceptedInRequest[i] else "No",
                self.parametersAllValueRequest[i]
            ])
        
        # Prepare headers for the table
        headers = [
            "Parameter", 
            "Description", 
            "Required", 
            "Default Value", 
            "Multiple Accepted", 
            "All Value Request"
        ]
        
        # Print the details using tabulate
        print("-" * terminal_width)
        print(f"Details for Dataset: {self.dataSetName}")
        print(f"Dataset description: {self.dataSetDescription}")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print("-" * terminal_width)

    def printValidInputDetails(self):
        """
        Prints the valid input values and descriptions for each parameter in the dataset in a tabular format using tabulate.
        Adjusts the table to fit within the terminal width and ensures readability for nested lists of valid inputs.
        """
        terminal_width = shutil.get_terminal_size().columns
        col_proportions = [0.2, 0.4, 0.4]  # Proportions for columns
        column_widths = [int(terminal_width * prop) for prop in col_proportions]

        # Check if valid inputs exist
        if not self.parameterInputs or not self.parameterInputsDescriptions:
            print("No valid input data available for this dataset.")
            return

        # Prepare data for the table
        table_data = []
        for param_idx, param in enumerate(self.parameters):
            # Get the corresponding valid inputs and descriptions for this parameter
            inputs = self.parameterInputs[param_idx]
            descriptions = self.parameterInputsDescriptions[param_idx]

            # Ensure inputs and descriptions align
            for input_value, description in zip(inputs, descriptions):
                # Wrap the description for readability
                wrapped_description = textwrap.fill(description, width=column_widths[2] - 2)
                table_data.append([param, input_value, wrapped_description])

        # Table headers
        headers = ["Parameter", "Valid Input", "Description"]

        # Print the table
        print("-" * terminal_width)
        print(f"Valid Inputs for Dataset: {self.dataSetName}")
        print(f"Dataset description: {self.dataSetDescription}")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print("-" * terminal_width)
