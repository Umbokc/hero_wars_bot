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