from typing import Generator, List, Optional, Tuple
from datahandler import DataHandler
from verb_forms import think_words
from sentence import Sentence, subjectType

TEST_PATH = "test_text.txt"




data_handler = DataHandler()
class Analyser:
	def __init__(self, verb_list=None, source_path:Optional[str]=None) -> None:
		verb_list = think_words if verb_list is None else verb_list 
		self.source_path =  source_path # None is fine
		self.verb_list:List[str] = verb_list

	def analyse_next_line(self) -> Generator[Tuple[int, int], None, None]:
		# lazy function to get the next sentence with a "think", and then get the thatness and complexity scores
		'''
		Returns None if the verb is not present
		'''
		quick_data_handler = DataHandler(self.source_path)
		for line in quick_data_handler.lazy_search(self.verb_list):
			thatness: int = 0
			complexity: int = 0

			current_sentence = Sentence(line, verb_forms=self.verb_list)
			try:
				verb_position = current_sentence.find_verb_position()
			except:
				return 
			subject_type = current_sentence.get_subject_type(verb_position)
			
			complexity = subject_type.get_complexity()
			thatness = int(current_sentence.contains_that)
			
			yield thatness, complexity

	def get_all_analyses(self) -> List[Tuple[int,int]]:
		results = []
		for result in self.analyse_next_line():
			results.append(result) # obviously atm this undermines the whole point of yielding, but with yield, now i can easily change when we stop going
		return results

	def analyse_all(self, write_path=None):
		results = self.get_all_analyses()
		that_complexity_avg, not_that_complexity_avg = self.interpret_thatness(results)
		if not write_path is None:
			data_handler.write_complexities(
				write_path,
				that_complexity_avg,
				not_that_complexity_avg,
				word_root = self.verb_list[0]
			)


	def analyse_first(self):
		return next(self.analyse_next_line())

	def interpret_thatness(self, thatness_scores:List[Tuple[int, int]]):
		# checking how average complexity is affected by thatness (or could make a logistic regression?)
		stripped_scores = [
			(thatness, complexity) for thatness, complexity in thatness_scores if complexity not in (
				subjectType.INVALID.complexity, subjectType.UNKNOWN.complexity
			)
		]
		containing_that = [complexity for thatness, complexity in stripped_scores if thatness]
		not_containing_that = [complexity for thatness, complexity in stripped_scores if not thatness]

		that_avg = sum(containing_that) / len(containing_that) if containing_that else 0
		not_that_avg = sum(not_containing_that) / len(not_containing_that) if not_containing_that else 0

		return that_avg, not_that_avg
