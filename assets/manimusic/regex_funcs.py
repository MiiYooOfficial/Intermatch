import re

def extract_number(string):
  pattern = r"-?\d+" 
  matches = re.findall(pattern, string)
  if not matches:
    return 0
  return int(matches[0])

def fm(string:str, split_str="|"):
  return string.strip().split(split_str)

def count_trailing_dots(string):
  pattern = r"\.*$"
  matches = re.search(pattern, string)
  if matches:
    trailing_dots = matches.group().count(".")
    return trailing_dots
  return 0

def count_trailing_underscore(string):
  pattern = r"_*$"
  matches = re.search(pattern, string)
  if matches:
    trailing_dots = matches.group().count("_")
    return trailing_dots
  return 0

