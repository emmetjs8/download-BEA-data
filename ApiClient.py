import time
import requests

# ===========================================================================
# BeaApiClient Class
# ===========================================================================
# This class encapsulates the logic for interacting with the BEA API, ensuring
# that requests adhere to the specified rate limits and data size constraints.
# The client enforces the following limits:
# 1. A maximum number of 100 requests per minute.
# 2. A maximum data volume of 100 MB per minute.
# 3. A maximum number of 30 errors per minute.
#
# Methods:
# - __init__: Initializes the BeaApiClient instance with API key and rate limits.
# - resetCounters: Resets the counters for requests, data, and errors every minute.
# - checkLimits: Checks if the request exceeds the limits and waits if necessary.
# - sendRequest: Sends the request after checking limits.

class BeaApiClient:
    """
    A client to interact with the BEA API, enforcing rate and data volume limits.

    Attributes:
        apiKey (str): The API key for authentication.
        requestLimit (int): The maximum number of requests allowed per minute.
        dataLimit (int): The maximum amount of data (in bytes) that can be fetched per minute.
        errorLimit (int): The maximum number of errors allowed per minute.
        requestsMade (int): The count of requests made in the current minute.
        dataReceived (int): The total amount of data received in the current minute (in bytes).
        errorsMade (int): The count of errors occurred in the current minute.
        lastReset (float): The timestamp of the last reset of counters.

    Methods:
        resetCounters: Resets the counters (requests, data, errors) every minute.
        checkLimits: Checks if the current request exceeds the limits and waits if necessary.
        sendRequest: Sends the request after checking the limits.

    """
    
    def __init__(self, apiKey, requestLimit=100, dataLimitMb=100, errorLimit=30):
        """
        Initializes the BeaApiClient with API key and rate limits.

        :param apiKey: The API key for authentication.
        :param requestLimit: The maximum number of requests allowed per minute (default 100).
        :param dataLimitMb: The maximum data volume allowed per minute in MB (default 100 MB).
        :param errorLimit: The maximum number of errors allowed per minute (default 30).
        """
        self.apiKey = apiKey
        self.requestLimit = requestLimit  # Max requests per minute
        self.dataLimit = dataLimitMb * 1024 * 1024  # Convert MB to bytes
        self.errorLimit = errorLimit  # Max errors per minute
        self.requestsMade = 0
        self.dataReceived = 0
        self.errorsMade = 0
        self.lastReset = time.time()

    def resetCounters(self):
        """
        Resets the counters for requests, data, and errors if a minute has passed.

        This method checks if a minute has passed since the last reset. If so,
        it resets the counters to start a new period.
        """
        currentTime = time.time()
        if currentTime - self.lastReset > 60:  # If a minute has passed
            self.requestsMade = 0
            self.dataReceived = 0
            self.errorsMade = 0
            self.lastReset = currentTime

    def checkLimits(self, url):
        """
        Checks if the current request exceeds the defined rate limits.

        This method checks if the request limits (requests per minute, data volume
        per minute, and errors per minute) are exceeded. If any limit is exceeded,
        it waits until the next period and then makes the request.

        :param url: The URL to send the request to.
        :return: The response data in JSON format.
        :raises Exception: If the request fails or if an error occurs during the request.
        """
        self.resetCounters()  # Reset counters if a new minute has passed

        # Check if limits are exceeded and wait if necessary
        while self.requestsMade >= self.requestLimit or self.dataReceived >= self.dataLimit or self.errorsMade >= self.errorLimit:
            # Calculate how long to wait until the next period (one minute)
            timeToWait = 60 - (time.time() - self.lastReset)
            if timeToWait > 0:
                print(f"Limit exceeded. Waiting for {timeToWait:.2f} seconds.")
                time.sleep(timeToWait)  # Wait until the next period

            # After waiting, reset counters and check limits again
            self.resetCounters()

        # Send the request
        response = requests.get(url, stream=True)  # Use stream to avoid loading the entire response into memory

        # Calculate the size of the response in bytes
        dataSize = len(response.content)

        # Track the number of requests and data received
        self.requestsMade += 1
        self.dataReceived += dataSize

        if response.status_code != 200:
            self.errorsMade += 1
            raise Exception(f"Error during request: {response.status_code}")

        return response.json()

    def sendRequest(self, url):
        """
        Sends the request after checking the limits.

        This method first checks if the limits are exceeded before sending the request
        to ensure that the rate limits are respected.

        :param url: The URL to send the request to.
        :return: The response data in JSON format.
        """
        return self.checkLimits(url)