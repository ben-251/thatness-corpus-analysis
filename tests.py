from bentests import asserts, testGroup, test_all
from analyser import Analyser, Sentence, subjectType
import analyser
from datahandler import DataHandler
from verb_forms import think_words

class Main(testGroup):
	def test_raw_text(self):
		sentence = Sentence("I think they know where Greece is NOT.")
		asserts.assertEquals(
			sentence.raw_text, "I think they know where Greece is NOT."
		)

	def test_extract_sentence_words(self):
		sentence = Sentence("I think they know where Greece is NOT.")
		asserts.assertEquals(
			sentence.sentence, ["i", "think", "they", "know", "where", "greece", "is", "not"]
		)

	def test_strip_delimiters(self):
		sentence = Sentence("I think, they. know. where Greece is NOT.")
		asserts.assertEquals(
			sentence.sentence, ["i", "think", "they", "know", "where", "greece", "is", "not"]
		)		

	def test_remove_that(self):
		sentence = Sentence("I think that they know the monkey.")
		asserts.assertEquals(
			sentence.sentence,
			["i","think","they","know","the","monkey"]
		)

	def test_find_think_simple(self):
		analyser = Sentence("i think they know the monkey.")
		position = analyser.find_verb_position()
		asserts.assertEquals(
			position,
			1
		)

	def testFindThinkHarder(self):
		analyser = Sentence("the small-winged puffin sometimes thinks gold is grass.")
		position = analyser.find_verb_position()
		asserts.assertEquals(
			position,
			4
		)



	def test_find_think_harder_that(self):
		analyser = Sentence("the small-winged puffin sometimes thinks that dogs think of grass.")
		position = analyser.find_verb_position()
		asserts.assertEquals(
			position,
			4
		)

	def test_think_comes_first(self):
		analyser = Sentence("think about this word first")
		position = analyser.find_verb_position()
		asserts.assertEquals(
			position,
			0
		)

	def test_final_analysis(self):
		analyser = Analyser()
		result = analyser.interpret_thatness([
			(1, 1),
			(0, 1),
			(1, 1),
			(1, 1),
			(1, 2),
			(1, 1),
			(0, 2)
		])

		asserts.assertEquals(
			result,
			(1.2, 1.5)
		)

	def test_final_analysis_strip(self):
		analyser = Analyser()
		result = analyser.interpret_thatness([
			(1, 1),
			(0, 1),
			(1, 1),
			(1, 1),
			(1, -1),
			(1, -1),
			(1, -1),
			(1, -1),
			(0, 0),
			(-1, 0),
			(1, 2),
			(1, 1),
			(0, 2)
		])

		asserts.assertEquals(
			result,
			(1.2, 1.5)
		)
	
class subject_type(testGroup):
	def test_think_comes_first(self):
		analyser = Sentence("think about the order of your words")
		type_ = analyser.get_subject_type(0)
		asserts.assertEquals(
			type_,
			subjectType.INVALID
		)		

	def test_subject_type_simple(self):
		analyser = Sentence("I think i know the monkey.")
		type_ = analyser.get_subject_type(1)
		asserts.assertEquals(
			type_,
			subjectType.SIMPLE
		)

	def test_subject_type_simple_that(self):
		analyser = Sentence("I think that i know the monkey.")
		type_ = analyser.get_subject_type(1)
		asserts.assertEquals(
			type_,
			subjectType.SIMPLE
		)

	def test_subject_type_complex_past(self):
		analyser = Sentence("I thought the dog knew the monkey.")
		type_ = analyser.get_subject_type(1)
		asserts.assertEquals(
			type_,
			subjectType.COMPLEX
		)


	def test_subject_type_complex_non_pronoun(self):
		analyser = Sentence("Greg thought that the dog knew the monkey.")
		type_ = analyser.get_subject_type(1)
		asserts.assertEquals(
			type_,
			subjectType.COMPLEX
		)

	def test_subject_type_simple_with_later_clause(self):
		# Should still treat as simple
		analyser = Sentence("Greg thought that I liked soup, but I didn't.")
		type_ = analyser.get_subject_type(1)
		asserts.assertEquals(
			type_,
			subjectType.SIMPLE
		)


	def test_subject_type_invalid_conjunction(self):
		# Should still treat as invalid, since a conjuction after "that" implies the clause has ended early
		analyser = Sentence("Greg thought that but I didn't want to wake him.")
		type_ = analyser.get_subject_type(1)
		asserts.assertEquals(
			type_,
			subjectType.INVALID
		)

	def test_subject_type_invalid(self):
		analyser = Sentence("I thought so.")
		type_ = analyser.get_subject_type(1)
		asserts.assertEquals(
			type_,
			subjectType.INVALID
		)

	def test_analyse_first_line(self):
		# sentence = Sentence("I thought that might be right.")
		analyser = Analyser(source_path="test_text.txt")
		thatness, complexity = analyser.analyse_first()
		asserts.assertEquals(
			[thatness, complexity],
			[0,1]
		)

	def test_analyse_first_line_no_verb(self):
		# sentence = Sentence("I thought that might be right.")
		analyser = Analyser(source_path="test_text_no_verb.txt")
		thatness, complexity = analyser.analyse_first()
		asserts.assertEquals(
			[thatness, complexity],
			[0,-1] # goes to first sentence with the verb
		)

	def test_get_complexity_simple(self):
		current_sentence = Sentence("I think he's asleep")
		subject_type = current_sentence.get_subject_type(1)
			
		complexity = subject_type.get_complexity()
		asserts.assertEquals(
			complexity,
			1
		)

	def test_get_complexity_complex(self):
		current_sentence = Sentence("I think that but is asleep")
		subject_type = current_sentence.get_subject_type(1)
			
		complexity = subject_type.get_complexity()
		asserts.assertEquals(
			complexity,
			-1
		)
	
	def test_get_all_data(self):
		analyser = Analyser(source_path="test_text.txt")
		result = analyser.analyse_all()
		asserts.assertEquals(
			result,
			[
				(0,1),
				(0,-1),
				(0,2),
				(1,-1),
				(0,-1)
			]
		)
	


class enum_group(testGroup):
	def test_enum_subject_type(self):
		asserts.assertEquals(subjectType.get_subject_type("i"), subjectType.SIMPLE)

class data(testGroup):
	def testLoad(self):
		data_handler = DataHandler("test_text.txt")
		results =  [line  for line in data_handler.lazy_load()]
		asserts.assertEquals(
			results,
			[
				"jake thinks he's won",
				"amy thinks not",
				"i think the way to greece is through that path over there.",
				"you thought that was correct",
				"dogs like some cats.",
				"i wish i thought about this",
				"greg wants soup"	
			]
		)

	def testSearch(self):
		data_handler = DataHandler("test_text.txt")
		results =  [line  for line in data_handler.lazy_search(think_words)]
		asserts.assertEquals(
			results,
			[
				"jake thinks he's won",
				"amy thinks not",
				"i think the way to greece is through that path over there.",
				"you thought that was correct",
				"i wish i thought about this" # this is of course invalid, but the lazy search isn't supposed to compute that.
			]
		)





test_all(
	Main,
	enum_group,
	subject_type,
	data
)