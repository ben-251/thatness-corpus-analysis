# Introduction
I'm going to be analysing complex sentences, specifically ones with noun clauses.

I'll analyse a large sample of text, to see when "that" is included between the main clause and noun clause, for example:

> I think (that) bananas are purple.

Specifically, I want to find out whether the "complexity" of the subject of the noun clause affects the probability of "that" occuring. 

_Note: this peoject requires the bentests module available [here.](https://github.com/ben-251/ben-tests)_

# Defining complexity
For now I'm over-reducing the problem, dividing all noun phrases into two groups:

## 1. Simple noun phrase subjects
Pronouns are the easiest to identify, so I will count any subject pronouns as complete subjects.
"I think that [I, you, he, she, we, they] like(s) soup"  

I may also add common subject names within the document (so if i was analysing _Harry Potter_ I might automatically add "Harry" and "Harry Potter" to my list)

## 2. "Complex" big subjects
"I think that a ... "    
"I think that the ... "  
Of course these could just be "a dog" or "the world" but I'm making this easy to work with.

## 3. Everything else (unknown)
- "I think that _my dog_ likes soup" ("my dog" is lengthy for my purposes)
- "I think that _Gwendolyn_ likes soup (unwhitelisted first name)
- "I think that _the person who hit me yesterday_ likes soup" 

## 4. Invalid
- "I think so."
- "I think of france in the winter" 
- "I think about this day"
- "I think [conj]"

In the future, rather than just having complexity be so discrete, I can measure the number of words in the subject. This initially seemed complicated, but I can just count the number of words after the verb (or the verb that, but the "that" is trimmed anyway) and treat that all as the nounphrase. this assumes the sentence does not have many clauses chained (i think that soup is hot and you think it is too.) but that's still far better than not considering this at all. I could then have a value called "thatness" that takes in to account size AND type. also allows me to immediately discount any "nounphrases" that are 1 word in length (i think that too; i think green. i think french) 

# What verb to use?
There are tons of candidates, but I think I want to select ones that are very commonly used, and rarely act on simple objects

So not:
"I _guessed_ 'green'" vs "I _guessed_ the right answer was 'green'"
"I _worried_ him" vs "I _worried_ she might be sick"
"I _understand_ Whales." vs "I _understand_ you're concerned
"I _believe_ her." vs "I _believe_ he has escaped his cell"

But words like:
- "I _agree_ that she might be sick" ('I _agree_ this' doesn't work)
- "I _think_ that he has won" ('I _think_ John' does sort of work, but is fairly rare)

Thankfully in a program this will just be a string (and it's tenses) so this should be easily changeable.



