# Import necessary libraries
import os
import sys
import platform
import subprocess
import pathlib
import difflib
from IPython.display import display
from Modules import InputMod

# Get the operating system type
os_type = platform.system()

# Define a dictionary to handle file opening based on the operating system
Known_OS_systems = {
'Windows': lambda path: os.startfile(path),
'Linux': lambda path: subprocess.run(['xdg-open', path]),
'Darwin': lambda path: subprocess.run(['open', path])
}

# Function to find a file in a given directory
def find_file(filename, directory = pathlib.Path.cwd()):
  for file in directory.rglob(filename):
    return file
  return None

# Initialize variables
user_input = None; close_match = None; break_flag = 'main menu';exit_flag = 'exit'

# Main loop
while (user_input != exit_flag):
  valid_inputs = 'view','create','modify'
  message = f'{'Welcome to the Directory creator' if not user_input else ''} \nDo you wish to {list(valid_inputs)} directory?' 
  message += f'\nType {list(valid_inputs)} or "{exit_flag}" to cancel:\nEnter input: '

  # Get user input
  user_input = InputMod.inputHandler(valid_inputs,message)

  # If user wants to view a directory
  if user_input == valid_inputs[0]:
    if os_type in Known_OS_systems:
      valid_inputs_02 = 'search'
      message_2 = f'\nPlease provide directory of file path you wish to view or Type "{valid_inputs_02}" ' 
      message_2 += f'to look for directory of file\nEnter input: '
      user_input_02 = InputMod.inputFunc(message_2)
      close_match = difflib.get_close_matches(user_input_02, valid_inputs_02, n=1)
      
      # If user input is not valid
      if close_match and user_input_02 not in valid_inputs_02: 
        message_3 = f'\nInvalid input,Type {valid_inputs_02} or {exit_flag}: '
        user_input_02 = InputMod.inputHandler(valid_inputs_02, message_3)

      # If user wants to search for a file
      if user_input_02 in valid_inputs_02:

        message_04 = f'\nType _File Name_ and _Directory_ to begin search, or type _File Name_ and "current" to search Current Directory\n'
        message_04 += f'Or type _File Name_ and "all" to search all directories\n'
        message_04 += '*Note that searching all Directories will start from the root directory (/),'.upper()
        message_04 += 'so it will search your entire PC."\n"Be aware that this can take a long time if you have a lot of files.*'.upper()
        display(message_04)
        user_input_03 = InputMod.inputFunc(f'\nEnter filename: ')
        valid_inputs_03 = 'current','all'
        message_04 = f'\nEnter directory name or "current" to get current directories \nor "all" to search all directories: '
        user_input_04 = InputMod.inputHandler(valid_inputs_03, message_04)
        
        # Determine the directory to search in
        if user_input_04 == 'current': directory = pathlib.Path.cwd()
        elif user_input_04 == 'all': directory = pathlib.Path('/').resolve()
        else: directory = pathlib.Path(user_input_04).resolve()
        
        # Try to find the file
        try:
          file = find_file(user_input_03, directory)
        except FileNotFoundError as e:print(f'File not found, {e}')
       
      # If user input is a directory path
      if user_input_02 != exit_flag and user_input_02 not in valid_inputs_02: 
        try:
          Known_OS_systems[os_type](user_input_02) 
          print('Directory opened succesfuly!')
        except FileNotFoundError as e:
          print(f'\nFile not found, {e}')