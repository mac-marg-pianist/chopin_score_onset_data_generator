def convert_float(num):
  try:
    return float("{:.8f}".format(num))
  except ValueError:
    return num