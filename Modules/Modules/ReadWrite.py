import os
import pathlib
import pickle
import platform
import subprocess
import logging as log
import pandas as pd
import numpy as np

os_type = platform.system()
Known_OS_systems = {
'Windows': lambda path: os.startfile(path),
'Linux': lambda path: subprocess.run(['xdg-open', path]),
'Darwin': lambda path: subprocess.run(['open', path])
}

def inputFunc(input_message):
  user_input = input(input_message).lower()
  return user_input

def find_file(filename, directory = pathlib.cwd()):
  for file in directory.rglob(filename):
    return file
  return None

if __name__ == '__main__':
  data = [[1,2,3,19], [5,6,7,14], [9,10,11,12]]
