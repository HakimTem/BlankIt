import random
from string import punctuation

common_words = []
with open("common_words.txt", "r") as f:  
  for line in f: 
    common_words += [line.replace("\n", "")]

#taken from https://www.delftstack.com/howto/python/how-to-split-string-with-multiple-delimiters-in-python/
import re
def custom_split(sepr_list, str_to_split):
    # create regular expression dynamically
    regular_exp = '|'.join(map(re.escape, sepr_list))
    return re.split(regular_exp, str_to_split)


def extract_sentence(text):
  candidates = custom_split(".?", text)[:-1]
  return candidates[random.randint(0, len(candidates) - 1)]

def create_question(text): 
  splitted = extract_sentence(text.replace(",", "")).split(" ")
  replaced_word = ""
  while True:
    randomIndex = random.randint(0, len(splitted) - 1)
    if splitted[randomIndex].lower() not in common_words and splitted[randomIndex] != " ":
       replaced_word = splitted[randomIndex]
       splitted[randomIndex] = "___"
       break
  return (" ".join(splitted), replaced_word)