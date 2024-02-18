import os
import sys
import platform
import subprocess
import pathlib
import difflib
import numpy as np
from IPython.display import display

os_type = platform.system()
Known_OS_systems = {
'Windows': lambda path: os.startfile(path),
'Linux': lambda path: subprocess.run(['xdg-open', path]),
'Darwin': lambda path: subprocess.run(['open', path])
}

def ConcatInputs(valid_inputs, break_flag, exit_flag): 
  valid_inputs = [str(input).lower() for input in valid_inputs]
  valid_inputs.extend([break_flag, exit_flag])  
  valid_inputs = np.array(valid_inputs)
  return valid_inputs

def inputFunc(input_message):
  user_input = input(input_message).lower()
  return user_input

def error_prompt(valid_inputs, user_input, **kwargs):

  attempts = kwargs.get('attempts', 5)
  attemptsMessage_at = kwargs.get('attemptsMessage_at', 3)
  break_flag = kwargs.get('break_flag', 'main menu')
  exit_flag = kwargs.get('exit_flag', 'exit')

  while True:
    close_match = difflib.get_close_matches(user_input, valid_inputs, n=1)
    if close_match: 
      error_message = f'\nInvalid input, did you intend to type {close_match[0]}?, Type "Yes" to proceed or "No" for Main Menu :, '
    else: 
      error_message = f'\nInvalid input, Type {valid_inputs[:-1]} to continue, "{break_flag}" to head back {f'or "{exit_flag}" to quit program' if exit_flag else ''}'
    
    if attempts:
      attempt_message = f'\n{"attempts" if attempts > 1 else "attempt" } left until you exited out program!' 
      user_input = inputFunc(f'\n{error_message} {f"\n{attempts}{attempt_message}" if attempts <= attemptsMessage_at else ""}\nEnter input: ')
    else: 
      user_input = inputFunc(f'\n{error_message}\nEnter input: ')

    if user_input in valid_inputs: return user_input
    if user_input == 'no' and close_match: break
    if user_input == 'yes' and close_match : user_input = close_match[0]; return user_input
    if attempts <= 1:raise SystemExit(f'\nYou have exceeded the maximum number of attempts, Exiting program') 

    attempts -= 1 
  
def inputHandler (valid_inputs,input_message, **error_kwargs):

  attempts = error_kwargs.get('attempts', 5)
  attemptsMessage_at = error_kwargs.get('attemptsMessage_at', 3)
  break_flag = error_kwargs.get('break_flag', 'main menu')
  exit_flag = error_kwargs.get('exit_flag', 'exit')

  valid_inputs = ConcatInputs(valid_inputs, break_flag, exit_flag)

  try:
    user_input = inputFunc(input_message)
    if user_input not in valid_inputs: 
      return error_prompt(valid_inputs, user_input, **error_kwargs)
    return user_input
  except SystemExit as e:exit()

def find_file(filename, directory = pathlib.Path.cwd()):
  for file in directory.rglob(filename):
    return file
  return None


user_input = None; close_match = None; break_flag = 'main menu';exit_flag = 'exit'

while (user_input != exit_flag):
  valid_inputs = 'view','create','modify'
  message = f'{'Welcome to the Directory creator' if not user_input else ''} \nDo you wish to {list(valid_inputs)} directory?' 
  message += f'\nType {list(valid_inputs)} or "{exit_flag}" to cancel:\nEnter input: '

  user_input = inputHandler(valid_inputs,message)

  if user_input == valid_inputs[0]:
    if os_type in Known_OS_systems:
      valid_inputs_02 = 'search'
      message_2 = f'\nPlease provide directory of file path you wish to view or Type "{valid_inputs_02}" ' 
      message_2 += f'to look for directory of file\nEnter input: '
      user_input_02 = inputFunc(message_2)
      close_match = difflib.get_close_matches(user_input_02, valid_inputs_02, n=1)
      
      if close_match and user_input_02 not in valid_inputs_02: 
        message_3 = f'\nInvalid input,Type {valid_inputs_02} or {exit_flag}: '
        user_input_02 = inputHandler(valid_inputs_02, message_3)

      if user_input_02 in valid_inputs_02:

        message_04 = f'\nType _File Name_ and _Directory_ to begin search, or type _File Name_ and "current" to search Current Directory\n'
        message_04 += f'Or type _File Name_ and "all" to search all directories\n'
        message_04 += '*Note that searching all Directories will start from the root directory (/),'.upper()
        message_04 += 'so it will search your entire PC."\n"Be aware that this can take a long time if you have a lot of files.*'.upper()
        display(message_04)
        user_input_03 = inputFunc(f'\nEnter filename: ')
        user_input_04 = inputFunc(f'\nEnter directory name or "current" to get current directories \nor "all" to search all directories: ')
        exit()
        if isinstance(user_input_03, tuple):
          directory = pathlib.Path('/') if user_input_03[1] == 'all' else user_input_03[1]
        else: directory = pathlib.Path.cwd()
        
        try:
          file = find_file(user_input_03[0], directory)
        except FileNotFoundError as e:print(f'File not found, {e}')
       
      if user_input_02 != exit_flag and user_input_02 not in valid_inputs_02: 
        try:
          Known_OS_systems[os_type](user_input_02) 
          print('Directory opened succesfuly!')
        except FileNotFoundError as e:
          print(f'\nFile not found, {e}')

      

      
