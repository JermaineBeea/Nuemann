import difflib
import pathlib
import numpy as np

# Concatenates valid inputs with break and exit flags, and converts them to lowercase
def ConcatInputs(valid_inputs, break_flag, exit_flag): 
  valid_inputs = [str(input).lower() for input in valid_inputs]
  valid_inputs.extend([break_flag, exit_flag])  
  valid_inputs = np.array(valid_inputs)
  return valid_inputs

# Takes user input and converts it to lowercase
def inputFunc(input_message):
  user_input = input(input_message).lower()
  return user_input

# Handles error prompts for invalid user inputs
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
  
# Handles user input and checks if it's valid
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

# Finds a file in the current directory or its subdirectories
def find_file(filename, directory = pathlib.Path.cwd()):
  for file in directory.rglob(filename):
    return file
  return None