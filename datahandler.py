from typing import List, Optional
from sentence import Sentence

class DataHandler:
	def __init__(self, file_name=None) -> None:
		if file_name is None:
			file_name = "data/ted2020.txt"
		self.file_name = file_name

	
	def lazy_load(self):
		with open(self.file_name, 'r', encoding='utf-8') as f:
			for sentence in f: # "each line <-> sentence"
				#TODO: fix error where i think the quotation mark or something is not getting imported. maybe strip all punctuation manually
				# it says UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d in position 7977: character maps to <undefined>
				# might also just be the newline?
				
				yield sentence.strip().lower()

	def lazy_search(self, queries:List[str]):
		for sentence in self.lazy_load():
			word_list =  Sentence(sentence).sentence 
			if any(query in word_list for query in queries):
				yield sentence


	def write_complexities(self, write_path:str, that_complexity_avg, not_that_complexity_avg):
		with open(write_path, "w") as f:
			f.write(
				f"with: {that_complexity_avg}\nwithout: {not_that_complexity_avg}"
			)