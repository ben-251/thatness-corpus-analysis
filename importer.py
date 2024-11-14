
class DataHandler:
	def __init__(self, file_name=None) -> None:
		if file_name is None:
			file_name = "ted2020.txt"
		self.file_name = file_name

	
	def lazy_load(self):
		with open(self.file_name, 'r') as file:
			for sentence in file: # "each line <-> sentence"
				yield sentence.strip().lower()

	