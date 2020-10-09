import os.path
from os import path
import numpy as np

class AttrDict(dict):
  def __init__(self, *args, **kwargs):
    super(AttrDict, self).__init__(*args, **kwargs)
    self.__dict__ = self

def findMiddle(input_list):
  middle = float(len(input_list))/2
  if middle % 2 != 0:
    return input_list[int(middle - .5)]
  else:
    return input_list[int(middle)]

def file_to_bytes(file):
  with open(file, 'rb') as f:
    raw = f.read()
  return raw

def file_exist(file_name):
  return path.exists(file_name)

def has_intersection(lst, item, sensity=0):
  first = lst[0]
  last = lst[-1]
  last2 = last+sensity

  if item in [first, last, last2] or (item > first and (item < last or item < last2)):
    return True

  return False

def chunks(l, n):
  res = np.array_split(l,n)
  new_array = []

  for x in res:
    if len(x):
      new_array.append(x[0])

  return new_array