#python 3.7.0 64-bit
#py -3 -m pip install numpy==1.19.3
#py -3 -m pip install spacy==2.1.0
#py -3 -m pip install neuralcoref==4.0
#py -3 -m spacy download en_core_web_sm
#py -3 -m spacy download en_core_web_lg

import sys
import spacy
import neuralcoref
import re
import random

def get_aux_bin(sent):
  subj_found = False 
  verb_found = False 
  question = None
  for idx, token in enumerate(sent): 
    #locate verb index
    if token.dep_ == "ROOT": 
      verb_found = True 
    #locate subj index 
  if verb_found: 
    for idx, token in enumerate(sent): 
      if token.dep_ == "nsubj": 
        subj_found = True 
        subj_index = idx 
      if subj_found and token.pos_ == "AUX" and token.dep_ == "aux": 
        question = str(token).capitalize() + " " + str(sent[subj_index]).lower() + " " + str(sent[idx+1:])
        if question[-1] == '\n': 
          question.rstrip('\n')
        question = question[:-1].strip(".") + "?"
  return question

def get_vb_bin(sent): #not done yet 
  subj_found = False 
  verb_found = False 
  question = None 
  for idx, token in enumerate(sent): 
    if token.dep_ == "ROOT": 
      verb_found = True 
      verb_index = idx 
  if verb_found: 
    for idx, token in enumerate(sent): 
      if token.dep_ == "nsubj": 
        subj_found = True 
        subj_index = idx 

      # VBZ --> Does, VBP --> Do, VBD --> Did
      if subj_found and token.pos_ == 'VERB': 
        if token.tag_ == "VBZ": 
          question = "Does" + " " + str(sent[subj_index]) 
  return None

def get_who(sent): #also gets what
  verb_found = False
  subj_found = False
  type_found = False
  #locate verb index
  for idx, token in enumerate(sent):
    if token.dep_ == "ROOT": 
      #verb_index = idx
      verb_found = True
  #locate subj index
  for idx, token in enumerate(sent):
    if token.dep_ == "nsubj":
      subj_index = idx
      subj_found = True
      if token.ent_type_ == "ORG":
        question_type = "What"
        type_found = True
      if token.ent_type_ == "PERSON":
        question_type = "Who"
        type_found = True
  
  if verb_found and subj_found and type_found:
    question = question_type + " " + str(sent[subj_index+1]) + " " + str(sent[subj_index+2:])
    if question[-1] == "\n":
      question.rstrip("\n")
    question = question[:-1] + "?"
    return question

def get_what(sent): #feel like this is not needed since it's covered in get_who 
  '''
  verb_found = False 
  subj_found = False 
  type_found = False 
  for idx, token in enumerate(sent): 
    if token.dep_ == "ROOT":
      verb_found = True 
  for idx, token in enumerate(sent): 
  '''
  return None

def get_where(sent): #
  '''
  subj_found = False 
  type_found = False 
  verb_found = False 
  start = None  
  end = None 
  prepositions = ["at", "in", "from", "to", "on"]
  for ent in sent.ents: 
    if (ent.label_ == "GPE" or ent.label_ == "LOC" or ent.label_ == "ORG"):
      print(ent)
      prev_word = str(sent[ent.start-1]) # <-- error here for some reason 
      print(prev_word, ent, ent.start)
      if prev_word in prepositions: 
        print(prev_word)
  '''
  return None

def get_when(sent):
  return None

#not tested yet
def generate_questions(doc):
  question_list = []
  #parse/tokenize document
  for sent in doc.sents:
    token_list = [token.text for token in sent]
    if ("(" in token_list or ")" in token_list):
      pass
    if "." not in token_list: 
      pass
    #if some other rule
    else: 
      #print("\n")    
      #print(sent)    
      temp_qs = []
      temp_qs.append(get_aux_bin(sent))
      temp_qs.append(get_vb_bin(sent))
      #temp_qs.append(get_who(sent))
      temp_qs.append(get_what(sent))
      temp_qs.append(get_where(sent))
      temp_qs.append(get_when(sent))

      for q in temp_qs:
        if q != None:
          question_list.append(q)

  return question_list

def print_questions(question_list, n_questions):
  if len(question_list) < n_questions:
    print("Error: Not enough questions generated from text.")
  else:
    question_counter = 0
    while question_counter < n_questions:
      random_index = random.randint(0, len(question_list)-1)
      random_question = question_list.pop(random_index)
      print(random_question)
      question_counter += 1

def main():
  print("Starting...")

  if len(sys.argv) != 3:
    print("**USAGE ERROR*** ./ask article.txt nquestions")
    sys.exit(1)
  
  article_text = sys.argv[1]
  n_questions = sys.argv[2]
  n_questions = int(n_questions)

  with open(article_text, 'r', encoding = 'utf8') as f:
    text = f.read()
  newtext = text.split('\n\n') #list of sections
  nlp = spacy.load('en_core_web_sm')
  neuralcoref.add_to_pipe(nlp)
  print("makes past neuralcoref")
  final_question_list = []
  #newtext is a list of sections split by double newlines
  for section in newtext: 
    #print("NEW SECTION")
    #run nlp on each section
    doc = nlp(section)
    #print("SECTION DONE")
    #doc = doc._.coref_resolved
    question_list = generate_questions(doc)

    for question in question_list:
      final_question_list.append(question)

  #question_list = generate_questions(text)
  #question_list_test = ["what is my name?", "who are you?", "sup?", "gang?"]
  #function to print selected questions from question_list
  #print_questions(question_list_test, n_questions)
  print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n")
  print_questions(final_question_list, n_questions)


if __name__ == "__main__":
  main()
