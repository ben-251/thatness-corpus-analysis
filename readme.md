# Goal
I'm going to be analysing complex sentences, specifically ones with noun clauses.

I'll analyse a large sample of text, to see when "that" is included between the main clause and noun clause, for example:

> I think (that) bananas are purple.

Specifically, I want to find out whether the "complexity" of the subject of the noun clause affects the probability of "that" occuring. 

# Defining complexity
For now I'm over-reducing the problem, dividing all noun phrases into two groups:

## 1. Simple noun phrase subjects
I will call these "small" subjects to avoid using the words simple and complex for everything

Pronouns are the easiest to identify, so I will count any subject pronouns as complete subjects.
"I think that [I, you, he, she, we, they] like(s) soup"  

I may also add common subject names within the document (so if i was analysing _Harry Potter_ I might automatically add "Harry" and "Harry Potter" to my list)

## 2. "confirmed" big subjects
"I think that a ... "    
"I think that the ... "  
Of course these could just be "a dog" or "the world" but I'm making this easy to work with.

## 3. Everything else
- "I think that _my dog_ likes soup" ("my dog" is lengthy for my purposes)
- "I think that _Gwendolyn_ likes soup (unwhitelisted first name)
- "I think that _the person who hit me yesterday_ likes soup" 

In the future, rather than just having complexity be binary, I can measure the number of words in the subject. The reason this is too complicated for now is that I'd need to make syntax trees to be sure when the noun phrases start

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



