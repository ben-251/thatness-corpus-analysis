from bentests import asserts, testGroup, test_all
from analyser import Analyser, Sentence, subjectType
from importer import DataHandler
from think_words import think_words

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

	def test_remove_that(self):
		sentence = Sentence("I think that they know the monkey.")
		sentence.remove_that()
		asserts.assertEquals(
			sentence.sentence,
			["i","think","they","know","the","monkey"]
		)

	def test_find_think_simple(self):
		analyser = Sentence("i think they know the monkey.")
		positions = analyser.find_verb_positions()
		asserts.assertEquals(
			positions,
			[1]
		)

	def testFindThinkHarder(self):
		analyser = Sentence("the small-winged puffin sometimes thinks gold is grass.")
		positions = analyser.find_verb_positions()
		asserts.assertEquals(
			positions,
			[4]
		)



	def test_find_think_harder_that(self):
		analyser = Sentence("the small-winged puffin sometimes thinks that gold is grass.")
		positions = analyser.find_verb_positions()
		asserts.assertEquals(
			positions,
			[4]
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
			subjectType.SIMPLE
		)

	def test_subject_type_invalid(self):
		analyser = Sentence("I thought so.")
		type_ = analyser.get_subject_type(1)
		asserts.assertEquals(
			type_,
			subjectType.INVALID
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
	data
)