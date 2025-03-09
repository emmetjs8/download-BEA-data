import os
import platform

def clearTerminal():
    """
    Clears the terminal screen based on the operating system.

    This function detects the operating system and uses the appropriate command 
    to clear the terminal screen.

    Supported operating systems:
    - Windows: uses 'cls'
    - macOS/Linux: uses 'clear'
    """
    system = platform.system().lower()
    if system == 'windows':
        os.system('cls')  # Windows command to clear the screen
    else:
        os.system('clear')  # macOS/Linux command to clear the screen

def terminalDimensions():
    terminalWidth = os.get_terminal_size().columns
    terminalHeight = os.get_terminal_size().lines
    return terminalWidth, terminalHeight
