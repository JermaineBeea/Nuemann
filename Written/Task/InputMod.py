import os, sys, subprocess, difflib

def inputFunc(input_message):
  user_input = input(input_message).lower()
  return user_input

def error_prompt(valid_inputs, user_input, **kwargs):

  attempts = kwargs.get('attempts', 5)
  attemptsMessage_at = kwargs.get('attemptsMessage_at', 3)
  exit_flag = kwargs.get('exit_flag', 'exit')
  valid_inputs = valid_inputs + [exit_flag]
  while True:
    close_match = difflib.get_close_matches(user_input, valid_inputs, n=1)
    if close_match: 
      error_message = f'Invalid input, did you intend to type {close_match[0]}?, Type "Yes" or "No" to continue:, '
    else: 
      error_message = f'Invalid input, Type {valid_inputs[:-1]} to continue {f'or {exit_flag} to quit program' if exit_flag else ''}'
    
    if attempts:
      attempt_message = f' {"attempts" if attempts > 1 else "attempt" } left until you exited out program!' 
      user_input = inputFunc(f'{error_message} {f"\n{attempts}{attempt_message}" if attempts <= attemptsMessage_at else ""}\nEnter input: ')
    else: 
      user_input = inputFunc(f'{error_message}\nEnter input: ')

    if user_input in valid_inputs: return user_input
    if user_input == 'no' and close_match: break
    if user_input == 'yes' and close_match : user_input = close_match[0]; return user_input
    if attempts <= 1:
      raise SystemExit(f'You have exceeded the maximum number of attempts, Exiting program')
    
    attempts -= 1 
  return user_input

def inputHandler (input_message, valid_inputs, **error_kwargs):
  try:
    user_input = inputFunc(input_message)
    if user_input not in valid_inputs: 
      return error_prompt(valid_inputs, user_input, **error_kwargs)
    return user_input
  except SystemExit as e:
    print(e); exit()

