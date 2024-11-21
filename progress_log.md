# 14 Nov
The tests all passed, meaning I can now take a sentence and immediately know what type of noun_phrase the "think" is, and whether there's a that or not (these two together form the basis of this entire analysis)

Todo:
- [ ] Import the sentences from txt file
- [ ] find out how often "that" is inserted, based on the type of noun_phrase

# 15 Nov
use R so just make csv of thatness and complexity

also I just realised each sentence should only take the first that.
"i think that you think"
"maybe it is best if you think about"

I definitely need to allow in-betweens though:
"I don't think"
"I won't think"
"I was thinking"
etc