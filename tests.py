import bentests as bt
from analyser import Sentence, subjectType
import analyser

class Main(bt.testGroup):
	def test_find_think_simple(self):
		analyser = Sentence("i think they know the monkey.")
		positions = analyser.find_verb_positions()
		bt.assertEquals(
			positions,
			[1]
		)

	def test_find_think_harder(self):
		analyser = Sentence("the small-winged puffin sometimes thinks gold is grass.")
		positions = analyser.find_verb_positions()
		bt.assertEquals(
			positions,
			[4]
		)

	def test_remove_that(self):
		sentence = Sentence("I think that they know the monkey.")
		sentence.remove_that()
		bt.assertEquals(
			sentence.sentence,
			["i","think","they","know","the","monkey"]
		)

	def test_find_think_harder_that(self):
		analyser = Sentence("the small-winged puffin sometimes thinks that gold is grass.")
		positions = analyser.find_verb_positions()
		bt.assertEquals(
			positions,
			[4]
		)

	def test_subject_type_simple(self):
		analyser = Sentence("I think i know the monkey.")
		type_ = analyser.get_subject_type(1)
		bt.assertEquals(
			type_,
			subjectType.SIMPLE
		)

	def test_subject_type_simple_that(self):
		analyser = Sentence("I think that i know the monkey.")
		type_ = analyser.get_subject_type(1)
		bt.assertEquals(
			type_,
			subjectType.SIMPLE
		)

	def test_subject_type_complex_past(self):
		analyser = Sentence("I thought the dog knew the monkey.")
		type_ = analyser.get_subject_type(1)
		bt.assertEquals(
			type_,
			subjectType.COMPLEX
		)


	def test_subject_type_complex_non_pronoun(self):
		analyser = Sentence("Greg thought that the dog knows the monkey.")
		type_ = analyser.get_subject_type(1)
		bt.assertEquals(
			type_,
			subjectType.COMPLEX
		)

	def test_subject_type_invalid(self):
		analyser = Sentence("I thought so.")
		type_ = analyser.get_subject_type(1)
		bt.assertEquals(
			type_,
			subjectType.INVALID
		)


class enum_group(bt.testGroup):
	def test_enum_subject_type(self):
		bt.assertEquals(subjectType.get_subject_type("i"), subjectType.SIMPLE)




bt.test_all(
	Main,
	enum_group
)