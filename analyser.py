from typing import List
from importer import DataHandler
from enum import Enum, auto

class subjectType(Enum):
	SIMPLE = [
		"i", "you", "we", "he", "she", "they" # I think YOU ate soup	
	]
	COMPLEX = [  
		"a", "the", "an" # (I) think ((AN excellent example) is ('(I) think ((A great example) is ("(i) think ((THE best example) is (this sentence))"))'))
	]
	INVALID = ["so"] 
	UNKNOWN = ["DEFAULT"] # will never be called cuz everything is lowercase


	@classmethod
	def get_subject_type(cls, word: str):
		for subjectType in cls:
			if word in subjectType.value:
				return subjectType
		return cls.UNKNOWN

data_handler = DataHandler()

class Sentence:
	def __init__(self, raw_text:str, verb_forms=None) -> None:
		'''
		Remove "that" and store the thatness

		'I think that this is right'
		first whitelist for subjects in subject phrase
		first black list for words immediately following verb
		second whitelist for valid subjects in noun phrase 
		
		'''
		self.verb_forms = set(("think", "thought", "thinks")) if verb_forms is None else verb_forms
		self.SUBJECT_PHRASE_WHITELIST = [
			"i", "you", "we", "he", "she", "they",  # SHE thinks he ate soup
			"it"
		]
		self.contains_that = False 
		self.raw_text = raw_text
		self.sentence = self.tidy(raw_text)
		self.remove_that()

	def tidy(self, raw_sentence:str) -> List[str]:
		sentence = raw_sentence.lower().split()
		sentence[-1] = sentence[-1][:-1] if sentence[-1][-1] == "." else sentence[-1]
		return sentence

	def remove_that(self):
		verb_positions = self.find_verb_positions()
		for verb_index in verb_positions:
			next_word = self.sentence[verb_index+1]
			if next_word == "that":
				self.contains_that = True # remember that this sentence had a that (for analysis later)
				self.sentence.pop(verb_index+1)



	def find_verb_positions(self) -> List[int]:
		'''

		'''
		# Sentence is assumed to be lowercase
		positions = []
		for i in range(1, len(self.sentence)): # can safely start on 1 because verb should have a subject first
			# Find all occurences of the verb not necessarily after a noun. 
			word = self.sentence[i]
			prev_word = self.sentence[i - 1]
			next_word = self.sentence[i + 1] if i < len(self.sentence) - 1 else None 

			if not word in self.verb_forms:
				continue
			positions.append(i)
		return positions

	def get_subject_type(self, verb_position):
		next_word = self.sentence[verb_position+1]
		# verb = sentence[verb_position]

		subject_type = subjectType.get_subject_type(next_word)
		return subject_type

		

	def check_all(self):
		for verb_position in self.find_verb_positions():
			if self.get_subject_type(verb_position) is subjectType.COMPLEX:
				pass

			