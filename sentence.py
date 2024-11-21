from enum import Enum, auto
from typing import List
from verb_forms import think_words
class VerbNotFoundError(BaseException): ...


conjunctions = [
	"and", "but", "or", "nor", "for", "so", "yet", "although", "because", "since",
	"if", "unless", "until", "while", "whereas", "as",
	"before", "after", "when", "whenever", "where", "wherever", "not"
]


#  (they, we, you) are in a group, (he, she) and then (I)
i_list = ["i"]
he_she = ["he", "she"]
others = ["they", "we", "you"]

simple_pronouns = i_list + he_she + others
future_pronouns = [word + "'ll" for word in simple_pronouns]
past_pronouns = [word + "'ve" for word in others+i_list] + [word + "'s" for word in he_she]
be_pronouns = [word + "'s" for word in he_she] + [word + "'re" for word in others] + ["i'm"]

be_verbs = ["is","was"]

articles = [ "a", "the", "an"]
demonstratives = ["this", "those", "these"]
posessives = ["my", "your", "his", "her", "its", "our", "their"]
quantifiers = ["some", "any", "no", "many", "few", "much", "little", "several", "all", "both", "each", "every", "either", "neither"]
determiners = articles + demonstratives + posessives

class subjectType(Enum):
	SIMPLE = (
		simple_pronouns + future_pronouns + past_pronouns + be_pronouns,
		1
	)
	COMPLEX = (determiners, 2)
	INVALID = (["so", "of", "about"] + conjunctions + be_verbs, # sentences that aren't useful for this analysis
		-1)
	UNKNOWN = (["DEFAULT"], # also not useful, but less sure
		0)

	def __init__(self, words, complexity):
		self.words = words
		self.complexity = complexity
		
	@classmethod
	def get_subject_type(cls, word: str):
		for subjectType in cls:
			if word in subjectType.words:
				return subjectType
		return cls.UNKNOWN

	def get_complexity(self) -> int:
		return self.complexity
		


class Sentence:
	def __init__(self, raw_text:str, verb_forms=None) -> None:
		'''
		Remove "that" and store the thatness

		'I think that this is right'
		first whitelist for subjects in subject phrase
		first black list for words immediately following verb
		second whitelist for valid subjects in noun phrase 
		
		'''
		self.verb_forms = think_words if verb_forms is None else verb_forms
		self.SUBJECT_PHRASE_WHITELIST = [
			"i", "you", "we", "he", "she", "they",  # SHE thinks he ate soup
			"it"
		]
		self.contains_that = False 
		self.raw_text = raw_text
		if raw_text == "":
			self.sentence = [""] 
			return
		self.sentence = self.tidy(raw_text)
		self.clear_delimiters()
		self.remove_that()

	def clear_delimiters(self):
		self.sentence = [word.rstrip(",.") for word in self.sentence]

	def tidy(self, raw_sentence:str) -> List[str]:
		sentence = raw_sentence.lower().split()
		sentence[-1] = sentence[-1][:-1] if sentence[-1][-1] == "." else sentence[-1]
		return sentence

	def remove_that(self):
		try:
			verb_position = self.find_verb_position()
			if verb_position >= len(self.sentence) - 1:
				return
			next_word_position = verb_position + 1
			next_word = self.sentence[next_word_position]
			if next_word == "that":
				self.contains_that = True # remember that this sentence had a that (for analysis later)
				self.sentence.pop(next_word_position)
		except VerbNotFoundError:
			self.contains_that = False
			return

	def find_verb_position(self) -> int:
		'''
		Finds the first occurence of the query verb within the sentence.
		'''
		# Sentence is assumed to be lowercase
		for i, word in enumerate(self.sentence):
			if word in self.verb_forms:				
				return i

		raise VerbNotFoundError("Verb not found")

	def get_subject_type(self, verb_position):
		if verb_position >= len(self.sentence) - 1:
			return subjectType.INVALID
		next_word = self.sentence[verb_position + 1]
		# verb = sentence[verb_position]

		subject_type = subjectType.get_subject_type(next_word)
		return subject_type

	def check_all(self):
		subject_type = self.get_subject_type(self.find_verb_position())
		return subject_type
