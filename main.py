from typing import List, Tuple
from analyser import Analyser
from datahandler import DataHandler
import sentence
from verb_forms import think_words

analyser = Analyser()

def first_test():
	results = []
	BATCH_SIZE = 2300
	i = 0
	for result in analyser.analyse_next_line():
		results.append(result)
		i += 1
		if i >= BATCH_SIZE:
			break
	print(results)
	

def second_test():
	datahandler = DataHandler()
	for raw_sentence in datahandler.lazy_search(think_words):
		result = sentence.Sentence(raw_sentence)
		position = result.find_verb_position()
		print(result.get_subject_type(position))

# first_test()
# second_test()

def main():
	# SOURCE = "data\\ted2020.txt"
	bases = ["en.txt", "ted2020.txt"]
	for base in bases:
		source = "data\\" + base
		write = "write\\" + base
		analyser = Analyser(source_path=source)
		analyser.analyse_all(write_path=write)
		#results:List[Tuple[int, int]] = analyser.analyse_all(write_path = "results\\enResults.txt")
		#thatness_avg, not_thatness_avg = analyser.interpret_thatness(results)
		#print(f"Average complexity with 'That': {thatness_avg}\nAverage complexity without 'That': {not_thatness_avg}")

main()