from typing import List

class DataHandler:
	def __init__(self, file_name=None) -> None:
		if file_name is None:
			file_name = "data/ted2020.txt"
		self.file_name = file_name

	
	def lazy_load(self):
		with open(self.file_name, 'r') as file:
			for sentence in file: # "each line <-> sentence"
				yield sentence.strip().lower()

	def lazy_search(self, queries:List[str]):
		for sentence in self.lazy_load():
			if any(query in sentence for query in queries):
				yield sentence