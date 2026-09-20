"""
questions.py – Question banks by grade (1-6), subject, and difficulty (diff 1-5).

Door subjects:
    Door 1 → Grammar
    Door 2 → Vocabulary
    Door 3 → Science

Each grade has 60 questions per subject (12 per difficulty stage × 5 stages).
Stages get progressively harder: diff 1 = easiest, diff 5 = hardest.
Questions never repeat across grades.

Entry format: {q, opts, ans, cat, diff}
    q    – question text (keep short for the game UI)
    opts – list of exactly 4 answer strings
    ans  – index of the correct answer (0-3)
    cat  – category badge
    diff – difficulty stage 1-5
"""

# ─── Grammar question bank ────────────────────────────────────────────────────
GRAMMAR_QS = {

    # ── Grade 1 ──────────────────────────────────────────────────────────────
    1: [
        # diff 1 — nouns/verbs/adjectives, "to be", capital letters, end punctuation
        {"q": 'Which word names a person, place, or thing?', "opts": ["run", "cat", "happy", "and"], "ans": 1, "cat": "Grammar", "diff": 1},
        {"q": 'Which word is an action word?', "opts": ["dog", "jump", "blue", "the"], "ans": 1, "cat": "Grammar", "diff": 1},
        {"q": '"I ___ happy." Choose the correct word.', "opts": ["am", "is", "are", "be"], "ans": 0, "cat": "Grammar", "diff": 1},
        {"q": 'Which mark ends a telling sentence?', "opts": ["?", "!", ".", ","], "ans": 2, "cat": "Grammar", "diff": 1},
        {"q": '"She ___ my friend." Choose the correct word.', "opts": ["am", "is", "are", "be"], "ans": 1, "cat": "Grammar", "diff": 1},
        {"q": 'Which sentence is written correctly?', "opts": ["my name is Ana.", "My name is Ana.", "my Name is Ana.", "MY name is Ana."], "ans": 1, "cat": "Grammar", "diff": 1},
        {"q": '"They ___ students." Choose the correct word.', "opts": ["am", "is", "are", "be"], "ans": 2, "cat": "Grammar", "diff": 1},
        {"q": 'Which word describes how something looks?', "opts": ["run", "big", "dog", "the"], "ans": 1, "cat": "Grammar", "diff": 1},
        {"q": 'Which mark ends a question?', "opts": [".", "!", ",", "?"], "ans": 3, "cat": "Grammar", "diff": 1},
        {"q": '"He ___ my brother." Choose the correct word.', "opts": ["am", "is", "are", "be"], "ans": 1, "cat": "Grammar", "diff": 1},
        {"q": 'Which word is a noun (names a thing)?', "opts": ["jump", "happy", "book", "quickly"], "ans": 2, "cat": "Grammar", "diff": 1},
        {"q": '"We ___ friends." Choose the correct word.', "opts": ["am", "is", "are", "be"], "ans": 2, "cat": "Grammar", "diff": 1},

        # diff 2 — plurals -s/-es, articles a/an, pronouns he/she/they, simple present -s
        {"q": '"I have ___ apple." Choose the correct article.', "opts": ["a", "an", "the", "some"], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": 'What is the plural of "box"?', "opts": ["boxs", "boxes", "boxe", "boxxes"], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": 'Which pronoun replaces "the boy"?', "opts": ["she", "it", "he", "they"], "ans": 2, "cat": "Grammar", "diff": 2},
        {"q": '"The cat ___ on the mat." Choose the correct word.', "opts": ["sit", "sits", "sitting", "sitted"], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": 'Which mark ends an excited sentence?', "opts": [".", "?", ",", "!"], "ans": 3, "cat": "Grammar", "diff": 2},
        {"q": 'What is the plural of "class"?', "opts": ["class", "classs", "classes", "clases"], "ans": 2, "cat": "Grammar", "diff": 2},
        {"q": 'Which pronoun replaces "the girls"?', "opts": ["he", "she", "it", "they"], "ans": 3, "cat": "Grammar", "diff": 2},
        {"q": '"She ___ to school every day." Choose the correct word.', "opts": ["go", "goes", "going", "went"], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": '"___ is my friend." (a girl) Choose the correct pronoun.', "opts": ["Him", "Her", "She", "They"], "ans": 2, "cat": "Grammar", "diff": 2},
        {"q": 'Which word is NOT a noun?', "opts": ["house", "happy", "dog", "school"], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": '"I have ___ umbrella." Choose the correct article.', "opts": ["a", "an", "some", "any"], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": 'What is the plural of "bush"?', "opts": ["bushs", "bushes", "bush", "bushies"], "ans": 1, "cat": "Grammar", "diff": 2},

        # diff 3 — past tense -ed, adjective -er/-est, conjunctions and/but/because, prepositions
        {"q": 'What is the past tense of "walk"?', "opts": ["walk", "walks", "walked", "walking"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": '"She is ___ than her brother."', "opts": ["tall", "taller", "tallest", "most tall"], "ans": 1, "cat": "Grammar", "diff": 3},
        {"q": '"I was tired ___ I ran so far."', "opts": ["so", "and", "because", "but"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": '"The book is ___ the table." (below it)', "opts": ["on", "in", "under", "over"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": 'What is the past tense of "play"?', "opts": ["play", "plays", "played", "playing"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": '"She is the ___ student in the class."', "opts": ["tall", "taller", "tallest", "most tallest"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": '"I like cats ___ I don\'t like dogs."', "opts": ["and", "because", "or", "but"], "ans": 3, "cat": "Grammar", "diff": 3},
        {"q": '"The cat is ___ the box." (inside)', "opts": ["on", "in", "under", "over"], "ans": 1, "cat": "Grammar", "diff": 3},
        {"q": 'What is the past tense of "want"?', "opts": ["wantes", "wants", "wanted", "wanting"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": '"She is ___ than me."', "opts": ["short", "shorter", "shortest", "most short"], "ans": 1, "cat": "Grammar", "diff": 3},
        {"q": '"He likes ice cream ___ cake." (in addition)', "opts": ["but", "or", "and", "because"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": '"The bird is ___ the tree." (above)', "opts": ["under", "in", "on", "over"], "ans": 3, "cat": "Grammar", "diff": 3},

        # diff 4 — compound words, irregular plurals, contractions, subject identification
        {"q": 'Which is a compound word?', "opts": ["happy", "sunshine", "dog", "run"], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": 'What is the plural of "child"?', "opts": ["childs", "childes", "children", "childrens"], "ans": 2, "cat": "Grammar", "diff": 4},
        {"q": 'What is the short form of "do not"?', "opts": ["dont", "do'nt", "don't", "dn't"], "ans": 2, "cat": "Grammar", "diff": 4},
        {"q": 'Find the subject: "The little dog barked."', "opts": ["little", "dog", "barked", "The"], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": 'What is the plural of "foot"?', "opts": ["foots", "feets", "footes", "feet"], "ans": 3, "cat": "Grammar", "diff": 4},
        {"q": 'What is the short form of "I am"?', "opts": ["Im", "I'am", "I'm", "I' m"], "ans": 2, "cat": "Grammar", "diff": 4},
        {"q": 'Which is a compound word?', "opts": ["pencil", "school", "football", "jump"], "ans": 2, "cat": "Grammar", "diff": 4},
        {"q": 'What is the plural of "tooth"?', "opts": ["tooths", "teeths", "teeth", "toothes"], "ans": 2, "cat": "Grammar", "diff": 4},
        {"q": 'What is the short form of "cannot"?', "opts": ["cant", "can't", "ca'nt", "canno't"], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": 'Find the subject: "My teacher is kind."', "opts": ["My", "teacher", "is", "kind"], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": 'Which is a compound word?', "opts": ["fast", "rainbow", "cat", "big"], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": 'What is the plural of "mouse"?', "opts": ["mouses", "meese", "mice", "mices"], "ans": 2, "cat": "Grammar", "diff": 4},

        # diff 5 — comma lists, to/too/two, there/their/they're, compound sentences, synonyms/antonyms
        {"q": 'Which uses commas correctly in a list?', "opts": ["I like cats dogs and fish.", "I like cats, dogs, and fish.", "I like, cats, dogs, fish.", "I like cats, dogs and, fish."], "ans": 1, "cat": "Grammar", "diff": 5},
        {"q": 'Which uses "too" correctly?', "opts": ["I want too go.", "Too I want go.", "I want to go too.", "I want go to too."], "ans": 2, "cat": "Grammar", "diff": 5},
        {"q": '"___ going to school." (they are)', "opts": ["There", "Their", "They're", "There's"], "ans": 2, "cat": "Grammar", "diff": 5},
        {"q": '"I like dogs, ___ I also like cats."', "opts": ["or", "but", "and", "so"], "ans": 2, "cat": "Grammar", "diff": 5},
        {"q": 'Which uses "two" correctly?', "opts": ["I have too cats.", "I have to cats.", "I have tow cats.", "I have two cats."], "ans": 3, "cat": "Grammar", "diff": 5},
        {"q": '"___ books are on the table." (belonging to them)', "opts": ["There", "Their", "They're", "There is"], "ans": 1, "cat": "Grammar", "diff": 5},
        {"q": 'Which is a synonym for "big"?', "opts": ["small", "fast", "large", "cold"], "ans": 2, "cat": "Grammar", "diff": 5},
        {"q": '"___ a dog in the garden." (there is)', "opts": ["Their", "They're", "Theres", "There's"], "ans": 3, "cat": "Grammar", "diff": 5},
        {"q": 'Which is an antonym of "sad"?', "opts": ["unhappy", "tired", "slow", "happy"], "ans": 3, "cat": "Grammar", "diff": 5},
        {"q": '"She is tired, ___ she went to bed."', "opts": ["but", "or", "and", "so"], "ans": 3, "cat": "Grammar", "diff": 5},
        {"q": 'What is the past tense of "go"?', "opts": ["goed", "goes", "went", "going"], "ans": 2, "cat": "Grammar", "diff": 5},
        {"q": 'Choose the correct sentence.', "opts": ["He and I goes to school.", "Him and me go to school.", "He and I go to school.", "He and me goes to school."], "ans": 2, "cat": "Grammar", "diff": 5},
    ],

    # ── Grade 2 ──────────────────────────────────────────────────────────────
    2: [
        # diff 1 — subject-verb agreement, regular past -ed, subject pronouns, a/an/the
        {"q": 'Which sentence has correct subject-verb agreement?', "opts": ["The dogs barks.", "The dog bark.", "The dog barks.", "The dogs barking."], "ans": 2, "cat": "Grammar", "diff": 1},
        {"q": 'Which pronoun is correct: "___ went to the store." (a girl)', "opts": ["Him", "Her", "She", "Them"], "ans": 2, "cat": "Grammar", "diff": 1},
        {"q": 'What is the past tense of "help"?', "opts": ["help", "helps", "helped", "helping"], "ans": 2, "cat": "Grammar", "diff": 1},
        {"q": 'Which sentence uses "but" correctly?', "opts": ["I like cats, but I like dogs.", "I like cats but, I like dogs.", "I but like cats.", "But I like cats I like dogs."], "ans": 0, "cat": "Grammar", "diff": 1},
        {"q": 'Which pronoun replaces "Mary and Tom"?', "opts": ["he", "she", "they", "it"], "ans": 2, "cat": "Grammar", "diff": 1},
        {"q": 'What is the past tense of "jump"?', "opts": ["jump", "jumps", "jumped", "jumping"], "ans": 2, "cat": "Grammar", "diff": 1},
        {"q": '"___ cat is big." (the specific one)', "opts": ["A", "An", "The", "Some"], "ans": 2, "cat": "Grammar", "diff": 1},
        {"q": 'Which sentence is correct?', "opts": ["He don't like pizza.", "He doesn't like pizza.", "He not like pizza.", "He no likes pizza."], "ans": 1, "cat": "Grammar", "diff": 1},
        {"q": 'Which is a compound sentence?', "opts": ["The dog ran.", "Running dog.", "The dog ran and the cat jumped.", "Fast dog."], "ans": 2, "cat": "Grammar", "diff": 1},
        {"q": 'What is the past tense of "clean"?', "opts": ["cleaned", "cleans", "clean", "cleaning"], "ans": 0, "cat": "Grammar", "diff": 1},
        {"q": '"___ uniform is blue." (a uniform starts with "y" sound)', "opts": ["A", "An", "The", "Some"], "ans": 0, "cat": "Grammar", "diff": 1},
        {"q": 'Which sentence has correct subject-verb agreement?', "opts": ["The children plays.", "The child play.", "The children play.", "The childs plays."], "ans": 2, "cat": "Grammar", "diff": 1},

        # diff 2 — irregular past tense, "or" compound, possessives -'s, adverbs -ly
        {"q": 'What is the past tense of "eat"?', "opts": ["eated", "eats", "ate", "eating"], "ans": 2, "cat": "Grammar", "diff": 2},
        {"q": 'Which shows possession correctly?', "opts": ["the dogs bone", "the dog's bone", "the dogs' bone", "the dogs bone's"], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": 'What is the past tense of "run"?', "opts": ["runned", "runs", "ran", "running"], "ans": 2, "cat": "Grammar", "diff": 2},
        {"q": 'Which sentence uses "or" correctly?', "opts": ["You can have cake or pie.", "You can have cake, or.", "Or you can have cake pie.", "Cake or, you can have pie."], "ans": 0, "cat": "Grammar", "diff": 2},
        {"q": 'Which word is an adverb?', "opts": ["quick", "quickly", "quicker", "quickest"], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": 'What is the past tense of "see"?', "opts": ["seed", "sees", "saw", "seeing"], "ans": 2, "cat": "Grammar", "diff": 2},
        {"q": 'Which shows possession correctly? (for Maria)', "opts": ["Marias book", "Maria's book", "Marias' book", "Marias's book"], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": 'What is the past tense of "buy"?', "opts": ["buyed", "buys", "bought", "buying"], "ans": 2, "cat": "Grammar", "diff": 2},
        {"q": '"She sings ___." Which word completes it with an adverb?', "opts": ["beautiful", "beautifully", "beauty", "beautifull"], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": 'What is the past tense of "give"?', "opts": ["gived", "gives", "gave", "giving"], "ans": 2, "cat": "Grammar", "diff": 2},
        {"q": 'Which sentence uses "so" correctly?', "opts": ["I was tired so, I slept.", "I was tired, so I slept.", "So I was tired I slept.", "I was so tired, slept."], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": 'What is the past tense of "come"?', "opts": ["comed", "comes", "came", "coming"], "ans": 2, "cat": "Grammar", "diff": 2},

        # diff 3 — progressive tense, future "will", does/doesn't, comparative -er/-est
        {"q": 'Which sentence uses the present progressive?', "opts": ["She sings.", "She sang.", "She is singing.", "She will sing."], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": 'What is the correct comparative? (smart)', "opts": ["She is more smart than me.", "She is smartest than me.", "She is smarter than me.", "She is the most smart."], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": 'Which sentence is in the future tense?', "opts": ["I eat lunch.", "I ate lunch.", "I will eat lunch.", "I was eating."], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": '"Does she ___ English?" Choose the correct form.', "opts": ["speaks", "speak", "spoke", "speaking"], "ans": 1, "cat": "Grammar", "diff": 3},
        {"q": 'Which is the superlative form of "fast"?', "opts": ["faster", "fastest", "most fast", "more fast"], "ans": 1, "cat": "Grammar", "diff": 3},
        {"q": '"They ___ TV right now." Choose the correct form.', "opts": ["watch", "watches", "are watching", "watched"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": '"She ___ like vegetables." (negative present)', "opts": ["don't", "not", "doesn't", "isn't"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": 'Which sentence is in the future tense?', "opts": ["He ran home.", "He runs home.", "He is running home.", "He is going to run home."], "ans": 3, "cat": "Grammar", "diff": 3},
        {"q": '"___ they play soccer on weekends?"', "opts": ["Does", "Is", "Do", "Are"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": 'Which is the comparative form of "good"?', "opts": ["gooder", "goodest", "better", "more good"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": '"I ___ my homework right now."', "opts": ["do", "does", "am doing", "did"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": 'Which is the superlative of "bad"?', "opts": ["badder", "baddest", "worse", "worst"], "ans": 3, "cat": "Grammar", "diff": 3},

        # diff 4 — past progressive, much/many, relative pronouns, too/enough, indirect objects
        {"q": '"___ books do you have?" Choose the correct question word.', "opts": ["Much", "How many", "How much", "Any"], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": 'Which sentence uses the past progressive?', "opts": ["She slept.", "She was sleeping.", "She sleeps.", "She will sleep."], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": '"The man ___ fixed my car is my uncle." Choose the correct word.', "opts": ["what", "which", "who", "where"], "ans": 2, "cat": "Grammar", "diff": 4},
        {"q": '"There is ___ water in the glass." (a lot, uncountable)', "opts": ["many", "much", "a few", "lot of"], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": '"The soup is ___ hot to eat." Choose the correct word.', "opts": ["so", "very", "too", "enough"], "ans": 2, "cat": "Grammar", "diff": 4},
        {"q": '"She gave ___ a gift." (to him) Choose the correct pronoun.', "opts": ["he", "his", "him", "himself"], "ans": 2, "cat": "Grammar", "diff": 4},
        {"q": '"___ students were absent today?"', "opts": ["Much", "How many", "How much", "A lot"], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": 'Which sentence uses the past progressive?', "opts": ["We ate dinner.", "We were eating dinner.", "We eat dinner.", "We had eaten dinner."], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": '"The book ___ I read was interesting." Choose the correct word.', "opts": ["who", "whom", "which", "what"], "ans": 2, "cat": "Grammar", "diff": 4},
        {"q": '"She is old ___ to drive." Choose the correct word.', "opts": ["too", "so", "very", "enough"], "ans": 3, "cat": "Grammar", "diff": 4},
        {"q": '"He sent ___ a letter." (to her) Choose the correct pronoun.', "opts": ["she", "hers", "her", "herself"], "ans": 2, "cat": "Grammar", "diff": 4},
        {"q": '"There are ___ apples on the table." (a small number)', "opts": ["much", "a little", "a few", "lot"], "ans": 2, "cat": "Grammar", "diff": 4},

        # diff 5 — present perfect, active/passive intro, whose, neither/nor, pronoun cases I/me
        {"q": '"She ___ in this city for five years." (still lives there)', "opts": ["lives", "lived", "has lived", "is living"], "ans": 2, "cat": "Grammar", "diff": 5},
        {"q": 'Which sentence uses the passive voice?', "opts": ["The dog chased the cat.", "The cat was chased by the dog.", "The cat ran from the dog.", "The dog ran after the cat."], "ans": 1, "cat": "Grammar", "diff": 5},
        {"q": '"___ coat is this?" Choose the correct word.', "opts": ["Who", "Whom", "Whose", "Which"], "ans": 2, "cat": "Grammar", "diff": 5},
        {"q": 'Which is correct? (subject pronouns)', "opts": ["Me and my friend went.", "My friend and me went.", "My friend and I went.", "I and my friend went."], "ans": 2, "cat": "Grammar", "diff": 5},
        {"q": '"___ she ___ he was at home." Choose the correct words.', "opts": ["Either/or", "Neither/nor", "Both/and", "Not only/but"], "ans": 1, "cat": "Grammar", "diff": 5},
        {"q": '"I have ___ seen that movie." (already, use present perfect)', "opts": ["never", "already", "yet", "just"], "ans": 1, "cat": "Grammar", "diff": 5},
        {"q": 'Which sentence uses the passive correctly?', "opts": ["The cake eaten by me.", "The cake was eaten by me.", "The cake was eat by me.", "The cake is ate by me."], "ans": 1, "cat": "Grammar", "diff": 5},
        {"q": '"Have you ___ visited Japan?" Choose the correct word.', "opts": ["never", "ever", "yet", "already"], "ans": 1, "cat": "Grammar", "diff": 5},
        {"q": 'Which is correct? (object pronoun)', "opts": ["Give it to I.", "Give it to me.", "Give it to my.", "Give it to mine."], "ans": 1, "cat": "Grammar", "diff": 5},
        {"q": '"She has ___ finished her homework." (a short time ago)', "opts": ["just", "yet", "since", "for"], "ans": 0, "cat": "Grammar", "diff": 5},
        {"q": '"The letter was written ___ my teacher."', "opts": ["from", "with", "by", "to"], "ans": 2, "cat": "Grammar", "diff": 5},
        {"q": 'Which is correct? (neither…nor)', "opts": ["Neither she or he came.", "Neither she nor he came.", "Neither she nor he come.", "Neither she and nor he came."], "ans": 1, "cat": "Grammar", "diff": 5},
    ],

    # ── Grade 3 ──────────────────────────────────────────────────────────────
    3: [
        # diff 1 — identify all 8 parts of speech, possessive nouns, frequency adverbs, preposition phrases
        {"q": 'Which word is a preposition?', "opts": ["run", "under", "happy", "book"], "ans": 1, "cat": "Grammar", "diff": 1},
        {"q": 'Which word is a conjunction?', "opts": ["table", "although", "quickly", "blue"], "ans": 1, "cat": "Grammar", "diff": 1},
        {"q": 'Which word is an interjection?', "opts": ["run", "big", "Wow!", "slowly"], "ans": 2, "cat": "Grammar", "diff": 1},
        {"q": '"Sarah\'s book" shows what?', "opts": ["plural", "possession", "contraction", "verb tense"], "ans": 1, "cat": "Grammar", "diff": 1},
        {"q": '"She ___ brushes her teeth." Choose the correct frequency adverb.', "opts": ["never / always / sometimes / often — pick one", "always", "often", "sometimes"], "ans": 1, "cat": "Grammar", "diff": 1},
        {"q": 'Which shows correct use of a frequency adverb?', "opts": ["She always is late.", "She is always late.", "Always she is late.", "She is late always."], "ans": 1, "cat": "Grammar", "diff": 1},
        {"q": 'Which word is a pronoun?', "opts": ["table", "run", "it", "quickly"], "ans": 2, "cat": "Grammar", "diff": 1},
        {"q": 'Which word is an adverb?', "opts": ["beautiful", "beauty", "beautifully", "beautify"], "ans": 2, "cat": "Grammar", "diff": 1},
        {"q": '"The students\' desks" means the desks belong to…', "opts": ["one student", "many students", "no students", "the teacher"], "ans": 1, "cat": "Grammar", "diff": 1},
        {"q": 'Which shows the possessive of "James"?', "opts": ["James's book", "James' book", "James book", "Jamess book"], "ans": 0, "cat": "Grammar", "diff": 1},
        {"q": 'Which word is a conjunction?', "opts": ["under", "fast", "because", "happy"], "ans": 2, "cat": "Grammar", "diff": 1},
        {"q": '"We go to the park ___ Saturdays." Choose the correct preposition.', "opts": ["in", "at", "on", "by"], "ans": 2, "cat": "Grammar", "diff": 1},

        # diff 2 — comparatives/superlatives (irregular), some/any, compound subjects & verbs, subordinating conjunctions
        {"q": 'Which sentence uses "any" correctly?', "opts": ["I have any milk.", "Do you have any milk?", "Any I don't have milk.", "I don't have some milk."], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": 'Which is the comparative form of "little" (amount)?', "opts": ["littler", "less", "lesser", "more little"], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": 'Which is the superlative of "many"?', "opts": ["most", "more", "very many", "maniest"], "ans": 0, "cat": "Grammar", "diff": 2},
        {"q": '"Although it rained, we ___ outside." Choose the correct form.', "opts": ["play", "played", "were playing", "will play"], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": '"Both Tom ___ Ana like soccer." Choose the correct conjunction.', "opts": ["or", "nor", "and", "but"], "ans": 2, "cat": "Grammar", "diff": 2},
        {"q": '"She ___ I went to the market." Choose the correct pronoun.', "opts": ["her and", "me and", "and me", "and I"], "ans": 3, "cat": "Grammar", "diff": 2},
        {"q": 'Which uses "some" correctly?', "opts": ["Do you want some coffee?", "I don't want some coffee.", "Any she has coffee.", "Some I don't have coffee."], "ans": 0, "cat": "Grammar", "diff": 2},
        {"q": '"___ she studies hard, she passes." Choose the correct conjunction.', "opts": ["Although", "Because", "Whenever", "If"], "ans": 3, "cat": "Grammar", "diff": 2},
        {"q": '"Neither Tom nor Ana ___ here." Choose the correct verb.', "opts": ["are", "is", "were", "am"], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": '"She both sings ___ dances." Choose the correct conjunction.', "opts": ["or", "nor", "but", "and"], "ans": 3, "cat": "Grammar", "diff": 2},
        {"q": 'Which is the superlative of "little" (amount)?', "opts": ["least", "less", "fewer", "very little"], "ans": 0, "cat": "Grammar", "diff": 2},
        {"q": '"Since ___ started school, she has many friends."', "opts": ["she", "her", "hers", "herself"], "ans": 0, "cat": "Grammar", "diff": 2},

        # diff 3 — future "going to" vs "will", zero conditional, gerunds as subjects, pronoun-antecedent agreement
        {"q": '"___ to rain soon." (planned/predicted)', "opts": ["It will", "It is going", "It is going to", "It was going to"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": '"If you heat ice, it ___." (zero conditional)', "opts": ["melts", "will melt", "melted", "is melting"], "ans": 0, "cat": "Grammar", "diff": 3},
        {"q": '"___ is good exercise." (swim - use as a noun)', "opts": ["Swim", "Swims", "Swimming", "To swim is"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": '"Every student must bring ___ book." Choose the correct pronoun.', "opts": ["their", "his or her", "its", "our"], "ans": 1, "cat": "Grammar", "diff": 3},
        {"q": 'Which sentence uses "will" for a spontaneous decision?', "opts": ['I\'m going to call you later.', 'I will answer the door — it\'s ringing now!', "I'm visiting her next week.", "I have called her already."], "ans": 1, "cat": "Grammar", "diff": 3},
        {"q": '"If water reaches 100°C, it ___." (zero conditional)', "opts": ["boils", "will boil", "boiled", "is boiling"], "ans": 0, "cat": "Grammar", "diff": 3},
        {"q": '"___ is my favorite hobby." (read - use as a noun)', "opts": ["Read", "Reads", "To reading", "Reading"], "ans": 3, "cat": "Grammar", "diff": 3},
        {"q": '"The team won ___ match." Choose the correct pronoun.', "opts": ["their", "its", "his", "our"], "ans": 1, "cat": "Grammar", "diff": 3},
        {"q": '"She ___ visit Paris next year." (firm plan)', "opts": ["will", "is going to", "is going", "goes to"], "ans": 1, "cat": "Grammar", "diff": 3},
        {"q": '"If you mix red and blue, you ___ purple." (zero conditional)', "opts": ["get", "will get", "got", "getting"], "ans": 0, "cat": "Grammar", "diff": 3},
        {"q": '"___ is not always easy." (learn - use as a noun)', "opts": ["Learn", "Learns", "Learning", "Learned"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": '"The class finished ___ project." Choose the correct pronoun.', "opts": ["their", "its", "his", "her"], "ans": 0, "cat": "Grammar", "diff": 3},

        # diff 4 — passive voice formation, relative clauses who/which/that/where, reported speech statements, conjunctive adverbs
        {"q": 'Which sentence is in the passive voice?', "opts": ["She wrote the letter.", "The letter was written by her.", "She writes letters.", "She had written the letter."], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": '"The city ___ I was born is beautiful." Choose the correct word.', "opts": ["who", "which", "that", "where"], "ans": 3, "cat": "Grammar", "diff": 4},
        {"q": 'Change to reported speech: He said, "I am tired."', "opts": ['He said he am tired.', 'He said he is tired.', 'He said he was tired.', 'He said I was tired.'], "ans": 2, "cat": "Grammar", "diff": 4},
        {"q": '"However" is an example of a…', "opts": ["subordinating conjunction", "conjunctive adverb", "preposition", "relative pronoun"], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": '"The person ___ called is my teacher." Choose the correct word.', "opts": ["which", "where", "who", "what"], "ans": 2, "cat": "Grammar", "diff": 4},
        {"q": '"English is spoken ___ many countries." Choose the correct word.', "opts": ["from", "with", "by", "in"], "ans": 2, "cat": "Grammar", "diff": 4},
        {"q": 'Change to reported speech: She said, "I like pizza."', "opts": ['She said she like pizza.', 'She said she liked pizza.', 'She said she likes pizza.', 'She said I liked pizza.'], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": '"The book ___ I recommended is sold out." Choose the correct word.', "opts": ["who", "whom", "which", "where"], "ans": 2, "cat": "Grammar", "diff": 4},
        {"q": '"The windows ___ broken during the storm." (passive)', "opts": ["are", "were", "was", "has been"], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": '"I was late; ___, I apologized." Choose the correct conjunctive adverb.', "opts": ["but", "however", "although", "because"], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": '"The park ___ we play is nearby." Choose the correct word.', "opts": ["which", "who", "that", "where"], "ans": 3, "cat": "Grammar", "diff": 4},
        {"q": 'Change to reported speech: He said, "She is working."', "opts": ['He said she is working.', 'He said she was working.', 'He said she worked.', 'He said she has worked.'], "ans": 1, "cat": "Grammar", "diff": 4},

        # diff 5 — present perfect continuous, conditional type 1, participial phrases, appositive phrases
        {"q": '"She ___ for two hours." (still studying now, use present perfect continuous)', "opts": ["studies", "studied", "has studied", "has been studying"], "ans": 3, "cat": "Grammar", "diff": 5},
        {"q": '"If it rains, we ___ inside." (conditional type 1)', "opts": ["stay", "stayed", "will stay", "would stay"], "ans": 2, "cat": "Grammar", "diff": 5},
        {"q": '"___ the test, she felt relieved." (after finishing)', "opts": ["Finish", "Finished", "Having finished", "Finishing"], "ans": 2, "cat": "Grammar", "diff": 5},
        {"q": '"My sister, ___, is visiting us." Identify the appositive.', "opts": ["My sister", "a doctor", "is visiting", "us"], "ans": 1, "cat": "Grammar", "diff": 5},
        {"q": '"They ___ soccer for an hour." (still playing now)', "opts": ["play", "played", "have been playing", "have played"], "ans": 2, "cat": "Grammar", "diff": 5},
        {"q": '"If you study hard, you ___ pass the exam." (conditional type 1)', "opts": ["pass", "passed", "will pass", "would pass"], "ans": 2, "cat": "Grammar", "diff": 5},
        {"q": '"___ at the window, she waved hello." Which form is correct?', "opts": ["Stand", "Stood", "Standing", "Having stood"], "ans": 2, "cat": "Grammar", "diff": 5},
        {"q": '"Tokyo, ___, is a very large city." Identify the appositive.', "opts": ["Tokyo", "the capital of Japan", "is a very", "large city"], "ans": 1, "cat": "Grammar", "diff": 5},
        {"q": '"He ___ piano since he was five." (still plays now)', "opts": ["plays", "played", "has played", "has been playing"], "ans": 3, "cat": "Grammar", "diff": 5},
        {"q": '"If she ___ earlier, she won\'t be late." (conditional type 1)', "opts": ["leaves", "left", "will leave", "would leave"], "ans": 0, "cat": "Grammar", "diff": 5},
        {"q": '"___ in the rain, he caught a cold."', "opts": ["Walk", "Walked", "Walking", "To walk"], "ans": 2, "cat": "Grammar", "diff": 5},
        {"q": '"Mr. Lee, our teacher, ___ us grammar." Identify the appositive.', "opts": ["Mr. Lee", "our teacher", "teaches", "grammar"], "ans": 1, "cat": "Grammar", "diff": 5},
    ],

    # ── Grade 4 ──────────────────────────────────────────────────────────────
    4: [
        # diff 1 — complex sentences, subordinating conjunctions, direct/indirect speech statements
        {"q": 'Which is a complex sentence?', "opts": ["I like dogs.", "I like dogs and cats.", "Although it rained, we played outside.", "Dogs and cats are animals."], "ans": 2, "cat": "Grammar", "diff": 1},
        {"q": '"___ she was tired, she kept working." Choose the correct conjunction.', "opts": ["Because", "Since", "Although", "If"], "ans": 2, "cat": "Grammar", "diff": 1},
        {"q": 'Change to indirect speech: She said, "I will help you."', "opts": ['She said she will help me.', 'She said she would help me.', 'She said she helped me.', 'She told I would help you.'], "ans": 1, "cat": "Grammar", "diff": 1},
        {"q": '"___ he studied, he could not pass." Choose the correct conjunction.', "opts": ["Although", "Because", "Since", "While"], "ans": 0, "cat": "Grammar", "diff": 1},
        {"q": 'Which sentence has a dependent clause?', "opts": ["She ran fast.", "She ran, and she fell.", "Because she ran, she was tired.", "She ran fast every day."], "ans": 2, "cat": "Grammar", "diff": 1},
        {"q": 'Change to indirect speech: He said, "I am a student."', "opts": ['He said he am a student.', 'He said he is a student.', 'He said he was a student.', 'He said I was a student.'], "ans": 2, "cat": "Grammar", "diff": 1},
        {"q": '"___ you leave, please turn off the lights." Choose the conjunction.', "opts": ["Although", "Because", "Before", "While"], "ans": 2, "cat": "Grammar", "diff": 1},
        {"q": 'Which is the dependent clause? "I couldn\'t sleep because I was nervous."', "opts": ["I couldn't sleep", "because I was nervous", "I couldn't sleep because", "sleep because I was"], "ans": 1, "cat": "Grammar", "diff": 1},
        {"q": 'Change to indirect speech: She said, "I love chocolate."', "opts": ['She said she loves chocolate.', 'She said she loved chocolate.', 'She said I loved chocolate.', 'She said she love chocolate.'], "ans": 1, "cat": "Grammar", "diff": 1},
        {"q": '"___ she arrived late, she missed the start." Choose the conjunction.', "opts": ["Although", "Since", "While", "Because"], "ans": 3, "cat": "Grammar", "diff": 1},
        {"q": 'Which sentence is complex?', "opts": ["He sings and dances.", "He sings.", "He sings whenever he is happy.", "He sings; he also dances."], "ans": 2, "cat": "Grammar", "diff": 1},
        {"q": 'Change to indirect speech: He said, "I have finished."', "opts": ['He said he have finished.', 'He said he has finished.', 'He said he had finished.', 'He said I had finished.'], "ans": 2, "cat": "Grammar", "diff": 1},

        # diff 2 — conditional type 2, had better/would rather, parallel structure, pronoun cases
        {"q": '"If I ___ a bird, I would fly away." (conditional type 2)', "opts": ["am", "was", "were", "be"], "ans": 2, "cat": "Grammar", "diff": 2},
        {"q": 'Which sentence has parallel structure?', "opts": ["She likes singing, to dance, and bikes.", "She likes singing, dancing, and biking.", "She likes sing, dance, and bike.", "She likes to sing, run, and biking."], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": '"You ___ better see a doctor." Choose the correct modal.', "opts": ["would", "had", "should", "could"], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": '"To whom did you send the letter?" — what is "whom" here?', "opts": ["subject pronoun", "object pronoun", "possessive pronoun", "reflexive pronoun"], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": '"If she ___ more, she would be healthier." (conditional type 2)', "opts": ["exercises", "exercised", "will exercise", "had exercised"], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": 'Which sentence has parallel structure?', "opts": ["He is smart, kind, and working hard.", "He is smart, kind, and hardworking.", "He is smart, kindly, and hardworking.", "He is smart, kind, and works hard."], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": '"I would ___ stay home than go out."', "opts": ["better", "had", "rather", "prefer"], "ans": 2, "cat": "Grammar", "diff": 2},
        {"q": '"___ is calling?" vs "___ did you call?" Choose the correct pronouns.', "opts": ["Whom/Who", "Who/Whom", "Whom/Whom", "Who/Who"], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": '"If they ___ harder, they would win." (conditional type 2)', "opts": ["try", "tried", "will try", "had tried"], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": 'Which sentence uses parallel structure correctly?', "opts": ["She reads, writing, and codes.", "She reads, writes, and codes.", "She reads, to write, and coding.", "She reading, writing, coding."], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": '"You had better ___ late again." Choose the correct form.', "opts": ["not to be", "not be", "don't be", "aren't"], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": '"___ you give this to?" Choose the correct pronoun.', "opts": ["Who did", "Whom did", "Whose did", "Who are"], "ans": 1, "cat": "Grammar", "diff": 2},

        # diff 3 — adverbial clauses, non-defining relative clauses, indirect questions, used to/would for past habits
        {"q": '"My friend, ___ lives next door, is a doctor." (non-defining)', "opts": ["that", "which", "who", "where"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": 'Change to an indirect question: "Where does she live?"', "opts": ['I wonder where does she live.', 'I wonder where she lives.', 'I wonder where she live.', 'I wonder she lives where.'], "ans": 1, "cat": "Grammar", "diff": 3},
        {"q": '"I ___ walk to school when I was young." (past habit, no longer true)', "opts": ["used to", "would", "was used to", "both A and B"], "ans": 3, "cat": "Grammar", "diff": 3},
        {"q": '"Paris, ___ is the capital of France, is beautiful." (non-defining)', "opts": ["that", "which", "who", "where"], "ans": 1, "cat": "Grammar", "diff": 3},
        {"q": 'Change to an indirect question: "Is she coming?"', "opts": ['I want to know is she coming.', 'I want to know if she is coming.', 'I want to know if she coming.', 'I want to know she is coming.'], "ans": 1, "cat": "Grammar", "diff": 3},
        {"q": '"She ___ have long hair when she was a child." (past habit)', "opts": ["used to", "would", "was used to", "both A and B"], "ans": 3, "cat": "Grammar", "diff": 3},
        {"q": '"My car, ___ I bought last year, is very fast." (non-defining)', "opts": ["that", "which", "who", "whose"], "ans": 1, "cat": "Grammar", "diff": 3},
        {"q": 'Change to an indirect question: "What time does the train leave?"', "opts": ['I need to know what time does the train leave.', 'I need to know what time the train leaves.', 'I need to know what time the train leave.', 'I need to know the train leaves what time.'], "ans": 1, "cat": "Grammar", "diff": 3},
        {"q": '"He ___ play football every Saturday as a child." (past habit)', "opts": ["used to", "would", "both A and B", "was"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": '"The teacher, ___ class I enjoy, is very kind." Choose the correct word.', "opts": ["who", "which", "whose", "that"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": 'Change to indirect question: "Did he finish the report?"', "opts": ['I wonder did he finish the report.', 'I wonder whether he finished the report.', 'I wonder whether he finish the report.', 'I wonder he finished the report.'], "ans": 1, "cat": "Grammar", "diff": 3},
        {"q": '"They ___ live in Paris." (past habit, no longer true)', "opts": ["used to", "would", "both A and B", "are used to"], "ans": 0, "cat": "Grammar", "diff": 3},

        # diff 4 — reported speech (questions & commands), past perfect, despite/although, inversion for emphasis
        {"q": 'Report this question: She asked, "Where do you live?"', "opts": ['She asked where do I live.', 'She asked where I lived.', 'She asked where I live.', 'She asked where did I live.'], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": '"She had already ___ before he arrived." Choose the correct form.', "opts": ["eat", "ate", "eaten", "eating"], "ans": 2, "cat": "Grammar", "diff": 4},
        {"q": '"___ the rain, they continued hiking."', "opts": ["Although", "Despite", "Even though", "However"], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": 'Report this command: She said, "Please sit down."', "opts": ['She said please sit down.', 'She told me please sit down.', 'She asked me to sit down.', 'She said to sat down.'], "ans": 2, "cat": "Grammar", "diff": 4},
        {"q": '"By the time I arrived, she ___ left." Choose the correct form.', "opts": ["already left", "has already left", "had already left", "already leaves"], "ans": 2, "cat": "Grammar", "diff": 4},
        {"q": '"___ the traffic, we arrived on time."', "opts": ["Despite", "Although", "Even though", "However"], "ans": 0, "cat": "Grammar", "diff": 4},
        {"q": '"Never ___ I seen such a beautiful view!" (inversion)', "opts": ["did", "have", "do", "was"], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": 'Report this question: He asked, "Can you help me?"', "opts": ['He asked can you help me.', 'He asked if I can help him.', 'He asked if I could help him.', 'He asked me help him.'], "ans": 2, "cat": "Grammar", "diff": 4},
        {"q": '"They ___ not met before the party." (past perfect negative)', "opts": ["have", "had", "did", "were"], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": '"___ his illness, he performed brilliantly."', "opts": ["Although", "Despite", "Even though", "Because"], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": '"Not only ___ she smart, but she is also kind." (inversion)', "opts": ["she is", "is she", "was she", "she was"], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": 'Report this command: The teacher said, "Open your books."', "opts": ['The teacher said open your books.', 'The teacher told us to open our books.', 'The teacher said we open books.', 'The teacher asked open books.'], "ans": 1, "cat": "Grammar", "diff": 4},

        # diff 5 — mixed conditionals, ellipsis, cleft sentences, concession, advanced punctuation
        {"q": '"If she had studied, she ___ pass the test now." (mixed conditional)', "opts": ["would", "will", "would have", "had"], "ans": 0, "cat": "Grammar", "diff": 5},
        {"q": '"It is Ana ___ won the prize." (cleft sentence) Choose the correct word.', "opts": ["which", "that", "who", "what"], "ans": 2, "cat": "Grammar", "diff": 5},
        {"q": 'Which sentence uses a semicolon correctly?', "opts": ["She was tired; but she kept working.", "She was tired; she kept working.", "She was; tired she kept working.", "She was tired she; kept working."], "ans": 1, "cat": "Grammar", "diff": 5},
        {"q": '"If I were braver, I ___ traveled the world by now." (mixed conditional)', "opts": ["would", "will have", "would have", "had"], "ans": 2, "cat": "Grammar", "diff": 5},
        {"q": '"It was in Paris ___ they first met." (cleft sentence)', "opts": ["who", "that", "which", "where"], "ans": 1, "cat": "Grammar", "diff": 5},
        {"q": 'Which uses a colon correctly?', "opts": ["She needs: to rest.", "She needs three things: rest, food, and water.", "She: needs rest food and water.", "She needs rest: food and water."], "ans": 1, "cat": "Grammar", "diff": 5},
        {"q": '"She could have called, but she ___." (ellipsis — same verb)', "opts": ["could have", "didn't", "didn't called", "wouldn't have"], "ans": 0, "cat": "Grammar", "diff": 5},
        {"q": '"___ he works hard, he cannot seem to succeed." (concession)', "opts": ["Despite", "Although", "In spite", "However"], "ans": 1, "cat": "Grammar", "diff": 5},
        {"q": '"If he had slept more, he ___ better now." (mixed conditional)', "opts": ["feels", "will feel", "would feel", "would have felt"], "ans": 2, "cat": "Grammar", "diff": 5},
        {"q": '"It was the noise ___ woke me up." (cleft sentence)', "opts": ["who", "which", "that", "when"], "ans": 2, "cat": "Grammar", "diff": 5},
        {"q": 'Which correctly uses an em-dash?', "opts": ["She has one goal—to win.", "She has one—goal to win.", "She has—one goal to win.", "She has one goal to—win."], "ans": 0, "cat": "Grammar", "diff": 5},
        {"q": '"I could attend; she ___." (ellipsis — same verb)', "opts": ["couldn't attend", "couldn't", "can't", "doesn't attend"], "ans": 1, "cat": "Grammar", "diff": 5},
    ],

    # ── Grade 5 ──────────────────────────────────────────────────────────────
    5: [
        # diff 1 — present perfect vs simple past, modal perfects, gerunds vs infinitives (with meaning change)
        {"q": '"I ___ Japan three times." (experience up to now)', "opts": ["visited", "visit", "have visited", "had visited"], "ans": 2, "cat": "Grammar", "diff": 1},
        {"q": '"You should ___ told me earlier." Choose the correct modal perfect.', "opts": ["have", "has", "had", "be"], "ans": 0, "cat": "Grammar", "diff": 1},
        {"q": '"I remember ___ her at the party." (recall a memory)', "opts": ["to meet", "meet", "met", "meeting"], "ans": 3, "cat": "Grammar", "diff": 1},
        {"q": '"She ___ already finished the project." (use present perfect)', "opts": ["did", "does", "has", "had"], "ans": 2, "cat": "Grammar", "diff": 1},
        {"q": '"He could ___ won the race." Choose the correct modal perfect.', "opts": ["have", "has", "had", "be"], "ans": 0, "cat": "Grammar", "diff": 1},
        {"q": '"I stopped ___ coffee." (gave up the habit)', "opts": ["to drink", "drink", "drunk", "drinking"], "ans": 3, "cat": "Grammar", "diff": 1},
        {"q": '"When ___ you see that film?" (specific past time)', "opts": ["have", "did", "do", "had"], "ans": 1, "cat": "Grammar", "diff": 1},
        {"q": '"She must ___ made a mistake." Choose the correct modal perfect.', "opts": ["have", "has", "had", "been"], "ans": 0, "cat": "Grammar", "diff": 1},
        {"q": '"He tried ___ the door." (made an attempt)', "opts": ["opening", "open", "to open", "opened"], "ans": 2, "cat": "Grammar", "diff": 1},
        {"q": '"I ___ this book last year." (specific past time)', "opts": ["have read", "read", "has read", "had read"], "ans": 1, "cat": "Grammar", "diff": 1},
        {"q": '"They might ___ left already." Choose the correct form.', "opts": ["have", "has", "had", "be"], "ans": 0, "cat": "Grammar", "diff": 1},
        {"q": '"She forgot ___ the door." (didn\'t remember at the time)', "opts": ["locking", "lock", "locked", "to lock"], "ans": 3, "cat": "Grammar", "diff": 1},

        # diff 2 — future perfect, wish clauses, reported speech all types, relative clauses with prepositions
        {"q": '"By 2030, scientists ___ a cure." Choose the correct future perfect.', "opts": ["find", "will find", "will have found", "had found"], "ans": 2, "cat": "Grammar", "diff": 2},
        {"q": '"I wish I ___ more time." (present wish about present situation)', "opts": ["have", "had", "will have", "would have"], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": 'Report: He asked, "What time does the show start?"', "opts": ['He asked what time does the show start.', 'He asked what time the show started.', 'He asked what time the show starts.', 'He asked what the show time start.'], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": '"The company ___ I applied to is well known." Choose the correct form.', "opts": ["which I applied to", "to which I applied", "that I applied to", "both A and C"], "ans": 3, "cat": "Grammar", "diff": 2},
        {"q": '"By the time he arrives, we ___ finished." Choose the correct form.', "opts": ["will finish", "are finishing", "will have finished", "have finished"], "ans": 2, "cat": "Grammar", "diff": 2},
        {"q": '"I wish I ___ studied harder." (regret about the past)', "opts": ["have", "had", "would have", "could have"], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": 'Report: She told him, "Don\'t be late."', "opts": ['She told him don\'t be late.', 'She told him to not be late.', 'She told him not to be late.', 'She said him not be late.'], "ans": 2, "cat": "Grammar", "diff": 2},
        {"q": '"The professor ___ I spoke to is very experienced." (formal)', "opts": ["who I spoke to", "to whom I spoke", "which I spoke to", "that I spoke"], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": '"By next week, she ___ all her exams." Choose the correct form.', "opts": ["finishes", "will finish", "will have finished", "has finished"], "ans": 2, "cat": "Grammar", "diff": 2},
        {"q": '"I wish it ___ so cold." (present wish)', "opts": ["is not", "was not", "were not", "will not be"], "ans": 2, "cat": "Grammar", "diff": 2},
        {"q": 'Report: He said, "I can\'t swim."', "opts": ['He said he can\'t swim.', 'He said he couldn\'t swim.', 'He said he cannot swim.', 'He said I couldn\'t swim.'], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": '"The house ___ we grew up in is now a museum." Choose the correct form.', "opts": ["which we grew up in", "in which we grew up", "that we grew up in", "all of the above are correct"], "ans": 3, "cat": "Grammar", "diff": 2},

        # diff 3 — participle clauses, "the more…the more", emphasis with do/does/did, fronting for emphasis
        {"q": '"___ all her work, she went to sleep." (after completing)', "opts": ["Finishing", "Finished", "Having finished", "To finish"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": '"The more you practice, ___ you become." Choose the correct form.', "opts": ["the good", "the better", "the best", "the more better"], "ans": 1, "cat": "Grammar", "diff": 3},
        {"q": '"I ___ want to go, but I can\'t." (emphasis — present)', "opts": ["am doing", "do", "did", "have"], "ans": 1, "cat": "Grammar", "diff": 3},
        {"q": '"___ the window, he saw the accident." Choose the correct participle.', "opts": ["Look out of", "Looked out of", "Looking out of", "Having looked"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": '"The faster you eat, ___ it is for digestion." Choose the correct form.', "opts": ["the worse", "the worst", "the more worse", "more bad"], "ans": 0, "cat": "Grammar", "diff": 3},
        {"q": '"She ___ apologize, but no one listened." (emphasis — past)', "opts": ["does", "did", "has", "had"], "ans": 1, "cat": "Grammar", "diff": 3},
        {"q": '"On the table ___ the missing keys." (fronting for emphasis)', "opts": ["was", "were", "is", "are"], "ans": 0, "cat": "Grammar", "diff": 3},
        {"q": '"___ by the sunset, she stopped to take a photo." Choose the correct form.', "opts": ["Inspiring", "Inspired", "Having inspired", "To inspire"], "ans": 1, "cat": "Grammar", "diff": 3},
        {"q": '"The more sleep you get, ___ you feel." Choose the correct form.', "opts": ["the good", "the better", "the best", "the more good"], "ans": 1, "cat": "Grammar", "diff": 3},
        {"q": '"He ___ try his best, even if he fails." (emphasis — present)', "opts": ["is doing", "does", "did", "will"], "ans": 1, "cat": "Grammar", "diff": 3},
        {"q": '"Rarely ___ we see such talent." (fronting negative adverb)', "opts": ["we do", "do we", "we did", "did we"], "ans": 1, "cat": "Grammar", "diff": 3},
        {"q": '"___ in several films, she was now famous." Choose the correct form.', "opts": ["Appearing", "Appeared", "Having appeared", "To appear"], "ans": 2, "cat": "Grammar", "diff": 3},

        # diff 4 — determiners (few/little/several), mixed conditionals, nominalization for academic writing, discourse markers
        {"q": '"There are ___ students who failed." (a small number — countable)', "opts": ["little", "a little", "few", "a few"], "ans": 3, "cat": "Grammar", "diff": 4},
        {"q": '"If she ___ the medicine, she would be healthy now." (mixed conditional)', "opts": ["takes", "took", "had taken", "would take"], "ans": 2, "cat": "Grammar", "diff": 4},
        {"q": 'Which is the nominalized form of "decide"?', "opts": ["decidement", "decidation", "decision", "decidance"], "ans": 2, "cat": "Grammar", "diff": 4},
        {"q": '"There is ___ hope for improvement." (small amount — uncountable)', "opts": ["few", "a few", "little", "a little"], "ans": 3, "cat": "Grammar", "diff": 4},
        {"q": '"___ I can see, the results are positive." (discourse marker — from evidence)', "opts": ["As far as", "In spite of", "Nevertheless", "On the contrary"], "ans": 0, "cat": "Grammar", "diff": 4},
        {"q": '"If I ___ harder, I would be a better writer now." (mixed conditional)', "opts": ["practice", "practiced", "had practiced", "have practiced"], "ans": 2, "cat": "Grammar", "diff": 4},
        {"q": 'Which is the nominalized form of "argue"?', "opts": ["arguement", "argument", "arguition", "arguance"], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": '"___ students attended the event." (more than two but not many)', "opts": ["Little", "A little", "Few", "Several"], "ans": 3, "cat": "Grammar", "diff": 4},
        {"q": '"___, she refused to give up." (contrast with difficulty)', "opts": ["In addition", "Nevertheless", "As a result", "For instance"], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": '"If he ___ better advice, he wouldn\'t be in trouble now." (mixed conditional)', "opts": ["follows", "followed", "had followed", "has followed"], "ans": 2, "cat": "Grammar", "diff": 4},
        {"q": 'Which is the nominalized form of "solve"?', "opts": ["solvance", "solving", "solution", "solvation"], "ans": 2, "cat": "Grammar", "diff": 4},
        {"q": '"___ the challenges, the team succeeded." (discourse marker — contrast)', "opts": ["As a result of", "In spite of", "In addition to", "Thanks to"], "ans": 1, "cat": "Grammar", "diff": 4},

        # diff 5 — advanced modal verbs, abstract noun phrases, passive + reporting verbs, complex noun phrases, hedging
        {"q": '"It ___ be true — it seems impossible." (strong deduction — negative)', "opts": ["mustn't", "can't", "couldn't", "shouldn't"], "ans": 1, "cat": "Grammar", "diff": 5},
        {"q": '"It is believed ___ climate change is accelerating." Choose the correct form.', "opts": ["that", "which", "what", "how"], "ans": 0, "cat": "Grammar", "diff": 5},
        {"q": '"The ___ of the new law has caused debate." (abstract noun from "introduce")', "opts": ["introduction", "introducing", "introducal", "introduce"], "ans": 0, "cat": "Grammar", "diff": 5},
        {"q": '"This result ___ suggest a link between the two." (hedging — possibility)', "opts": ["definitely", "clearly", "may", "certainly"], "ans": 2, "cat": "Grammar", "diff": 5},
        {"q": '"It is reported ___ the economy is improving."', "opts": ["that", "which", "what", "how"], "ans": 0, "cat": "Grammar", "diff": 5},
        {"q": '"The ___ of the president surprised everyone." (abstract noun from "resign")', "opts": ["resignation", "resigning", "resignal", "resignment"], "ans": 0, "cat": "Grammar", "diff": 5},
        {"q": '"She ___ have forgotten — she never forgets anything." (strong deduction)', "opts": ["must", "can't", "should", "might"], "ans": 1, "cat": "Grammar", "diff": 5},
        {"q": '"The evidence ___ indicate that further research is needed." (hedging)', "opts": ["certainly", "appears to", "definitely proves", "clearly shows"], "ans": 1, "cat": "Grammar", "diff": 5},
        {"q": '"It has been shown ___ exercise improves mood."', "opts": ["that", "which", "what", "how"], "ans": 0, "cat": "Grammar", "diff": 5},
        {"q": '"The ___ of affordable housing is a major issue." (abstract noun from "lack")', "opts": ["lacking", "lacker", "lack", "lackness"], "ans": 2, "cat": "Grammar", "diff": 5},
        {"q": '"He ___ be at home — his car is there." (logical deduction — present)', "opts": ["should", "must", "will", "can"], "ans": 1, "cat": "Grammar", "diff": 5},
        {"q": '"The results ___ suggest a possible relationship." (hedging)', "opts": ["definitely", "might", "clearly prove", "certainly"], "ans": 1, "cat": "Grammar", "diff": 5},
    ],

    # ── Grade 6 ──────────────────────────────────────────────────────────────
    6: [
        # diff 1 — subjunctive mood, compound-complex sentences, advanced comma rules
        {"q": '"The doctor recommended that he ___ rest." (subjunctive)', "opts": ["rests", "rest", "rested", "is resting"], "ans": 1, "cat": "Grammar", "diff": 1},
        {"q": 'Which is a compound-complex sentence?', "opts": ["She studies hard.", "She studies hard, and she excels.", "Although she studies hard, she struggles, but she never gives up.", "She studies hard although she is tired."], "ans": 2, "cat": "Grammar", "diff": 1},
        {"q": '"It is essential that every student ___ on time." (subjunctive)', "opts": ["arrives", "arrive", "arrived", "is arriving"], "ans": 1, "cat": "Grammar", "diff": 1},
        {"q": 'Which sentence uses commas correctly with a non-defining clause?', "opts": ["The book that she wrote became famous.", "The book, that she wrote, became famous.", "The book, which she wrote, became famous.", "The book which, she wrote, became famous."], "ans": 2, "cat": "Grammar", "diff": 1},
        {"q": '"The committee insisted that the report ___ submitted by Friday." (subjunctive)', "opts": ["is", "be", "was", "has been"], "ans": 1, "cat": "Grammar", "diff": 1},
        {"q": 'Which correctly combines these: "She is tired. She works. She never complains."', "opts": ["Although she is tired and works hard, she never complains.", "She is tired she works she never complains.", "She is tired, she works hard, she never complains.", "She is tired but never complains and she works."], "ans": 0, "cat": "Grammar", "diff": 1},
        {"q": '"I suggest that she ___ the opportunity." (subjunctive)', "opts": ["takes", "take", "took", "is taking"], "ans": 1, "cat": "Grammar", "diff": 1},
        {"q": 'Identify the error in comma usage.', "opts": ["He studied hard, yet he failed.", "She is, however, very talented.", "After eating, she felt better.", "She is talented, and, smart."], "ans": 3, "cat": "Grammar", "diff": 1},
        {"q": '"The law requires that citizens ___ their taxes." (subjunctive)', "opts": ["pays", "pay", "paid", "are paying"], "ans": 1, "cat": "Grammar", "diff": 1},
        {"q": 'Which is correctly punctuated as a compound-complex sentence?', "opts": ["Although it was late, she finished her work, and she sent the email.", "Although it was late she finished her work and she sent the email.", "Although it was late, she finished her work and, she sent the email.", "Although it was late she finished her work, and she sent the email."], "ans": 0, "cat": "Grammar", "diff": 1},
        {"q": '"The principal demanded that all students ___ the rules." (subjunctive)', "opts": ["follows", "follow", "followed", "are following"], "ans": 1, "cat": "Grammar", "diff": 1},
        {"q": 'Which sentence correctly uses a comma with a conjunctive adverb?', "opts": ["She was sick however she came to work.", "She was sick; however, she came to work.", "She was sick, however she came to work.", "She was sick however, she came to work."], "ans": 1, "cat": "Grammar", "diff": 1},

        # diff 2 — colon and semicolon usage, em-dash, nominalization in academic writing
        {"q": 'Which correctly uses a colon?', "opts": ["She loves: cooking, reading, and hiking.", "She loves three things: cooking, reading, and hiking.", "She loves three: things cooking, reading, hiking.", "She: loves cooking reading and hiking."], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": 'Which is the nominalized form of "develop"?', "opts": ["developal", "developation", "development", "developing"], "ans": 2, "cat": "Grammar", "diff": 2},
        {"q": 'Which correctly uses a semicolon?', "opts": ["She loves reading; but she also likes hiking.", "She loves reading; she also likes hiking.", "She loves; reading she also likes hiking.", "She loves reading she; also likes hiking."], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": 'Which correctly uses an em-dash?', "opts": ["She had one fear—failure.", "She had—one fear failure.", "She had one—fear, failure.", "She had one fear—, failure."], "ans": 0, "cat": "Grammar", "diff": 2},
        {"q": 'Which is the nominalized form of "suggest"?', "opts": ["suggestal", "suggestion", "suggesting", "suggestance"], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": 'Which correctly uses a semicolon?', "opts": ["The results were good; however, more research is needed.", "The results were good; but more research is needed.", "The results were; good however more research is needed.", "The results; were good however more research is needed."], "ans": 0, "cat": "Grammar", "diff": 2},
        {"q": 'Which correctly uses an em-dash for added emphasis?', "opts": ["The solution—elegant and simple—impressed everyone.", "The solution—elegant and simple impressed everyone.", "The—solution elegant and simple—impressed everyone.", "The solution elegant—and simple—impressed everyone."], "ans": 0, "cat": "Grammar", "diff": 2},
        {"q": 'Which is the nominalized form of "analyze"?', "opts": ["analyzement", "analyzation", "analyzeance", "analysis"], "ans": 3, "cat": "Grammar", "diff": 2},
        {"q": 'Choose the correct colon usage in academic writing.', "opts": ["The study aims to: determine the effect.", "The study aims to determine the effect:", "The study found one key result: a significant decrease in emissions.", "The study: found a significant decrease."], "ans": 2, "cat": "Grammar", "diff": 2},
        {"q": 'Which correctly uses a semicolon in a list with internal commas?', "opts": ["Attendees came from Paris, France, Rome, Italy and Tokyo, Japan.", "Attendees came from Paris, France; Rome, Italy; and Tokyo, Japan.", "Attendees came from Paris, France; Rome, Italy, and Tokyo, Japan.", "Attendees came from Paris; France, Rome; Italy, Tokyo; Japan."], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": 'Which is the nominalized form of "implement"?', "opts": ["implemental", "implementation", "implementing", "implementance"], "ans": 1, "cat": "Grammar", "diff": 2},
        {"q": 'Which correctly uses an em-dash to indicate a sudden change?', "opts": ["She was about to speak—then she stopped.", "She was about—to speak then she stopped.", "She was—about to speak then stopped.", "She was about to speak then—she stopped."], "ans": 0, "cat": "Grammar", "diff": 2},

        # diff 3 — conditional type 3, "as if/as though" + subjunctive, inversion with negative adverbials
        {"q": '"If she had known, she ___ differently." (conditional type 3)', "opts": ["acted", "acts", "would have acted", "would act"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": '"He speaks as if he ___ the president." (unreal situation)', "opts": ["is", "was", "were", "be"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": '"Hardly ___ she arrived when the show began." (inversion with negative adverbial)', "opts": ["she had", "had she", "she did", "did she"], "ans": 1, "cat": "Grammar", "diff": 3},
        {"q": '"If they ___ earlier, the project would have succeeded." (conditional type 3)', "opts": ["start", "started", "had started", "would start"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": '"She looks as though she ___ seen a ghost." (just now — unreal)', "opts": ["sees", "saw", "had seen", "has seen"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": '"No sooner ___ the game started than it began to rain." (inversion)', "opts": ["the game had", "had the game", "the game did", "did the game"], "ans": 1, "cat": "Grammar", "diff": 3},
        {"q": '"If I ___ the lottery, I would have bought a house." (conditional type 3)', "opts": ["win", "won", "had won", "would win"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": '"He acts as if he ___ everything." (present unreal)', "opts": ["knows", "know", "knew", "had known"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": '"Not until she spoke ___ he understand." (inversion)', "opts": ["he did", "did he", "he does", "does he"], "ans": 1, "cat": "Grammar", "diff": 3},
        {"q": '"If you ___ told me, I could have helped." (conditional type 3)', "opts": ["tell", "told", "had told", "would tell"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": '"She cried as though her ___ broken." (as if — formal subjunctive)', "opts": ["heart was", "heart is", "heart were", "heart has been"], "ans": 2, "cat": "Grammar", "diff": 3},
        {"q": '"Seldom ___ we see such dedication." (inversion)', "opts": ["we have", "have we", "we do", "do we"], "ans": 1, "cat": "Grammar", "diff": 3},

        # diff 4 — complex passive, reporting verbs (It is alleged/believed/claimed), rhetorical questions
        {"q": '"The suspect ___ have committed the crime." (passive deduction)', "opts": ["is believed to", "believes to", "is believed that", "believed to"], "ans": 0, "cat": "Grammar", "diff": 4},
        {"q": 'Which is a rhetorical question?', "opts": ['"Do you know the answer?" (needing a reply)', '"Can anyone really know the future?" (no answer expected)', '"What time does it start?" (needing a reply)', '"Is the report ready?" (needing a reply)'], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": '"It is alleged ___ he lied to the committee."', "opts": ["that", "which", "what", "how"], "ans": 0, "cat": "Grammar", "diff": 4},
        {"q": '"___ having been there before, she navigated easily." Choose the correct form.', "opts": ["Despite", "Because of", "After", "Due to"], "ans": 0, "cat": "Grammar", "diff": 4},
        {"q": '"The data ___ show an increase in temperatures." (passive report)', "opts": ["is claimed to", "are claimed to", "is claimed that", "are claimed that"], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": 'What is the function of "Is this not what we all hope for?" in a speech?', "opts": ["to ask for information", "to provide evidence", "to persuade through rhetorical effect", "to state a counterargument"], "ans": 2, "cat": "Grammar", "diff": 4},
        {"q": '"It has been confirmed ___ the merger will proceed."', "opts": ["that", "which", "what", "whether"], "ans": 0, "cat": "Grammar", "diff": 4},
        {"q": '"She ___ to be the most qualified candidate." (passive report — present)', "opts": ["considers", "is considered", "considered", "was considered"], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": 'Which sentence correctly uses a complex passive?', "opts": ["He is said that he is brilliant.", "He is said to be brilliant.", "He said to be brilliant.", "It says he is brilliant."], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": '"___ having worked all night, he submitted the report." Choose the correct form.', "opts": ["Despite", "After", "Because of", "Although"], "ans": 1, "cat": "Grammar", "diff": 4},
        {"q": '"It is understood ___ further action is required."', "opts": ["that", "which", "what", "how"], "ans": 0, "cat": "Grammar", "diff": 4},
        {"q": '"She ___ to have arrived before midnight." (passive inference — past)', "opts": ["appears", "appeared", "is appeared", "appears to have"], "ans": 3, "cat": "Grammar", "diff": 4},

        # diff 5 — parallel structure in complex sentences, ellipsis in formal writing, advanced noun clauses, cohesive devices
        {"q": 'Which sentence has correct parallel structure in formal writing?', "opts": ["The goals are to improve efficiency, reducing cost, and the enhancement of quality.", "The goals are improving efficiency, to reduce cost, and to enhance quality.", "The goals are to improve efficiency, reduce cost, and enhance quality.", "The goals are efficiency improvement, cost reduction, and to enhance quality."], "ans": 2, "cat": "Grammar", "diff": 5},
        {"q": '"The fact ___ she lied changed everything." Choose the correct word.', "opts": ["which", "that", "what", "how"], "ans": 1, "cat": "Grammar", "diff": 5},
        {"q": 'Which cohesive device shows contrast?', "opts": ["Furthermore", "Consequently", "Nevertheless", "Similarly"], "ans": 2, "cat": "Grammar", "diff": 5},
        {"q": '"She could attend the meeting; her colleague ___." (formal ellipsis)', "opts": ["couldn't attend", "couldn't", "can't", "is not able to attend"], "ans": 1, "cat": "Grammar", "diff": 5},
        {"q": '"___ he succeeds or fails is irrelevant." Choose the correct noun clause starter.', "opts": ["That", "Whether", "What", "How"], "ans": 1, "cat": "Grammar", "diff": 5},
        {"q": 'Which cohesive device introduces an example?', "opts": ["However", "Moreover", "For instance", "Therefore"], "ans": 2, "cat": "Grammar", "diff": 5},
        {"q": 'Which sentence correctly uses ellipsis in formal writing?', "opts": ["Some students prefer lectures; others prefer seminars.", "Some students prefer lectures; others prefer to attend seminars.", "Some students prefer lectures; others preferring seminars.", "Some students prefer lectures; others like seminars."], "ans": 0, "cat": "Grammar", "diff": 5},
        {"q": '"___ she meant by that is unclear." Choose the correct noun clause starter.', "opts": ["That", "Whether", "What", "If"], "ans": 2, "cat": "Grammar", "diff": 5},
        {"q": 'Which cohesive device adds information?', "opts": ["On the other hand", "However", "In contrast", "Furthermore"], "ans": 3, "cat": "Grammar", "diff": 5},
        {"q": 'Which sentence has correct parallel structure?', "opts": ["She is known for her intelligence, her honesty, and being creative.", "She is known for her intelligence, her honesty, and her creativity.", "She is known for being intelligent, honesty, and her creativity.", "She is known for intelligence, being honest, and creativity."], "ans": 1, "cat": "Grammar", "diff": 5},
        {"q": '"___ the report was accurate surprised the committee." Choose the correct noun clause.', "opts": ["Whether", "What", "That", "How"], "ans": 0, "cat": "Grammar", "diff": 5},
        {"q": 'Which cohesive device signals a conclusion?', "opts": ["For example", "In addition", "To summarize", "On the contrary"], "ans": 2, "cat": "Grammar", "diff": 5},
    ],
}

# ─── Vocabulary question bank ─────────────────────────────────────────────────
VOCAB_QS = {

    # ── Grade 1 ──────────────────────────────────────────────────────────────
    1: [
        # diff 1 — colors, numbers, animals, school objects
        {"q": 'Which word is an animal?', "opts": ["run", "cat", "happy", "blue"], "ans": 1, "cat": "Vocabulary", "diff": 1},
        {"q": 'What color is the sky on a sunny day?', "opts": ["red", "green", "blue", "yellow"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": 'Which word is a number?', "opts": ["cat", "blue", "seven", "run"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": 'Which object do you use to write?', "opts": ["chair", "pencil", "window", "door"], "ans": 1, "cat": "Vocabulary", "diff": 1},
        {"q": 'What color is grass?', "opts": ["blue", "red", "yellow", "green"], "ans": 3, "cat": "Vocabulary", "diff": 1},
        {"q": 'Which word is a school object?', "opts": ["dog", "table", "fish", "bird"], "ans": 1, "cat": "Vocabulary", "diff": 1},
        {"q": 'Which animal can fly?', "opts": ["dog", "fish", "bird", "cat"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": 'What color is a banana?', "opts": ["red", "blue", "yellow", "green"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": 'Which object do you sit on?', "opts": ["book", "pencil", "chair", "window"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": 'Which animal lives in water?', "opts": ["cat", "dog", "fish", "bird"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": 'How many fingers are on one hand?', "opts": ["4", "5", "6", "10"], "ans": 1, "cat": "Vocabulary", "diff": 1},
        {"q": 'Which word is a color?', "opts": ["big", "run", "red", "cat"], "ans": 2, "cat": "Vocabulary", "diff": 1},

        # diff 2 — body parts, family members, feelings, basic opposites
        {"q": 'Which body part do you use to see?', "opts": ["ear", "nose", "mouth", "eye"], "ans": 3, "cat": "Vocabulary", "diff": 2},
        {"q": 'How do you feel when you smile?', "opts": ["sad", "happy", "angry", "tired"], "ans": 1, "cat": "Vocabulary", "diff": 2},
        {"q": 'What is the opposite of "big"?', "opts": ["huge", "tall", "small", "fast"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'Which word is a family member?', "opts": ["happy", "run", "mother", "blue"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'Which body part do you use to smell?', "opts": ["eye", "ear", "nose", "mouth"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'What is the opposite of "day"?', "opts": ["morning", "evening", "noon", "night"], "ans": 3, "cat": "Vocabulary", "diff": 2},
        {"q": 'Which body part do you use to hear?', "opts": ["eye", "nose", "hand", "ear"], "ans": 3, "cat": "Vocabulary", "diff": 2},
        {"q": 'How do you feel when something bad happens?', "opts": ["happy", "excited", "sad", "bored"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'What is the opposite of "hot"?', "opts": ["warm", "cool", "big", "cold"], "ans": 3, "cat": "Vocabulary", "diff": 2},
        {"q": 'Which word means "father or mother"?', "opts": ["teacher", "doctor", "parent", "friend"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'What is the opposite of "fast"?', "opts": ["quick", "big", "slow", "tall"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'How do you feel when you win a prize?', "opts": ["sad", "angry", "bored", "excited"], "ans": 3, "cat": "Vocabulary", "diff": 2},

        # diff 3 — simple synonyms/antonyms, word meanings in context
        {"q": 'What does "huge" mean?', "opts": ["very small", "very old", "very big", "very fast"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": 'Which word is a synonym for "happy"?', "opts": ["sad", "slow", "glad", "mad"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": 'What does "cold" mean?', "opts": ["very warm", "very loud", "not hot", "not quiet"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": 'Which word is an antonym of "begin"?', "opts": ["start", "go", "finish", "run"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": 'What does "gentle" mean?', "opts": ["very loud", "very fast", "soft and careful", "very angry"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": 'Which word is a synonym for "run"?', "opts": ["sleep", "sit", "jog", "walk"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": 'What does "brave" mean?', "opts": ["very afraid", "not afraid of danger", "very weak", "very slow"], "ans": 1, "cat": "Vocabulary", "diff": 3},
        {"q": 'Which word is an antonym of "clean"?', "opts": ["neat", "tidy", "new", "dirty"], "ans": 3, "cat": "Vocabulary", "diff": 3},
        {"q": 'What does "thirsty" mean?', "opts": ["needing food", "needing water", "needing sleep", "needing rest"], "ans": 1, "cat": "Vocabulary", "diff": 3},
        {"q": 'Which word is a synonym for "look"?', "opts": ["smell", "hear", "taste", "see"], "ans": 3, "cat": "Vocabulary", "diff": 3},
        {"q": 'What does "tiny" mean?', "opts": ["very big", "very loud", "very small", "very fast"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": 'Which word is an antonym of "quiet"?', "opts": ["calm", "soft", "noisy", "slow"], "ans": 2, "cat": "Vocabulary", "diff": 3},

        # diff 4 — more nuanced word meanings, context clues
        {"q": 'What does "curious" mean?', "opts": ["tired", "scared", "angry", "wanting to know more"], "ans": 3, "cat": "Vocabulary", "diff": 4},
        {"q": 'Which word means "to keep something safe"?', "opts": ["destroy", "ignore", "protect", "break"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": '"She was ___; she kept trying even after failing." Which word fits best?', "opts": ["lazy", "tired", "persistent", "bored"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does "predict" mean?', "opts": ["to remember the past", "to forget something", "to guess what will happen", "to know for sure"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": 'Which word means "not enough of something"?', "opts": ["plenty", "extra", "scarce", "full"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": '"The scientist made an important ___." Which word fits? (a finding)', "opts": ["mistake", "discovery", "dream", "journey"], "ans": 1, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does "communicate" mean?', "opts": ["to eat", "to sleep", "to play", "to share information"], "ans": 3, "cat": "Vocabulary", "diff": 4},
        {"q": 'Which word means "to move very fast"?', "opts": ["stroll", "creep", "walk", "dash"], "ans": 3, "cat": "Vocabulary", "diff": 4},
        {"q": '"The students worked ___." Which word shows they worked together?', "opts": ["alone", "cooperatively", "secretly", "carelessly"], "ans": 1, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does "similar" mean?', "opts": ["exactly the same", "completely different", "almost the same", "opposite"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": 'Which word means "to look at carefully"?', "opts": ["ignore", "sleep", "observe", "glance"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": '"The crowd was ___." Which word means very large?', "opts": ["tiny", "small", "enormous", "quiet"], "ans": 2, "cat": "Vocabulary", "diff": 4},

        # diff 5 — advanced word meanings for Grade 1 level
        {"q": 'What does "persevere" mean?', "opts": ["to give up", "to start something new", "to ask for help", "to keep trying even when it is hard"], "ans": 3, "cat": "Vocabulary", "diff": 5},
        {"q": 'Which word is a synonym for "frightened"?', "opts": ["brave", "calm", "safe", "terrified"], "ans": 3, "cat": "Vocabulary", "diff": 5},
        {"q": 'What does "independent" mean?', "opts": ["needing help from others", "very young", "very tired", "able to do things without help"], "ans": 3, "cat": "Vocabulary", "diff": 5},
        {"q": 'What does "ancient" mean?', "opts": ["very new", "very fast", "very big", "very old"], "ans": 3, "cat": "Vocabulary", "diff": 5},
        {"q": 'Which word means "to show how something is done"?', "opts": ["hide", "confuse", "forget", "demonstrate"], "ans": 3, "cat": "Vocabulary", "diff": 5},
        {"q": 'What does "patient" mean?', "opts": ["moving fast", "getting angry", "giving up", "able to wait calmly"], "ans": 3, "cat": "Vocabulary", "diff": 5},
        {"q": 'Which word is a synonym for "exhausted"?', "opts": ["energetic", "excited", "refreshed", "very tired"], "ans": 3, "cat": "Vocabulary", "diff": 5},
        {"q": 'What does "magnificent" mean?', "opts": ["very ugly", "very ordinary", "very small", "very impressive"], "ans": 3, "cat": "Vocabulary", "diff": 5},
        {"q": 'Which word means "to say something again"?', "opts": ["repeat", "forget", "ignore", "remember"], "ans": 0, "cat": "Vocabulary", "diff": 5},
        {"q": 'What does "sudden" mean?', "opts": ["slow", "gradual", "quiet", "happening very quickly without warning"], "ans": 3, "cat": "Vocabulary", "diff": 5},
        {"q": 'Which word is the opposite of "accept"?', "opts": ["take", "receive", "keep", "reject"], "ans": 3, "cat": "Vocabulary", "diff": 5},
        {"q": 'What does "cooperate" mean?', "opts": ["to argue", "to ignore others", "to work together", "to compete"], "ans": 2, "cat": "Vocabulary", "diff": 5},
    ],

    # ── Grade 2 ──────────────────────────────────────────────────────────────
    2: [
        # diff 1 — compound words, action words, community helpers
        {"q": 'Which is a compound word?', "opts": ["happy", "dog", "sunshine", "run"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": 'Which word describes what a teacher does?', "opts": ["teaches", "heals", "builds", "cooks"], "ans": 0, "cat": "Vocabulary", "diff": 1},
        {"q": 'What two words make "classroom"?', "opts": ["class + room", "clas + sroom", "cl + assroom", "clas + room"], "ans": 0, "cat": "Vocabulary", "diff": 1},
        {"q": 'Which word is a community helper?', "opts": ["dog", "chair", "doctor", "pencil"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": 'Which is a compound word?', "opts": ["pencil", "blue", "rainbow", "fast"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": 'Which person helps when you are sick?', "opts": ["farmer", "teacher", "driver", "doctor"], "ans": 3, "cat": "Vocabulary", "diff": 1},
        {"q": 'What two words make "football"?', "opts": ["foot + ball", "foo + tball", "f + ootball", "fo + otball"], "ans": 0, "cat": "Vocabulary", "diff": 1},
        {"q": 'Which person grows food for us?', "opts": ["doctor", "farmer", "driver", "teacher"], "ans": 1, "cat": "Vocabulary", "diff": 1},
        {"q": 'Which is a compound word?', "opts": ["happy", "school", "bedroom", "fast"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": 'Which person drives a bus or taxi?', "opts": ["farmer", "teacher", "driver", "doctor"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": 'What two words make "birthday"?', "opts": ["birth + day", "bir + thday", "bi + rthday", "birt + hday"], "ans": 0, "cat": "Vocabulary", "diff": 1},
        {"q": 'Which word tells what a firefighter does?', "opts": ["teaches", "heals", "fights fires", "grows food"], "ans": 2, "cat": "Vocabulary", "diff": 1},

        # diff 2 — synonyms/antonyms (simple), descriptive words, seasons
        {"q": 'Which word is a synonym for "begin"?', "opts": ["end", "stop", "start", "finish"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'What season comes after summer?', "opts": ["winter", "spring", "fall/autumn", "spring"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'Which word is an antonym of "near"?', "opts": ["close", "next to", "beside", "far"], "ans": 3, "cat": "Vocabulary", "diff": 2},
        {"q": 'Which word describes something that makes you laugh?', "opts": ["sad", "boring", "funny", "quiet"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'What season has flowers blooming and birds singing?', "opts": ["winter", "fall", "summer", "spring"], "ans": 3, "cat": "Vocabulary", "diff": 2},
        {"q": 'Which word is a synonym for "shout"?', "opts": ["whisper", "yell", "talk", "murmur"], "ans": 1, "cat": "Vocabulary", "diff": 2},
        {"q": 'What season is the coldest?', "opts": ["spring", "summer", "fall", "winter"], "ans": 3, "cat": "Vocabulary", "diff": 2},
        {"q": 'Which word is an antonym of "rough"?', "opts": ["bumpy", "hard", "smooth", "sharp"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'Which word describes very good food?', "opts": ["terrible", "tasteless", "delicious", "awful"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'What season is the hottest?', "opts": ["spring", "summer", "fall", "winter"], "ans": 1, "cat": "Vocabulary", "diff": 2},
        {"q": 'Which word is a synonym for "tired"?', "opts": ["energetic", "wide-awake", "excited", "exhausted"], "ans": 3, "cat": "Vocabulary", "diff": 2},
        {"q": 'Which word describes something that is not interesting?', "opts": ["exciting", "amazing", "boring", "wonderful"], "ans": 2, "cat": "Vocabulary", "diff": 2},

        # diff 3 — context clues, multiple-meaning words, simple figurative language
        {"q": '"The movie made me cry — it was so ___." Which word fits best?', "opts": ["funny", "boring", "moving", "loud"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": 'Which meaning of "bat" fits "He used a bat to hit the ball"?', "opts": ["a flying animal", "a sports tool", "a container", "a type of hat"], "ans": 1, "cat": "Vocabulary", "diff": 3},
        {"q": '"She has a great ___ of humor." Which word fits?', "opts": ["sense", "piece", "part", "bit"], "ans": 0, "cat": "Vocabulary", "diff": 3},
        {"q": 'Which meaning of "wave" fits "She waved goodbye"?', "opts": ["water movement", "a hand movement", "a hairstyle", "a radio signal"], "ans": 1, "cat": "Vocabulary", "diff": 3},
        {"q": '"The puppy is ___ — it keeps running around." Which word fits?', "opts": ["calm", "sleepy", "energetic", "quiet"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": 'Which meaning of "spring" fits "The spring water was cold"?', "opts": ["a season", "a metal coil", "a natural water source", "to jump"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": '"She gave a ___ performance." (very impressive)', "opts": ["poor", "dull", "boring", "brilliant"], "ans": 3, "cat": "Vocabulary", "diff": 3},
        {"q": 'Which meaning of "fly" fits "The pilot will fly the plane"?', "opts": ["an insect", "to move through air", "to escape quickly", "a zipper"], "ans": 1, "cat": "Vocabulary", "diff": 3},
        {"q": '"The new student felt ___ in the unfamiliar classroom." Which word fits?', "opts": ["confident", "excited", "nervous", "bored"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": 'Which meaning of "light" fits "Can you turn on the light?"', "opts": ["not heavy", "a source of brightness", "not dark in color", "gentle"], "ans": 1, "cat": "Vocabulary", "diff": 3},
        {"q": '"He finished in ___ place." (won the race)', "opts": ["last", "first", "middle", "fourth"], "ans": 1, "cat": "Vocabulary", "diff": 3},
        {"q": 'Which meaning of "bank" fits "She put money in the bank"?', "opts": ["a river edge", "a pile of clouds", "a slope", "a financial institution"], "ans": 3, "cat": "Vocabulary", "diff": 3},

        # diff 4 — prefixes un-/re-, word families, idioms (simple)
        {"q": 'What does the prefix "un-" mean in "unhappy"?', "opts": ["very", "again", "not", "before"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does "rewrite" mean?', "opts": ["to write for the first time", "to read again", "to write again", "to not write"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": '"It\'s raining cats and dogs." What does this idiom mean?', "opts": ["cats and dogs are falling", "it is raining very hard", "animals are outside", "it is a little rainy"], "ans": 1, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does "preview" mean? (pre- = before)', "opts": ["to view again", "to view before others", "to not view", "to view slowly"], "ans": 1, "cat": "Vocabulary", "diff": 4},
        {"q": 'Which word in the word family of "help" is an adjective?', "opts": ["help", "helps", "helper", "helpful"], "ans": 3, "cat": "Vocabulary", "diff": 4},
        {"q": '"Break a leg!" What does this idiom mean?', "opts": ["hurt yourself", "break something", "good luck", "stop running"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does "dislike" mean? (dis- = not)', "opts": ["to like very much", "to like again", "to not like", "to like slowly"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": 'Which word in the word family of "create" is a noun (a person)?', "opts": ["create", "creation", "creative", "creator"], "ans": 3, "cat": "Vocabulary", "diff": 4},
        {"q": '"Under the weather" means…', "opts": ["outside in the rain", "feeling ill", "standing below clouds", "feeling very happy"], "ans": 1, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does "redo" mean?', "opts": ["to not do", "to do slowly", "to do before", "to do again"], "ans": 3, "cat": "Vocabulary", "diff": 4},
        {"q": 'Which word in the word family of "danger" is an adjective?', "opts": ["danger", "endanger", "dangerously", "dangerous"], "ans": 3, "cat": "Vocabulary", "diff": 4},
        {"q": '"Hit the books" means…', "opts": ["throw books", "hurt a book", "study", "close books"], "ans": 2, "cat": "Vocabulary", "diff": 4},

        # diff 5 — suffixes -ful/-less/-tion/-ment, homophones, figurative language
        {"q": 'What does the suffix "-less" mean in "hopeless"?', "opts": ["full of", "the act of", "without", "one who"], "ans": 2, "cat": "Vocabulary", "diff": 5},
        {"q": 'Which pair are homophones?', "opts": ["big/large", "to/too", "cat/dog", "run/walk"], "ans": 1, "cat": "Vocabulary", "diff": 5},
        {"q": 'What does "-ful" mean in "joyful"?', "opts": ["without joy", "full of joy", "joy again", "not joy"], "ans": 1, "cat": "Vocabulary", "diff": 5},
        {"q": '"Her smile is sunshine." This is an example of a…', "opts": ["simile", "metaphor", "idiom", "definition"], "ans": 1, "cat": "Vocabulary", "diff": 5},
        {"q": 'Which pair are homophones?', "opts": ["see/sea", "big/huge", "fast/slow", "run/walk"], "ans": 0, "cat": "Vocabulary", "diff": 5},
        {"q": 'What does "-tion" mean in "celebration"?', "opts": ["one who celebrates", "without celebration", "the act or result of celebrating", "full of celebration"], "ans": 2, "cat": "Vocabulary", "diff": 5},
        {"q": '"As fast as lightning." This is an example of a…', "opts": ["metaphor", "idiom", "simile", "antonym"], "ans": 2, "cat": "Vocabulary", "diff": 5},
        {"q": 'Which pair are homophones?', "opts": ["flower/flour", "big/small", "run/jump", "cat/dog"], "ans": 0, "cat": "Vocabulary", "diff": 5},
        {"q": 'What does "-ment" mean in "excitement"?', "opts": ["one who excites", "without excitement", "the state or act of being excited", "full of excitement"], "ans": 2, "cat": "Vocabulary", "diff": 5},
        {"q": '"The wind sang through the trees." This is an example of…', "opts": ["simile", "metaphor", "personification", "idiom"], "ans": 2, "cat": "Vocabulary", "diff": 5},
        {"q": 'Which pair are homophones?', "opts": ["write/right", "big/large", "hot/cold", "fast/quick"], "ans": 0, "cat": "Vocabulary", "diff": 5},
        {"q": '"The classroom was a zoo." This is an example of a…', "opts": ["simile", "metaphor", "personification", "idiom"], "ans": 1, "cat": "Vocabulary", "diff": 5},
    ],

    # ── Grade 3 ──────────────────────────────────────────────────────────────
    3: [
        # diff 1 — prefixes (un-, re-, pre-, dis-), context clues
        {"q": 'What does the prefix "pre-" mean in "prehistoric"?', "opts": ["after", "again", "before", "not"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": 'What does "disagree" mean? (dis-)', "opts": ["to agree strongly", "to agree again", "to not agree", "to agree slowly"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": '"She was ___; she would not give up." (continuing despite difficulty)', "opts": ["lazy", "tired", "determined", "bored"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": 'What does "reconstruct" mean? (re- = again)', "opts": ["to build for the first time", "to not build", "to build again", "to destroy"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": '"The forest was ___ — no one had been there in years." (empty, abandoned)', "opts": ["crowded", "noisy", "abandoned", "busy"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": 'What does "preheat" mean? (pre- = before)', "opts": ["to heat again", "to not heat", "to heat after", "to heat before"], "ans": 3, "cat": "Vocabulary", "diff": 1},
        {"q": 'What does "disconnect" mean? (dis- = away/not)', "opts": ["to connect again", "to connect strongly", "to separate/cut off", "to connect slowly"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": '"She felt ___ after running the marathon." (very tired)', "opts": ["energetic", "excited", "exhausted", "calm"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": 'What does "uncertain" mean? (un-)', "opts": ["very certain", "certain again", "not certain", "certainly before"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": 'What does "prepay" mean? (pre- = before)', "opts": ["to not pay", "to pay again", "to pay late", "to pay before"], "ans": 3, "cat": "Vocabulary", "diff": 1},
        {"q": '"The explorer made a remarkable ___." (a new finding)', "opts": ["mistake", "dream", "discovery", "journey"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": 'What does "disappear" mean? (dis- = away)', "opts": ["to appear again", "to appear slowly", "to appear clearly", "to go away or stop being seen"], "ans": 3, "cat": "Vocabulary", "diff": 1},

        # diff 2 — suffixes (-ful, -less, -tion, -er), homophones, multiple meanings
        {"q": 'What does the suffix "-er" mean in "teacher"?', "opts": ["without", "full of", "the act of", "one who does"], "ans": 3, "cat": "Vocabulary", "diff": 2},
        {"q": 'Which pair are homophones?', "opts": ["their/there", "big/large", "cat/dog", "fast/slow"], "ans": 0, "cat": "Vocabulary", "diff": 2},
        {"q": 'What does "careless" mean? (suffix -less)', "opts": ["very careful", "full of care", "without care", "care before"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'Which meaning of "cross" fits "She was cross with him"?', "opts": ["to go across a road", "angry", "a plus sign", "to mix two things"], "ans": 1, "cat": "Vocabulary", "diff": 2},
        {"q": 'What does "-ness" mean in "kindness"?', "opts": ["-ful", "-less", "the state or quality of", "-tion"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'Which pair are homophones?', "opts": ["bare/bear", "big/huge", "hot/cold", "fast/quick"], "ans": 0, "cat": "Vocabulary", "diff": 2},
        {"q": 'What does "cheerful" mean? (suffix -ful)', "opts": ["without cheer", "the act of cheering", "full of cheer and happiness", "one who cheers"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'Which meaning of "fair" fits "The weather is fair today"?', "opts": ["a carnival", "just and equal", "pleasant/clear", "light in color"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'What does "-tion" indicate in "education"?', "opts": ["one who educates", "without education", "the act of educating", "before education"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'Which pair are homophones?', "opts": ["knight/night", "big/small", "run/jump", "hot/warm"], "ans": 0, "cat": "Vocabulary", "diff": 2},
        {"q": 'What does "powerless" mean? (suffix -less)', "opts": ["very powerful", "full of power", "one with power", "without power"], "ans": 3, "cat": "Vocabulary", "diff": 2},
        {"q": 'Which meaning of "fall" fits "Leaves fall in autumn"?', "opts": ["a season", "to drop downward", "to fail", "a waterfall"], "ans": 1, "cat": "Vocabulary", "diff": 2},

        # diff 3 — context clues (harder), figurative language (simile, metaphor, idiom, hyperbole)
        {"q": '"The soldier showed enormous ___ in battle." (bravery)', "opts": ["cowardice", "laziness", "courage", "weakness"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": '"As quiet as a mouse." This is a…', "opts": ["metaphor", "simile", "idiom", "hyperbole"], "ans": 1, "cat": "Vocabulary", "diff": 3},
        {"q": '"He was over the moon." This idiom means he was…', "opts": ["sad", "confused", "afraid", "very happy"], "ans": 3, "cat": "Vocabulary", "diff": 3},
        {"q": '"The scientist gathered ___ to prove her theory." (facts/information)', "opts": ["stories", "opinions", "evidence", "feelings"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": '"The city is a jungle." This is a…', "opts": ["simile", "metaphor", "idiom", "hyperbole"], "ans": 1, "cat": "Vocabulary", "diff": 3},
        {"q": '"She bit off more than she could chew." This means…', "opts": ["she ate too fast", "she took on more than she could handle", "she chewed slowly", "she was hungry"], "ans": 1, "cat": "Vocabulary", "diff": 3},
        {"q": '"The announcement was ___." (told to everyone publicly)', "opts": ["secret", "private", "public", "hidden"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": '"I have told you a million times!" This is an example of…', "opts": ["simile", "metaphor", "idiom", "hyperbole"], "ans": 3, "cat": "Vocabulary", "diff": 3},
        {"q": '"He was so hungry he could eat a horse." This is…', "opts": ["simile", "metaphor", "personification", "hyperbole"], "ans": 3, "cat": "Vocabulary", "diff": 3},
        {"q": '"The results were ___." (the expected outcome happened)', "opts": ["surprising", "unexpected", "predictable", "shocking"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": '"The stars winked at me." This is an example of…', "opts": ["simile", "metaphor", "personification", "hyperbole"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": '"The volcano erupted with ___." (great force and anger)', "opts": ["silence", "gentleness", "fury", "calmness"], "ans": 2, "cat": "Vocabulary", "diff": 3},

        # diff 4 — Greek/Latin roots (bio-, geo-, -ology, -graph), academic vocabulary
        {"q": 'What does the root "bio-" mean in "biology"?', "opts": ["earth", "water", "life", "star"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does "geography" study? (geo- = earth, -graph = record)', "opts": ["life on Earth", "space and stars", "Earth\'s features and regions", "the history of people"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does the root "-ology" mean?', "opts": ["the study of", "the writing of", "the feeling of", "the history of"], "ans": 0, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does "telescope" help you do? (tele- = far)', "opts": ["see things up close", "hear from far away", "see things far away", "measure temperature"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does "aquatic" relate to? (aqua- = water)', "opts": ["fire", "land", "air", "water"], "ans": 3, "cat": "Vocabulary", "diff": 4},
        {"q": '"Psychology" is the study of what? (psycho- = mind)', "opts": ["the body", "the earth", "the mind and behavior", "living things"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does "thermometer" measure? (therm- = heat)', "opts": ["weight", "distance", "time", "temperature"], "ans": 3, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does "microscope" help you see? (micro- = small)', "opts": ["things very far away", "things very small", "things in the dark", "things underwater"], "ans": 1, "cat": "Vocabulary", "diff": 4},
        {"q": '"Geology" is the study of what? (geo- = earth)', "opts": ["stars", "life", "Earth\'s rocks and layers", "the ocean"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does "transport" mean? (trans- = across)', "opts": ["to stay in place", "to carry across from one place to another", "to destroy", "to build"], "ans": 1, "cat": "Vocabulary", "diff": 4},
        {"q": '"Autobiography" means a person writes about…', "opts": ["someone else\'s life", "cars", "their own life", "nature"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does the root "graph" mean?', "opts": ["life", "earth", "to write or record", "study"], "ans": 2, "cat": "Vocabulary", "diff": 4},

        # diff 5 — connotation, analogies, alliteration, advanced context clues
        {"q": '"Slender" and "skinny" both mean thin. Which has a more positive connotation?', "opts": ["skinny", "slender", "both are equal", "neither is positive"], "ans": 1, "cat": "Vocabulary", "diff": 5},
        {"q": '"Puppy is to dog as kitten is to ___." Complete the analogy.', "opts": ["cat", "fish", "bird", "horse"], "ans": 0, "cat": "Vocabulary", "diff": 5},
        {"q": '"Brave" and "reckless" both suggest action despite risk. Which is more positive?', "opts": ["reckless", "brave", "both are equal", "neither"], "ans": 1, "cat": "Vocabulary", "diff": 5},
        {"q": '"Peter Piper picked a peck of pickled peppers." This is an example of…', "opts": ["metaphor", "simile", "alliteration", "hyperbole"], "ans": 2, "cat": "Vocabulary", "diff": 5},
        {"q": '"Hot is to cold as light is to ___." Complete the analogy.', "opts": ["fire", "lamp", "bright", "dark"], "ans": 3, "cat": "Vocabulary", "diff": 5},
        {"q": '"Determined" and "stubborn" — which has a negative connotation?', "opts": ["determined", "stubborn", "both are equal", "neither"], "ans": 1, "cat": "Vocabulary", "diff": 5},
        {"q": '"Sally sells seashells by the seashore." This is…', "opts": ["personification", "simile", "hyperbole", "alliteration"], "ans": 3, "cat": "Vocabulary", "diff": 5},
        {"q": '"Book is to library as painting is to ___." Complete the analogy.', "opts": ["school", "museum", "store", "garden"], "ans": 1, "cat": "Vocabulary", "diff": 5},
        {"q": '"Cheap" and "affordable" both mean low cost. Which is more positive?', "opts": ["cheap", "affordable", "both are equal", "neither"], "ans": 1, "cat": "Vocabulary", "diff": 5},
        {"q": '"Chef is to kitchen as scientist is to ___." Complete the analogy.', "opts": ["school", "office", "hospital", "laboratory"], "ans": 3, "cat": "Vocabulary", "diff": 5},
        {"q": '"Curious and creative, Clara caught colorful creatures." This uses…', "opts": ["personification", "metaphor", "alliteration", "hyperbole"], "ans": 2, "cat": "Vocabulary", "diff": 5},
        {"q": '"Assertive" vs "aggressive" — which describes a positive communication style?', "opts": ["aggressive", "assertive", "both are positive", "neither"], "ans": 1, "cat": "Vocabulary", "diff": 5},
    ],

    # ── Grade 4 ──────────────────────────────────────────────────────────────
    4: [
        # diff 1 — similes, metaphors, idioms
        {"q": '"As brave as a lion." This is a…', "opts": ["metaphor", "simile", "idiom", "hyperbole"], "ans": 1, "cat": "Vocabulary", "diff": 1},
        {"q": '"She has a heart of gold." This is a…', "opts": ["simile", "metaphor", "idiom", "hyperbole"], "ans": 1, "cat": "Vocabulary", "diff": 1},
        {"q": '"It\'s a piece of cake." This idiom means…', "opts": ["it tastes good", "it is very easy", "it costs a lot", "it is very hard"], "ans": 1, "cat": "Vocabulary", "diff": 1},
        {"q": '"The classroom was as noisy as a market." This is a…', "opts": ["metaphor", "idiom", "simile", "hyperbole"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": '"Time is money." This is a…', "opts": ["simile", "idiom", "metaphor", "alliteration"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": '"Spill the beans." This idiom means…', "opts": ["drop your food", "share a secret", "cook food", "make a mess"], "ans": 1, "cat": "Vocabulary", "diff": 1},
        {"q": '"Her laughter was music to his ears." This is a…', "opts": ["simile", "idiom", "hyperbole", "metaphor"], "ans": 3, "cat": "Vocabulary", "diff": 1},
        {"q": '"Life is a rollercoaster." This is a…', "opts": ["simile", "metaphor", "idiom", "personification"], "ans": 1, "cat": "Vocabulary", "diff": 1},
        {"q": '"Once in a blue moon." This idiom means…', "opts": ["on a cold night", "very frequently", "very rarely", "during a lunar eclipse"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": '"He runs like the wind." This is a…', "opts": ["metaphor", "simile", "idiom", "personification"], "ans": 1, "cat": "Vocabulary", "diff": 1},
        {"q": '"The world is a stage." This is a…', "opts": ["simile", "metaphor", "idiom", "alliteration"], "ans": 1, "cat": "Vocabulary", "diff": 1},
        {"q": '"Let the cat out of the bag." This idiom means…', "opts": ["release an animal", "make a mess", "reveal a secret", "lose something"], "ans": 2, "cat": "Vocabulary", "diff": 1},

        # diff 2 — Greek/Latin roots (harder), academic vocabulary level 1
        {"q": 'What does "chronological" relate to? (chrono- = time)', "opts": ["place", "size", "time", "color"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'What does "analyze" mean in academic writing?', "opts": ["to describe", "to list", "to examine in detail", "to summarize"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'What does "contradict" mean? (contra- = against)', "opts": ["to agree with", "to say the opposite of", "to repeat", "to explain"], "ans": 1, "cat": "Vocabulary", "diff": 2},
        {"q": '"Hypothesis" in science means…', "opts": ["a proven fact", "a final conclusion", "a testable prediction or educated guess", "experimental data"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'What does "multilingual" mean? (multi- = many)', "opts": ["speaking one language", "speaking two languages", "speaking many languages", "not speaking any language"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'What does "evaluate" mean in academic writing?', "opts": ["to list facts", "to describe", "to judge the value or quality of", "to copy"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'What does "portable" mean? (port- = carry)', "opts": ["expensive", "heavy and large", "easy to carry", "fixed in place"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": '"Evidence" in an argument means…', "opts": ["an opinion", "a guess", "a feeling", "facts that support a claim"], "ans": 3, "cat": "Vocabulary", "diff": 2},
        {"q": 'What does "invisible" mean? (in- = not, vis- = see)', "opts": ["very visible", "hard to see", "cannot be seen", "colorful"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'What does "conclude" mean in academic writing?', "opts": ["to begin", "to describe", "to list", "to reach a final decision or judgment"], "ans": 3, "cat": "Vocabulary", "diff": 2},
        {"q": 'What does "aqueduct" carry? (aqua- = water)', "opts": ["electricity", "gas", "water", "people"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": '"Significant" means…', "opts": ["very small", "unimportant", "very common", "important and meaningful"], "ans": 3, "cat": "Vocabulary", "diff": 2},

        # diff 3 — connotation/denotation, analogies, morphology
        {"q": '"Stubborn" and "determined" are similar. Which has a negative connotation?', "opts": ["determined", "stubborn", "both are negative", "neither"], "ans": 1, "cat": "Vocabulary", "diff": 3},
        {"q": '"Pen is to write as scissors is to ___." Complete the analogy.', "opts": ["paint", "cut", "draw", "erase"], "ans": 1, "cat": "Vocabulary", "diff": 3},
        {"q": 'The root "dict" (as in "dictate") means…', "opts": ["to see", "to say or speak", "to write", "to hear"], "ans": 1, "cat": "Vocabulary", "diff": 3},
        {"q": '"Economical" and "cheap" both mean low cost. Which sounds more positive?', "opts": ["cheap", "economical", "both are equal", "neither"], "ans": 1, "cat": "Vocabulary", "diff": 3},
        {"q": '"Doctor is to hospital as teacher is to ___." Complete the analogy.', "opts": ["library", "office", "school", "market"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": 'The root "scrib/script" (as in "scribe") means…', "opts": ["to see", "to hear", "to write", "to walk"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": '"Thin" vs "slender" — which has a more positive connotation?', "opts": ["thin", "slender", "both equal", "neither positive"], "ans": 1, "cat": "Vocabulary", "diff": 3},
        {"q": '"Hand is to glove as foot is to ___." Complete the analogy.', "opts": ["sock", "shoe", "boot", "sandal"], "ans": 0, "cat": "Vocabulary", "diff": 3},
        {"q": 'The root "aud" (as in "audience") means…', "opts": ["to write", "to see", "to hear", "to speak"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": '"Nosy" and "curious" both mean interested in others. Which is negative?', "opts": ["curious", "nosy", "both are negative", "neither"], "ans": 1, "cat": "Vocabulary", "diff": 3},
        {"q": '"Director is to film as author is to ___." Complete the analogy.', "opts": ["music", "painting", "book", "play"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": 'The root "vis/vid" (as in "vision") means…', "opts": ["to hear", "to write", "to walk", "to see"], "ans": 3, "cat": "Vocabulary", "diff": 3},

        # diff 4 — advanced figurative language, nuance, morphology
        {"q": '"The thunder roared its anger." This is an example of…', "opts": ["simile", "metaphor", "hyperbole", "personification"], "ans": 3, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does "plausible" mean?', "opts": ["impossible", "certain to happen", "able to be believed or possible", "completely false"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": '"I\'ve told you a billion times." This is an example of…', "opts": ["simile", "metaphor", "hyperbole", "personification"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does the suffix "-ize" mean in "modernize"?', "opts": ["the state of", "one who", "to make or become", "without"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does "ambiguous" mean?', "opts": ["very clear", "having one clear meaning", "having more than one possible meaning", "impossible to understand"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": '"Justice is blind." This is a…', "opts": ["simile", "idiom", "personification", "metaphor"], "ans": 3, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does "innovative" mean?', "opts": ["old-fashioned", "introducing new ideas or methods", "common and usual", "slow and careful"], "ans": 1, "cat": "Vocabulary", "diff": 4},
        {"q": '"Frugal" and "miserly" both relate to spending little money. Which is negative?', "opts": ["frugal", "miserly", "both are negative", "neither"], "ans": 1, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does the prefix "counter-" mean in "counterargument"?', "opts": ["for", "with", "before", "against"], "ans": 3, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does "meticulous" mean?', "opts": ["careless", "very careful about small details", "very fast", "very creative"], "ans": 1, "cat": "Vocabulary", "diff": 4},
        {"q": '"Confident" vs "arrogant" — which is positive?', "opts": ["arrogant", "confident", "both are positive", "neither"], "ans": 1, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does "collaborate" mean?', "opts": ["to compete", "to ignore others", "to work together toward a shared goal", "to work alone"], "ans": 2, "cat": "Vocabulary", "diff": 4},

        # diff 5 — etymology, advanced analogies, rhetorical devices
        {"q": 'The word "telephone" comes from Greek "tele" (far) + "phone" (sound). What does it do?', "opts": ["sends images far", "transmits sound over long distances", "measures temperature", "records writing"], "ans": 1, "cat": "Vocabulary", "diff": 5},
        {"q": '"Justice is to law as medicine is to ___." Complete the analogy.', "opts": ["school", "science", "health", "art"], "ans": 2, "cat": "Vocabulary", "diff": 5},
        {"q": 'Which word has a Latin root meaning "to carry"?', "opts": ["biology", "chronology", "transport", "spectacle"], "ans": 2, "cat": "Vocabulary", "diff": 5},
        {"q": 'What is "antithesis" in writing?', "opts": ["a synonym for metaphor", "placing opposite ideas side by side for contrast", "a type of rhyme", "a repeated idea"], "ans": 1, "cat": "Vocabulary", "diff": 5},
        {"q": '"Poverty is to wealth as ignorance is to ___." Complete the analogy.', "opts": ["school", "wisdom", "happiness", "money"], "ans": 1, "cat": "Vocabulary", "diff": 5},
        {"q": 'The Latin root "rupt" (as in "erupt") means…', "opts": ["to flow", "to grow", "to break or burst", "to shine"], "ans": 2, "cat": "Vocabulary", "diff": 5},
        {"q": '"Ask not what your country can do for you; ask what you can do for your country." This is an example of…', "opts": ["simile", "personification", "hyperbole", "antithesis"], "ans": 3, "cat": "Vocabulary", "diff": 5},
        {"q": 'The Greek root "aster/astro" (as in "astronomy") means…', "opts": ["water", "star", "earth", "life"], "ans": 1, "cat": "Vocabulary", "diff": 5},
        {"q": '"Author is to novel as composer is to ___." Complete the analogy.', "opts": ["painting", "sculpture", "poem", "symphony"], "ans": 3, "cat": "Vocabulary", "diff": 5},
        {"q": 'Which word has a Greek root meaning "to write"?', "opts": ["biology", "auditorium", "calligraphy", "geography"], "ans": 2, "cat": "Vocabulary", "diff": 5},
        {"q": '"Courage is not the absence of fear; it is action in spite of fear." This uses…', "opts": ["simile", "hyperbole", "antithesis", "alliteration"], "ans": 2, "cat": "Vocabulary", "diff": 5},
        {"q": 'The Latin root "bene" (as in "benefit") means…', "opts": ["bad", "small", "far", "good/well"], "ans": 3, "cat": "Vocabulary", "diff": 5},
    ],

    # ── Grade 5 ──────────────────────────────────────────────────────────────
    5: [
        # diff 1 — connotation/denotation, advanced figurative language
        {"q": '"Childish" and "childlike" both relate to children. Which has a negative connotation?', "opts": ["childlike", "childish", "both are negative", "neither"], "ans": 1, "cat": "Vocabulary", "diff": 1},
        {"q": '"The whole world watched." This is an example of…', "opts": ["simile", "metaphor", "personification", "hyperbole"], "ans": 3, "cat": "Vocabulary", "diff": 1},
        {"q": '"Inquisitive" and "nosy" both mean curious. Which is more positive?', "opts": ["nosy", "inquisitive", "both are positive", "neither"], "ans": 1, "cat": "Vocabulary", "diff": 1},
        {"q": '"The ocean sang a lullaby." This is an example of…', "opts": ["simile", "metaphor", "personification", "hyperbole"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": '"Eccentric" and "weird" both mean unusual. Which is more neutral or positive?', "opts": ["weird", "eccentric", "both are equal", "neither"], "ans": 1, "cat": "Vocabulary", "diff": 1},
        {"q": '"The news hit her like a brick wall." This is a…', "opts": ["metaphor", "simile", "personification", "hyperbole"], "ans": 1, "cat": "Vocabulary", "diff": 1},
        {"q": '"Slender" vs "scrawny" — both mean thin. Which is negative?', "opts": ["slender", "scrawny", "both are equal", "neither"], "ans": 1, "cat": "Vocabulary", "diff": 1},
        {"q": '"The flowers danced in the breeze." This is…', "opts": ["simile", "metaphor", "personification", "hyperbole"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": '"Thrifty" and "stingy" both mean saving money. Which is positive?', "opts": ["stingy", "thrifty", "both are positive", "neither"], "ans": 1, "cat": "Vocabulary", "diff": 1},
        {"q": '"She carried the weight of the world on her shoulders." This is a…', "opts": ["simile", "metaphor", "personification", "alliteration"], "ans": 1, "cat": "Vocabulary", "diff": 1},
        {"q": '"Youthful" and "immature" both relate to youth. Which is negative?', "opts": ["youthful", "immature", "both are equal", "neither"], "ans": 1, "cat": "Vocabulary", "diff": 1},
        {"q": '"I\'m so hungry I could eat a horse." This is an example of…', "opts": ["simile", "metaphor", "personification", "hyperbole"], "ans": 3, "cat": "Vocabulary", "diff": 1},

        # diff 2 — analogies, morphology (harder), advanced prefixes/suffixes
        {"q": '"Frequent is to infrequent as possible is to ___." Complete the analogy.', "opts": ["likely", "impossible", "maybe", "probable"], "ans": 1, "cat": "Vocabulary", "diff": 2},
        {"q": 'The suffix "-ous" (as in "courageous") means…', "opts": ["without", "the act of", "full of / having the quality of", "one who"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": '"Cause is to effect as action is to ___." Complete the analogy.', "opts": ["reason", "plan", "consequence", "goal"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'The prefix "hyper-" (as in "hyperactive") means…', "opts": ["under", "before", "against", "over/excessive"], "ans": 3, "cat": "Vocabulary", "diff": 2},
        {"q": '"Map is to geography as timeline is to ___." Complete the analogy.', "opts": ["art", "science", "music", "history"], "ans": 3, "cat": "Vocabulary", "diff": 2},
        {"q": 'The prefix "sub-" (as in "submarine") means…', "opts": ["over", "before", "under", "against"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": '"Optimist is to hope as pessimist is to ___." Complete the analogy.', "opts": ["joy", "energy", "despair", "action"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'The suffix "-ify" (as in "clarify") means…', "opts": ["without", "full of", "one who", "to make or cause to be"], "ans": 3, "cat": "Vocabulary", "diff": 2},
        {"q": '"Symptom is to disease as clue is to ___." Complete the analogy.', "opts": ["criminal", "mystery", "police", "court"], "ans": 1, "cat": "Vocabulary", "diff": 2},
        {"q": 'The prefix "inter-" (as in "international") means…', "opts": ["within", "before", "between or among", "against"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": '"Transparent is to opaque as clear is to ___." Complete the analogy.', "opts": ["bright", "see-through", "shiny", "blocked"], "ans": 3, "cat": "Vocabulary", "diff": 2},
        {"q": 'The suffix "-ance/-ence" (as in "performance") means…', "opts": ["one who performs", "the act or state of", "without", "to perform again"], "ans": 1, "cat": "Vocabulary", "diff": 2},

        # diff 3 — nuanced vocabulary, academic word list
        {"q": 'What does "ambivalent" mean?', "opts": ["very certain", "having mixed or uncertain feelings", "very happy", "completely confused"], "ans": 1, "cat": "Vocabulary", "diff": 3},
        {"q": '"The data ___ a clear trend." Which word fits? (shows evidence of)', "opts": ["hides", "ignores", "indicates", "destroys"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": 'What does "eloquent" mean?', "opts": ["speaking poorly", "speaking clearly and effectively", "speaking loudly", "speaking rarely"], "ans": 1, "cat": "Vocabulary", "diff": 3},
        {"q": '"The study ___ that exercise improves mood." Which word fits? (suggests but doesn\'t prove)', "opts": ["proves", "confirms", "suggests", "guarantees"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": 'What does "tenacious" mean?', "opts": ["very weak", "giving up easily", "keeping a firm hold; not giving up", "moving very fast"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": '"The ___ of his speech convinced the audience." (power and skill of expression)', "opts": ["length", "volume", "eloquence", "simplicity"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": 'What does "perspective" mean in an argument?', "opts": ["a proven fact", "a type of evidence", "a point of view or way of seeing something", "a conclusion"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": 'What does "reluctant" mean?', "opts": ["eager and enthusiastic", "not wanting to do something", "very confident", "very slow"], "ans": 1, "cat": "Vocabulary", "diff": 3},
        {"q": '"The scientist sought to ___ the results." (prove to be false)', "opts": ["confirm", "support", "ignore", "refute"], "ans": 3, "cat": "Vocabulary", "diff": 3},
        {"q": 'What does "integrity" mean?', "opts": ["great intelligence", "physical strength", "being honest and having strong moral principles", "great wealth"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": 'What does "vague" mean?', "opts": ["very specific and clear", "not clear or detailed", "very long", "very short"], "ans": 1, "cat": "Vocabulary", "diff": 3},
        {"q": '"The argument was ___." (well-reasoned and convincing)', "opts": ["vague", "weak", "compelling", "irrelevant"], "ans": 2, "cat": "Vocabulary", "diff": 3},

        # diff 4 — advanced figurative language analysis, etymology
        {"q": '"The pen is mightier than the sword." This implies that…', "opts": ["swords are weak", "writing and ideas are more powerful than violence", "pens are dangerous", "soldiers use pens"], "ans": 1, "cat": "Vocabulary", "diff": 4},
        {"q": 'The Greek root "dem/demo" (as in "democracy") means…', "opts": ["ruler", "law", "people", "power"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": '"Through the window, the city glittered like a field of stars." This is a…', "opts": ["metaphor", "simile", "personification", "hyperbole"], "ans": 1, "cat": "Vocabulary", "diff": 4},
        {"q": 'The Latin root "fract/frag" (as in "fracture") means…', "opts": ["to join", "to break", "to grow", "to flow"], "ans": 1, "cat": "Vocabulary", "diff": 4},
        {"q": 'What literary device uses contradictory terms together, like "bittersweet"?', "opts": ["simile", "hyperbole", "oxymoron", "alliteration"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": 'The Greek root "polis" (as in "politics") means…', "opts": ["family", "city/state", "water", "war"], "ans": 1, "cat": "Vocabulary", "diff": 4},
        {"q": '"Living death" and "deafening silence" are examples of…', "opts": ["similes", "hyperboles", "personification", "oxymorons"], "ans": 3, "cat": "Vocabulary", "diff": 4},
        {"q": 'The Latin root "cred" (as in "incredible") means…', "opts": ["to see", "to believe or trust", "to say", "to write"], "ans": 1, "cat": "Vocabulary", "diff": 4},
        {"q": 'What is an "allusion" in literature?', "opts": ["a direct quote", "a visual image", "an indirect reference to a well-known person, place, or event", "a type of rhyme"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": 'The Latin root "mort" (as in "mortal") means…', "opts": ["life", "death", "water", "fire"], "ans": 1, "cat": "Vocabulary", "diff": 4},
        {"q": '"Cruel kindness" is an example of…', "opts": ["hyperbole", "simile", "personification", "oxymoron"], "ans": 3, "cat": "Vocabulary", "diff": 4},
        {"q": 'The Greek root "path" (as in "sympathy") means…', "opts": ["thought", "feeling/suffering", "body", "mind"], "ans": 1, "cat": "Vocabulary", "diff": 4},

        # diff 5 — advanced etymology, academic vocabulary, complex analogies
        {"q": 'What does "ubiquitous" mean?', "opts": ["very rare", "very large", "very old", "seeming to be everywhere at once"], "ans": 3, "cat": "Vocabulary", "diff": 5},
        {"q": '"Catalyst is to reaction as trigger is to ___." Complete the analogy.', "opts": ["end", "event", "delay", "silence"], "ans": 1, "cat": "Vocabulary", "diff": 5},
        {"q": 'What does "paradigm" mean?', "opts": ["a type of experiment", "a proven fact", "a diagram", "a typical model or pattern of thinking"], "ans": 3, "cat": "Vocabulary", "diff": 5},
        {"q": 'The Latin root "spec/spect" (as in "inspect") means…', "opts": ["to speak", "to see/look at", "to hear", "to write"], "ans": 1, "cat": "Vocabulary", "diff": 5},
        {"q": 'What does "pragmatic" mean?', "opts": ["very emotional", "based on imagination", "dealing with things practically rather than theoretically", "very detailed"], "ans": 2, "cat": "Vocabulary", "diff": 5},
        {"q": '"Hypothesis is to theory as guess is to ___." Complete the analogy.', "opts": ["fact", "error", "proven explanation", "question"], "ans": 2, "cat": "Vocabulary", "diff": 5},
        {"q": 'What does "nuanced" mean?', "opts": ["very simple", "very obvious", "showing subtle and complex distinctions", "completely unclear"], "ans": 2, "cat": "Vocabulary", "diff": 5},
        {"q": 'The Latin root "luc/lum" (as in "illuminate") means…', "opts": ["water", "dark", "light", "heat"], "ans": 2, "cat": "Vocabulary", "diff": 5},
        {"q": 'What does "rhetoric" mean?', "opts": ["a type of poem", "the art of effective or persuasive speaking/writing", "a grammar rule", "a style of music"], "ans": 1, "cat": "Vocabulary", "diff": 5},
        {"q": '"Genre is to literature as medium is to ___." Complete the analogy.', "opts": ["science", "art", "history", "math"], "ans": 1, "cat": "Vocabulary", "diff": 5},
        {"q": 'What does "ephemeral" mean?', "opts": ["lasting forever", "very large", "lasting only a very short time", "very important"], "ans": 2, "cat": "Vocabulary", "diff": 5},
        {"q": 'The Greek root "chron" (as in "chronicle") means…', "opts": ["color", "time", "sound", "space"], "ans": 1, "cat": "Vocabulary", "diff": 5},
    ],

    # ── Grade 6 ──────────────────────────────────────────────────────────────
    6: [
        # diff 1 — etymology, academic word list level 3
        {"q": 'The Latin root "equi" (as in "equilibrium") means…', "opts": ["over", "under", "equal", "far"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": 'What does "synthesize" mean in academic writing?', "opts": ["to list facts", "to describe one idea", "to combine information from multiple sources", "to argue against an idea"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": 'The Latin root "alter" (as in "alternate") means…', "opts": ["same", "other", "first", "last"], "ans": 1, "cat": "Vocabulary", "diff": 1},
        {"q": 'What does "substantiate" mean?', "opts": ["to question", "to deny", "to support with evidence", "to ignore"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": 'The Greek root "tele" (as in "telegram") means…', "opts": ["fast", "small", "far", "bright"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": 'What does "mitigate" mean?', "opts": ["to make worse", "to ignore completely", "to make less severe", "to celebrate"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": 'The Latin root "vert/vers" (as in "convert") means…', "opts": ["to see", "to turn", "to build", "to speak"], "ans": 1, "cat": "Vocabulary", "diff": 1},
        {"q": 'What does "corroborate" mean?', "opts": ["to argue against", "to ignore", "to confirm or support with additional evidence", "to question"], "ans": 2, "cat": "Vocabulary", "diff": 1},
        {"q": 'The Latin root "mal" (as in "malfunction") means…', "opts": ["good", "over", "again", "bad"], "ans": 3, "cat": "Vocabulary", "diff": 1},
        {"q": 'What does "diverge" mean? (di- = apart)', "opts": ["to come together", "to move apart in different directions", "to stay still", "to repeat"], "ans": 1, "cat": "Vocabulary", "diff": 1},
        {"q": 'The Latin root "nov" (as in "innovate") means…', "opts": ["old", "fast", "small", "new"], "ans": 3, "cat": "Vocabulary", "diff": 1},
        {"q": 'What does "immutable" mean? (im- = not, mut = change)', "opts": ["easily changed", "impossible to change", "changing often", "slowly changing"], "ans": 1, "cat": "Vocabulary", "diff": 1},

        # diff 2 — nuanced word choice, advanced argument vocabulary
        {"q": '"Sycophant" describes someone who…', "opts": ["argues with authority", "praises others excessively to gain favor", "works extremely hard", "thinks independently"], "ans": 1, "cat": "Vocabulary", "diff": 2},
        {"q": 'What does "cogent" mean when describing an argument?', "opts": ["very long", "confusing and unclear", "clear, logical, and convincing", "emotional and passionate"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'What does "superfluous" mean?', "opts": ["necessary", "extremely important", "very rare", "more than what is needed; unnecessary"], "ans": 3, "cat": "Vocabulary", "diff": 2},
        {"q": 'What does "extrapolate" mean?', "opts": ["to describe in detail", "to deny a claim", "to extend known data to predict unknown situations", "to simplify"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'What does "esoteric" mean?', "opts": ["very popular", "very simple", "understood by many people", "understood by only a small specialized group"], "ans": 3, "cat": "Vocabulary", "diff": 2},
        {"q": 'What does "indelible" mean?', "opts": ["easily erased", "lasting forever; impossible to forget or remove", "very colorful", "very small"], "ans": 1, "cat": "Vocabulary", "diff": 2},
        {"q": 'What does "pervasive" mean?', "opts": ["found rarely", "found in one place only", "slowly disappearing", "spreading widely throughout"], "ans": 3, "cat": "Vocabulary", "diff": 2},
        {"q": 'What does "prerogative" mean?', "opts": ["a type of problem", "a responsibility", "a right or privilege", "a limitation"], "ans": 2, "cat": "Vocabulary", "diff": 2},
        {"q": 'What does "dichotomy" mean?', "opts": ["a gradual change", "a division into two opposite things", "a type of argument", "a similarity"], "ans": 1, "cat": "Vocabulary", "diff": 2},
        {"q": 'What does "ameliorate" mean?', "opts": ["to make worse", "to make better or more bearable", "to keep the same", "to completely solve"], "ans": 1, "cat": "Vocabulary", "diff": 2},
        {"q": 'What does "taciturn" mean?', "opts": ["very talkative", "very emotional", "very secretive", "habitually silent"], "ans": 3, "cat": "Vocabulary", "diff": 2},
        {"q": 'What does "nuance" mean?', "opts": ["a major obvious difference", "a type of argument", "a subtle distinction or detail", "a clear conclusion"], "ans": 2, "cat": "Vocabulary", "diff": 2},

        # diff 3 — allusions, oxymorons, complex figurative language
        {"q": '"David and Goliath" as an allusion in modern writing refers to…', "opts": ["a story about giants", "a small person defeating a much larger opponent", "an ancient battle", "a religious miracle"], "ans": 1, "cat": "Vocabulary", "diff": 3},
        {"q": '"The sound of silence" is an example of…', "opts": ["simile", "hyperbole", "personification", "oxymoron"], "ans": 3, "cat": "Vocabulary", "diff": 3},
        {"q": '"He is a modern Romeo." This allusion suggests he is…', "opts": ["a skilled fighter", "a great leader", "a very romantic person", "a tragic villain"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": '"Clearly confused" and "awfully good" are examples of…', "opts": ["similes", "hyperboles", "oxymorons", "alliterations"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": '"Opening Pandora\'s box" alludes to…', "opts": ["solving all problems", "starting something with uncontrollable negative consequences", "finding great treasure", "solving a mystery"], "ans": 1, "cat": "Vocabulary", "diff": 3},
        {"q": '"A Herculean task" refers to something that is…', "opts": ["very simple", "very quick", "extremely difficult", "very well organized"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": 'What is an "oxymoron"?', "opts": ["two words with the same meaning", "a word with multiple meanings", "two contradictory terms placed together", "an exaggerated statement"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": '"She\'s an Einstein when it comes to math." This allusion means she is…', "opts": ["very slow", "extremely intelligent", "very creative", "very old"], "ans": 1, "cat": "Vocabulary", "diff": 3},
        {"q": '"He met his Waterloo." This allusion suggests he…', "opts": ["visited France", "met a great leader", "suffered a decisive defeat", "achieved a great victory"], "ans": 2, "cat": "Vocabulary", "diff": 3},
        {"q": '"Small giant" and "deafening silence" are examples of…', "opts": ["similes", "personification", "hyperboles", "oxymorons"], "ans": 3, "cat": "Vocabulary", "diff": 3},
        {"q": '"Fighting windmills" (from Don Quixote) means…', "opts": ["working outdoors", "fighting real enemies", "solving real problems", "struggling with imaginary problems"], "ans": 3, "cat": "Vocabulary", "diff": 3},
        {"q": '"Act of God" and "controlled chaos" are examples of…', "opts": ["allusions", "hyperboles", "oxymorons", "similes"], "ans": 2, "cat": "Vocabulary", "diff": 3},

        # diff 4 — pathos/logos/ethos, rhetorical devices, juxtaposition
        {"q": 'What is "pathos" in rhetoric?', "opts": ["an appeal to logic", "an appeal to the speaker\'s credibility", "an appeal to emotion", "an appeal to authority"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does "juxtaposition" mean in writing?', "opts": ["repeating an idea", "placing two contrasting things side by side", "listing things in order", "building to a climax"], "ans": 1, "cat": "Vocabulary", "diff": 4},
        {"q": 'What is "logos" in rhetoric?', "opts": ["an appeal to emotion", "an appeal to credibility", "an appeal to logic and reason", "an appeal to tradition"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does "anaphora" mean in rhetoric?', "opts": ["a sudden change of topic", "repeating a word at the end of clauses", "repeating a word at the beginning of successive clauses", "using contradictory terms"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": 'What is "ethos" in rhetoric?', "opts": ["an appeal to emotion", "an appeal to the speaker\'s credibility and character", "an appeal to logic", "an appeal to fear"], "ans": 1, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does "chiasmus" refer to? (e.g., "Ask not what your country can do for you…")', "opts": ["a simile using like or as", "a reversal of grammatical structure in successive phrases", "a repeated metaphor", "an extended analogy"], "ans": 1, "cat": "Vocabulary", "diff": 4},
        {"q": 'What is "synecdoche"? (e.g., "All hands on deck")', "opts": ["a part representing the whole, or the whole for a part", "an exaggeration", "a comparison using like or as", "a repeated sound"], "ans": 0, "cat": "Vocabulary", "diff": 4},
        {"q": 'What is the difference between "denotation" and "connotation"?', "opts": ["they are the same", "denotation is emotional meaning; connotation is literal", "denotation is literal meaning; connotation is emotional/cultural meaning", "both refer to figurative language"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": '"We shall fight on the beaches… we shall never surrender." This uses…', "opts": ["simile", "personification", "oxymoron", "anaphora"], "ans": 3, "cat": "Vocabulary", "diff": 4},
        {"q": 'What is "euphemism"?', "opts": ["an exaggeration", "a contradiction in terms", "a mild expression substituted for a harsh one", "a comparison without like or as"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": 'What does "hyperbole" achieve in rhetoric?', "opts": ["literal description", "providing evidence", "creating emphasis through exaggeration", "logical reasoning"], "ans": 2, "cat": "Vocabulary", "diff": 4},
        {"q": '"The pen is mightier than the sword." What rhetorical device is this?', "opts": ["anaphora", "synecdoche", "metaphor", "euphemism"], "ans": 2, "cat": "Vocabulary", "diff": 4},

        # diff 5 — nuanced vocabulary (most advanced), complex analogies
        {"q": 'What does "epistemology" study?', "opts": ["the nature of beauty", "the nature and limits of knowledge", "the nature of morality", "the nature of existence"], "ans": 1, "cat": "Vocabulary", "diff": 5},
        {"q": '"Axiom is to proof as premise is to ___." Complete the analogy.', "opts": ["question", "conclusion", "hypothesis", "topic"], "ans": 1, "cat": "Vocabulary", "diff": 5},
        {"q": 'What does "ontology" study? (ont = being)', "opts": ["the nature of knowledge", "the nature of existence and reality", "the nature of beauty", "the nature of society"], "ans": 1, "cat": "Vocabulary", "diff": 5},
        {"q": 'What effect does juxtaposition create in a text?', "opts": ["it creates rhyme", "it highlights similarities", "it entertains the reader", "it emphasizes contrasts"], "ans": 3, "cat": "Vocabulary", "diff": 5},
        {"q": 'What does "dialectical" thinking involve?', "opts": ["emotional reasoning", "random guessing", "examining contradictions to reach truth", "following tradition"], "ans": 2, "cat": "Vocabulary", "diff": 5},
        {"q": '"Soliloquy is to theater as inner monologue is to ___." Complete the analogy.', "opts": ["music", "painting", "novel", "film script"], "ans": 2, "cat": "Vocabulary", "diff": 5},
        {"q": 'What does "verisimilitude" mean in fiction?', "opts": ["a type of plot twist", "an unreliable narrator", "a violent scene", "the appearance of being real or true"], "ans": 3, "cat": "Vocabulary", "diff": 5},
        {"q": '"Archetype is to character as motif is to ___." Complete the analogy.', "opts": ["plot", "setting", "theme", "genre"], "ans": 2, "cat": "Vocabulary", "diff": 5},
        {"q": 'What does "polemic" describe?', "opts": ["a balanced argument", "a strong attack on or argument against someone\'s opinions", "a type of poem", "a literary analysis"], "ans": 1, "cat": "Vocabulary", "diff": 5},
        {"q": '"Genre is to novel as form is to ___." Complete the analogy.', "opts": ["history", "color", "poetry", "grammar"], "ans": 2, "cat": "Vocabulary", "diff": 5},
        {"q": 'What does "anachronism" mean?', "opts": ["a hidden symbol", "a type of metaphor", "something placed in the wrong time period", "an unresolved conflict"], "ans": 2, "cat": "Vocabulary", "diff": 5},
        {"q": '"Protagonist is to antagonist as thesis is to ___." Complete the analogy.', "opts": ["argument", "evidence", "antithesis", "conclusion"], "ans": 2, "cat": "Vocabulary", "diff": 5},
    ],
}

# ─── Science question bank ─────────────────────────────────────────────────────
SCIENCE_QS = {

    # ── Grade 1 ──────────────────────────────────────────────────────────────
    1: [
        # diff 1 — 5 senses, living vs. non-living
        {"q": "Which body part do you use to see?", "opts": ["ears", "eyes", "nose", "mouth"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "Which body part do you use to hear?", "opts": ["eyes", "nose", "ears", "hands"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "Which sense helps you smell a flower?", "opts": ["sight", "hearing", "touch", "smell"], "ans": 3, "cat": "Science", "diff": 1},
        {"q": "Is a rock a living thing?", "opts": ["Yes", "No", "Sometimes", "Maybe"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "Is a dog a living thing?", "opts": ["No", "Yes", "Only at night", "Maybe"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "How many senses does a person have?", "opts": ["3", "4", "5", "6"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "Which body part do you use to taste food?", "opts": ["nose", "ears", "tongue", "eyes"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "Which is a living thing?", "opts": ["rock", "water", "chair", "tree"], "ans": 3, "cat": "Science", "diff": 1},
        {"q": "Which body part do you use to touch things?", "opts": ["eyes", "ears", "nose", "hands"], "ans": 3, "cat": "Science", "diff": 1},
        {"q": "Which is NOT a living thing?", "opts": ["fish", "flower", "table", "cat"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "What do living things need to grow?", "opts": ["metal", "food and water", "glass", "plastic"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "What do you use to feel if something is hot or cold?", "opts": ["eyes", "ears", "skin", "nose"], "ans": 2, "cat": "Science", "diff": 1},

        # diff 2 — plants basics, animals and their homes
        {"q": "What part of a plant holds it in the ground?", "opts": ["leaf", "root", "stem", "flower"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "What do plants need from the sun?", "opts": ["water", "soil", "light", "air"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "Which part of a plant makes seeds?", "opts": ["root", "stem", "leaf", "flower"], "ans": 3, "cat": "Science", "diff": 2},
        {"q": "What do plants drink?", "opts": ["juice", "milk", "water", "soil"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "Where do most fish live?", "opts": ["desert", "forest", "water", "sky"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "Which animal lays eggs?", "opts": ["dog", "cat", "horse", "bird"], "ans": 3, "cat": "Science", "diff": 2},
        {"q": "What color are leaves usually?", "opts": ["red", "green", "blue", "purple"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "Which part of a plant carries water up from the roots?", "opts": ["flower", "leaf", "stem", "seed"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "Where does a bird make its home?", "opts": ["hole", "nest", "pond", "cave"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "What do most plants grow from?", "opts": ["eggs", "seeds", "rocks", "water"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "Which animal eats grass?", "opts": ["lion", "shark", "cow", "eagle"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "What do leaves use sunlight to do?", "opts": ["sleep", "make food", "drink water", "sing"], "ans": 1, "cat": "Science", "diff": 2},

        # diff 3 — weather and seasons
        {"q": "Which season is the coldest?", "opts": ["spring", "summer", "fall", "winter"], "ans": 3, "cat": "Science", "diff": 3},
        {"q": "What falls from clouds during a storm?", "opts": ["snow only", "rain or snow", "sunshine", "wind"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "Which season do many flowers bloom?", "opts": ["winter", "fall", "spring", "summer"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "What tool measures temperature?", "opts": ["ruler", "thermometer", "scale", "clock"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "What type of weather has strong winds and heavy rain?", "opts": ["sunny", "foggy", "storm", "cloudy"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "In which season do leaves fall from trees?", "opts": ["summer", "spring", "winter", "fall"], "ans": 3, "cat": "Science", "diff": 3},
        {"q": "What falls from the sky in winter when it is very cold?", "opts": ["rain", "snow", "sun", "wind"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "Which season comes after spring?", "opts": ["fall", "winter", "summer", "spring"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "How many seasons are in a year?", "opts": ["2", "3", "4", "5"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "What do we call days with lots of sun and no clouds?", "opts": ["rainy", "cloudy", "windy", "sunny"], "ans": 3, "cat": "Science", "diff": 3},
        {"q": "Which season is the hottest?", "opts": ["spring", "summer", "fall", "winter"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "Where does rain come from?", "opts": ["the ground", "rivers", "clouds", "trees"], "ans": 2, "cat": "Science", "diff": 3},

        # diff 4 — push/pull forces, floating/sinking, day and night
        {"q": "When you push a ball, what makes it move?", "opts": ["heat", "light", "force", "color"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "Which object usually floats in water?", "opts": ["rock", "coin", "wooden block", "metal spoon"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "What do we call the force that pulls things toward the ground?", "opts": ["wind", "gravity", "heat", "light"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "Which object usually sinks in water?", "opts": ["balloon", "leaf", "feather", "rock"], "ans": 3, "cat": "Science", "diff": 4},
        {"q": "What gives us daylight?", "opts": ["the moon", "stars", "the sun", "clouds"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "When you pull something, you move it ___ you.", "opts": ["away from", "toward", "over", "under"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "What happens to the sky when the sun sets?", "opts": ["It gets cold", "It rains", "It gets dark", "It gets hot"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "Which is an example of a push?", "opts": ["pulling a door open", "pressing a button", "picking up a bag", "lifting a box"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "Which is an example of a pull?", "opts": ["pushing a door closed", "kicking a ball", "opening a door toward you", "pressing a button"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "What do we see in the sky at night?", "opts": ["the sun", "the moon and stars", "clouds only", "nothing"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "A heavy rock is harder to push than a feather because it has more ___.", "opts": ["color", "size", "mass", "warmth"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "Which comes first in a day?", "opts": ["midnight", "sunset", "sunrise", "noon"], "ans": 2, "cat": "Science", "diff": 4},

        # diff 5 — plant life cycle, animal needs, habitats
        {"q": "What is the first stage in a plant's life cycle?", "opts": ["flower", "seed", "leaf", "fruit"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "Which do ALL living things need?", "opts": ["soil only", "sunlight only", "water and food", "plastic and glass"], "ans": 2, "cat": "Science", "diff": 5},
        {"q": "A caterpillar changes into a ___.", "opts": ["frog", "bird", "butterfly", "fish"], "ans": 2, "cat": "Science", "diff": 5},
        {"q": "What do we call the natural home where an animal lives?", "opts": ["school", "habitat", "factory", "store"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "What grows from a seed into a seedling?", "opts": ["animal", "rock", "plant", "water"], "ans": 2, "cat": "Science", "diff": 5},
        {"q": "Which animal lives in the ocean?", "opts": ["camel", "dolphin", "eagle", "bear"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "What do plants make in their leaves using sunlight?", "opts": ["water", "soil", "food/sugar", "air only"], "ans": 2, "cat": "Science", "diff": 5},
        {"q": "Which is a desert animal?", "opts": ["penguin", "camel", "dolphin", "frog"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "What does a seed need to sprout?", "opts": ["sunlight only", "water, soil, and warmth", "plastic", "nothing"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "How do plants help animals?", "opts": ["by making noise", "by providing food and oxygen", "by making rain", "by creating gravity"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "A tadpole grows into a ___.", "opts": ["fish", "bird", "frog", "snake"], "ans": 2, "cat": "Science", "diff": 5},
        {"q": "What gas do plants release that animals need to breathe?", "opts": ["carbon dioxide", "nitrogen", "oxygen", "hydrogen"], "ans": 2, "cat": "Science", "diff": 5},
    ],

    # ── Grade 2 ──────────────────────────────────────────────────────────────
    2: [
        # diff 1 — life cycles and animal groups
        {"q": "What are the four stages of a butterfly's life?", "opts": ["egg, fish, bird, adult", "egg, larva, pupa, adult", "seed, sprout, plant, fruit", "egg, tadpole, frog, adult"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "Which animal goes through metamorphosis?", "opts": ["dog", "horse", "frog", "elephant"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "What do we call animals that have a backbone?", "opts": ["insects", "vertebrates", "plants", "fungi"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "Which group do fish belong to?", "opts": ["birds", "mammals", "reptiles", "fish"], "ans": 3, "cat": "Science", "diff": 1},
        {"q": "What is a tadpole?", "opts": ["a baby fish", "a baby bird", "a baby frog", "a baby butterfly"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "Which animal is a mammal?", "opts": ["eagle", "salmon", "whale", "crocodile"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "What do mammals feed their babies?", "opts": ["grass", "fish", "milk", "insects"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "Which stage comes after the egg in a butterfly's life?", "opts": ["adult", "pupa", "caterpillar/larva", "flower"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "Which animal is a reptile?", "opts": ["dolphin", "frog", "lizard", "eagle"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "Which of these is a bird?", "opts": ["bat", "penguin", "whale", "lizard"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "What does a caterpillar become inside a pupa?", "opts": ["moth or butterfly", "bird", "fish", "frog"], "ans": 0, "cat": "Science", "diff": 1},
        {"q": "Which animal lives on both land and in water?", "opts": ["mammal", "bird only", "amphibian", "fish only"], "ans": 2, "cat": "Science", "diff": 1},

        # diff 2 — states of matter
        {"q": "Which is an example of a solid?", "opts": ["water", "air", "rock", "steam"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "Which is an example of a liquid?", "opts": ["ice", "stone", "milk", "smoke"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "Which is an example of a gas?", "opts": ["wood", "juice", "sand", "steam"], "ans": 3, "cat": "Science", "diff": 2},
        {"q": "What happens to water when it freezes?", "opts": ["It becomes a gas", "It becomes a solid", "It disappears", "It becomes warm"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "What happens to ice when it gets warm?", "opts": ["It gets bigger", "It melts to liquid", "It turns to stone", "It flies away"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "Which state of matter has a definite shape?", "opts": ["liquid", "gas", "solid", "air"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "Which state of matter spreads to fill its container?", "opts": ["solid", "liquid", "gas", "ice"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "What do we call the change from liquid to gas?", "opts": ["freezing", "melting", "evaporation", "condensation"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "Which state of matter cannot be seen but can be felt?", "opts": ["solid", "liquid", "gas", "water"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "What do we call the change from solid to liquid?", "opts": ["freezing", "melting", "evaporation", "boiling"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "What state of matter is air?", "opts": ["solid", "liquid", "gas", "water"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "Which state of matter flows and takes the shape of its container?", "opts": ["solid", "liquid", "gas", "rock"], "ans": 1, "cat": "Science", "diff": 2},

        # diff 3 — weather patterns and clouds
        {"q": "What type of cloud is fluffy and white?", "opts": ["cirrus", "stratus", "cumulus", "fog"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "What tool measures wind speed?", "opts": ["thermometer", "ruler", "anemometer", "scale"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "What type of cloud is thin and high in the sky?", "opts": ["cumulus", "cirrus", "stratus", "nimbus"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "Which weather condition has low clouds that reduce visibility?", "opts": ["sunny", "windy", "foggy", "hot"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "What causes wind?", "opts": ["moving clouds", "moving water", "moving air", "moving soil"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "What tool measures how much rain has fallen?", "opts": ["thermometer", "rain gauge", "anemometer", "barometer"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "Which type of cloud often brings heavy rain?", "opts": ["cirrus", "cumulus", "nimbostratus", "fog"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "What is it called when water moves from oceans to clouds and back to land?", "opts": ["food chain", "water cycle", "life cycle", "rock cycle"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "How does the sun affect the weather?", "opts": ["It creates fog", "It heats the air and water", "It makes wind by moving", "It causes earthquakes"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "What do we call ice crystals that fall from clouds?", "opts": ["rain", "hail", "snow", "fog"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "Which direction does hot air move?", "opts": ["down", "sideways", "up", "in circles"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "What causes seasons to change on Earth?", "opts": ["Earth orbiting the sun", "the moon changing shape", "clouds moving", "wind changing direction"], "ans": 0, "cat": "Science", "diff": 3},

        # diff 4 — habitats and animal adaptations intro
        {"q": "Which animal is adapted to live in a cold, icy habitat?", "opts": ["camel", "polar bear", "elephant", "frog"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "What do we call an animal's natural home environment?", "opts": ["school", "factory", "habitat", "store"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "Which animal is adapted for a hot desert?", "opts": ["polar bear", "penguin", "camel", "whale"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "Why do ducks have webbed feet?", "opts": ["to climb trees", "to run fast", "to swim in water", "to dig in sand"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "When an animal's color matches its surroundings to hide, it is called ___.", "opts": ["migration", "adaptation", "camouflage", "hibernation"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "Why do bears hibernate in winter?", "opts": ["They like cold", "Food is scarce and temperatures drop", "They are sick", "They travel south"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "Which body part helps a fish breathe underwater?", "opts": ["lungs", "gills", "skin", "fins"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "What is an adaptation?", "opts": ["a type of weather", "a feature that helps an organism survive", "a kind of habitat", "part of the water cycle"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "Why do some birds fly south in winter?", "opts": ["to find cooler weather", "to find food and warmth", "to escape rain", "to find salt water"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "Which feature helps a cactus survive in the desert?", "opts": ["thick stems that store water", "large roots that float", "soft bark", "colorful flowers only"], "ans": 0, "cat": "Science", "diff": 4},
        {"q": "What is migration?", "opts": ["animals sleeping in winter", "animals moving seasonally for food or warmth", "animals hiding from predators", "animals building nests"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "Why do owls have large eyes?", "opts": ["to scare other animals", "to see well in the dark", "to help them fly", "to find water"], "ans": 1, "cat": "Science", "diff": 4},

        # diff 5 — simple machines
        {"q": "What is a lever?", "opts": ["a type of wheel", "a bar that turns on a fulcrum to lift things", "a ramp for sliding objects up", "a wheel with a rope"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "Which simple machine is a ramp?", "opts": ["lever", "wheel and axle", "inclined plane", "pulley"], "ans": 2, "cat": "Science", "diff": 5},
        {"q": "What is a pulley used for?", "opts": ["to cut things", "to lift or move objects using a rope and wheel", "to measure temperature", "to mix liquids"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "Which simple machine is found in a door knob?", "opts": ["lever", "inclined plane", "wheel and axle", "pulley"], "ans": 2, "cat": "Science", "diff": 5},
        {"q": "How does an inclined plane help us?", "opts": ["It makes things heavier", "It makes moving heavy loads upward easier", "It helps us cut paper", "It creates electricity"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "The point where a lever balances is called the ___.", "opts": ["pivot", "axle", "fulcrum", "gear"], "ans": 2, "cat": "Science", "diff": 5},
        {"q": "Which simple machine is used in scissors?", "opts": ["lever", "pulley", "wheel and axle", "inclined plane"], "ans": 0, "cat": "Science", "diff": 5},
        {"q": "A screw is a twisted ___.", "opts": ["inclined plane", "type of wheel", "kind of pulley", "flat lever"], "ans": 0, "cat": "Science", "diff": 5},
        {"q": "What do simple machines do?", "opts": ["They create energy", "They make work easier", "They store water", "They heat homes"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "Which simple machine helps you raise a flag on a flagpole?", "opts": ["lever", "wedge", "pulley", "inclined plane"], "ans": 2, "cat": "Science", "diff": 5},
        {"q": "A wedge is used to ___.", "opts": ["lift objects up", "split or separate objects", "measure mass", "carry water"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "Which simple machine is found in a bicycle wheel?", "opts": ["pulley", "lever", "wheel and axle", "wedge"], "ans": 2, "cat": "Science", "diff": 5},
    ],

    # ── Grade 3 ──────────────────────────────────────────────────────────────
    3: [
        # diff 1 — food chains (producer/consumer/decomposer)
        {"q": "What is a producer in a food chain?", "opts": ["an animal that eats plants", "a plant that makes its own food", "an animal that eats meat", "a fungus that breaks down waste"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "What is a consumer?", "opts": ["a plant that makes food", "a fungus", "an organism that eats other organisms", "a rock"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "Where does a food chain start?", "opts": ["with an animal", "with a plant/producer", "with a fungus", "with the sun only"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "What do decomposers do?", "opts": ["hunt animals", "make food from sunlight", "break down dead organisms", "swim in water"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "In the chain grass → rabbit → fox, what is the rabbit?", "opts": ["producer", "decomposer", "consumer", "predator only"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "What is a herbivore?", "opts": ["an animal that eats only meat", "an animal that eats only plants", "an animal that eats both", "a plant"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "What is a carnivore?", "opts": ["an animal that eats only plants", "an animal that eats only meat", "an animal that eats both plants and meat", "a decomposer"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "Which organism is a decomposer?", "opts": ["lion", "grass", "mushroom/fungus", "eagle"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "What is an omnivore?", "opts": ["an animal that eats only plants", "an animal that eats only meat", "an animal that eats both plants and meat", "a producer"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "In the chain leaf → caterpillar → bird, what is the leaf?", "opts": ["consumer", "decomposer", "producer", "predator"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "What is a predator?", "opts": ["an animal that is hunted", "an animal that hunts other animals", "a plant producer", "a decomposer"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "What is prey?", "opts": ["an animal that hunts", "an animal that is hunted by another", "a type of plant", "a type of fungus"], "ans": 1, "cat": "Science", "diff": 1},

        # diff 2 — the water cycle
        {"q": "What is evaporation?", "opts": ["water changing from gas to liquid", "water changing from liquid to gas", "water freezing into ice", "water falling as rain"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "What is condensation?", "opts": ["water becoming a gas", "water vapor cooling into liquid water drops", "water falling from clouds", "ice melting"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "What is precipitation?", "opts": ["water evaporating from oceans", "water vapor becoming clouds", "water falling from clouds as rain or snow", "water collecting in rivers"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "What drives the water cycle?", "opts": ["wind", "the moon", "energy from the sun", "gravity only"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "Where does most water evaporate from?", "opts": ["rivers", "glaciers", "oceans and lakes", "soil"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "What do we call water that flows into lakes and rivers after rain?", "opts": ["condensation", "runoff", "evaporation", "groundwater"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "Clouds are made of tiny drops of ___.", "opts": ["ice only", "water vapor and water droplets", "dust", "steam"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "What happens to water at a lake's surface on a hot day?", "opts": ["It freezes", "It evaporates", "It condenses", "It turns to rock"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "In the water cycle, what forms when water vapor cools?", "opts": ["rain directly", "clouds and fog", "ice only", "steam"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "Which stage of the water cycle delivers fresh water to the land?", "opts": ["evaporation", "condensation", "precipitation", "transpiration"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "Plants release water vapor through a process called ___.", "opts": ["evaporation", "condensation", "transpiration", "precipitation"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "What term names the complete path water takes from ocean to sky to land?", "opts": ["food chain", "rock cycle", "water cycle", "life cycle"], "ans": 2, "cat": "Science", "diff": 2},

        # diff 3 — rocks, minerals, and soil
        {"q": "What are the three main types of rock?", "opts": ["soft, hard, medium", "igneous, sedimentary, metamorphic", "red, black, white", "wet, dry, powdery"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "How is igneous rock formed?", "opts": ["from layers of sand pressing together", "from magma or lava cooling down", "from rocks squished by heat and pressure", "from living things decaying"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "How is sedimentary rock formed?", "opts": ["from cooling lava", "from layers of sediment pressed together over time", "from rocks squeezed by extreme heat", "from melted metal"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "What gives soil its dark color?", "opts": ["clay minerals", "sand grains", "decomposed organic matter (humus)", "rock fragments"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "Which rock was once a different type changed by heat and pressure?", "opts": ["igneous", "sedimentary", "metamorphic", "magma"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "What is a mineral?", "opts": ["a type of animal", "a naturally occurring solid substance", "a kind of soil", "a decomposed rock"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "Which soil layer contains the most nutrients for plants?", "opts": ["bedrock", "subsoil", "topsoil", "clay layer"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "What do we call the wearing away of rock by wind and water?", "opts": ["erosion", "deposition", "compression", "crystallization"], "ans": 0, "cat": "Science", "diff": 3},
        {"q": "Which type of rock often contains fossils?", "opts": ["igneous", "metamorphic", "sedimentary", "magma"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "What is the hardest natural mineral?", "opts": ["granite", "quartz", "diamond", "marble"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "What causes metamorphic rock to form?", "opts": ["cooling lava", "layering of sediment", "extreme heat and pressure", "freezing water"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "What are fossils?", "opts": ["crystals in rock", "preserved remains of ancient living things found in rock", "types of soil", "minerals that glow"], "ans": 1, "cat": "Science", "diff": 3},

        # diff 4 — light, shadows, and sound
        {"q": "What is a shadow?", "opts": ["a reflection of light", "a dark area formed when an object blocks light", "a type of cloud", "a bright flash of light"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "What does light travel in?", "opts": ["curves", "circles", "straight lines", "zigzags"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "What happens to your shadow when you face the sun?", "opts": ["It appears in front of you", "It is behind you", "It disappears", "It gets larger"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "Sound is produced by ___.", "opts": ["light energy", "vibrations", "gravity", "heat only"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "Which travels faster — light or sound?", "opts": ["sound", "light", "they are equal", "it depends on the day"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "What does a mirror do to light?", "opts": ["absorbs it", "reflects it", "destroys it", "creates new light"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "When sound bounces off a hard surface and returns, it is called an ___.", "opts": ["orbit", "echo", "eclipse", "eruption"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "Which material allows light to pass through completely?", "opts": ["wood", "metal", "clear glass", "cardboard"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "What happens to sound as it travels farther from its source?", "opts": ["it gets louder", "it gets quieter", "it gets faster", "it changes pitch"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "What is the bending of light as it passes from air into water called?", "opts": ["reflection", "refraction", "absorption", "diffraction"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "Which material blocks light completely?", "opts": ["clear glass", "window screen", "opaque cardboard", "thin curtain"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "Higher-pitched sounds have ___ vibrations per second.", "opts": ["fewer", "more", "the same number of", "no"], "ans": 1, "cat": "Science", "diff": 4},

        # diff 5 — ecosystems and biomes
        {"q": "What is an ecosystem?", "opts": ["only the animals in an area", "all living and nonliving things in an area and their interactions", "only the plants in a forest", "a type of weather system"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "Which biome is very dry, receiving less than 25 cm of rain per year?", "opts": ["rainforest", "tundra", "desert", "wetland"], "ans": 2, "cat": "Science", "diff": 5},
        {"q": "What is a biome?", "opts": ["a single habitat", "a large region with specific climate, plants, and animals", "a food chain", "a type of rock"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "Which biome has the greatest biodiversity?", "opts": ["tundra", "desert", "tropical rainforest", "grassland"], "ans": 2, "cat": "Science", "diff": 5},
        {"q": "What do we call the variety of species living in an ecosystem?", "opts": ["food web", "biodiversity", "habitat", "population"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "Which nonliving things are part of an ecosystem?", "opts": ["animals and plants", "water, air, sunlight, soil, and rocks", "trees and birds", "bacteria only"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "What is a food web?", "opts": ["a single path of who eats whom", "many overlapping food chains in an ecosystem", "a type of habitat", "a biome map"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "The grassland biome is best described as ___.", "opts": ["mainly tall trees with no grass", "mostly grasses with few trees and moderate rainfall", "snow and ice year-round", "tropical trees and heavy rain"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "What do we call a species crucial to keeping an ecosystem balanced?", "opts": ["prey species", "keystone species", "invasive species", "decomposer species"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "Which biome has permafrost (permanently frozen ground)?", "opts": ["desert", "grassland", "tundra", "rainforest"], "ans": 2, "cat": "Science", "diff": 5},
        {"q": "Removing a keystone species from an ecosystem can ___.", "opts": ["change nothing", "cause the ecosystem to collapse or change dramatically", "make it healthier", "increase rainfall"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "What term describes species brought from elsewhere that harm local ecosystems?", "opts": ["native species", "keystone species", "invasive species", "endemic species"], "ans": 2, "cat": "Science", "diff": 5},
    ],

    # ── Grade 4 ──────────────────────────────────────────────────────────────
    4: [
        # diff 1 — body systems
        {"q": "What is the main job of the skeletal system?", "opts": ["to pump blood", "to support and protect the body", "to digest food", "to breathe air"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "Which organ pumps blood through the body?", "opts": ["lungs", "liver", "heart", "stomach"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "What is the job of the muscular system?", "opts": ["to filter blood", "to produce hormones", "to move the body by contracting", "to carry oxygen"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "Which organ is the control center of the nervous system?", "opts": ["heart", "lungs", "brain", "liver"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "What does the digestive system do?", "opts": ["pumps blood", "breaks down food to absorb nutrients", "carries messages through the body", "moves air in and out"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "Where does digestion begin?", "opts": ["stomach", "small intestine", "mouth", "liver"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "What is the job of the lungs?", "opts": ["to pump blood", "to digest food", "to take in oxygen and release carbon dioxide", "to produce hormones"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "What are bones primarily made of?", "opts": ["muscle tissue", "cartilage only", "calcium and minerals", "skin cells"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "How many bones are in the adult human body?", "opts": ["100", "150", "206", "300"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "What connects muscles to bones?", "opts": ["ligaments", "tendons", "cartilage", "nerves"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "Which organ system includes the skin?", "opts": ["skeletal system", "integumentary system", "nervous system", "digestive system"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "What do red blood cells carry throughout the body?", "opts": ["nutrients only", "waste only", "oxygen", "hormones"], "ans": 2, "cat": "Science", "diff": 1},

        # diff 2 — forms of energy
        {"q": "Which type of energy does the sun produce that plants use for photosynthesis?", "opts": ["electrical", "chemical", "light and heat", "mechanical"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "What is kinetic energy?", "opts": ["stored energy", "energy of motion", "heat energy", "chemical energy in food"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "What is potential energy?", "opts": ["energy being released", "energy of motion", "stored energy due to position or state", "electrical energy"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "A ball at the top of a hill has mainly ___ energy.", "opts": ["kinetic", "potential", "electrical", "nuclear"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "A ball rolling down a hill has mainly ___ energy.", "opts": ["potential", "kinetic", "chemical", "nuclear"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "Which energy form is produced when objects vibrate?", "opts": ["light", "heat", "sound", "electrical"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "When a flashlight turns on, electrical energy is changed to ___.", "opts": ["heat only", "light and heat", "sound only", "chemical energy"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "What type of energy does food store?", "opts": ["electrical", "mechanical", "chemical", "nuclear"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "Energy cannot be created or destroyed — it can only be ___.", "opts": ["used up completely", "stored forever unchanged", "transformed from one form to another", "eliminated"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "Which device converts mechanical energy into electrical energy?", "opts": ["light bulb", "generator", "battery", "heater"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "What type of energy is produced when you rub your hands together?", "opts": ["light", "sound", "heat", "chemical"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "Solar panels convert ___ energy into electrical energy.", "opts": ["heat", "chemical", "light/solar", "wind"], "ans": 2, "cat": "Science", "diff": 2},

        # diff 3 — adaptations (structural and behavioral)
        {"q": "What is a structural adaptation?", "opts": ["a behavior that helps survival", "a physical feature that helps an organism survive", "a type of habitat", "a food chain role"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "What is a behavioral adaptation?", "opts": ["a physical body part", "an action that helps an organism survive", "a type of rock", "a biome feature"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "A chameleon changing color to match its surroundings is an example of ___.", "opts": ["mimicry", "camouflage", "hibernation", "migration"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "An insect that looks like a dangerous animal to avoid predators is showing ___.", "opts": ["camouflage", "mimicry", "hibernation", "adaptation"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "A bird's hollow bones help it to ___.", "opts": ["swim faster", "fly by reducing body weight", "digest food better", "hear more clearly"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "Arctic foxes have white fur in winter. This is a ___ adaptation.", "opts": ["mimicry", "behavioral", "structural/camouflage", "hibernation"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "A snake that rattles its tail to warn predators is showing a ___.", "opts": ["structural adaptation", "behavioral adaptation", "camouflage", "migration"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "Which adaptation helps a plant survive drought?", "opts": ["broad flat leaves", "thick waxy skin and stored water", "thin stems", "colorful flowers only"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "Being nocturnal (active at night) helps animals ___.", "opts": ["get more sunlight", "avoid daytime predators and heat", "find more food in daylight", "sleep less"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "Monarch butterflies flying thousands of miles south each winter is an example of ___.", "opts": ["hibernation", "structural adaptation", "migration", "camouflage"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "A woodpecker's strong beak is adapted for ___.", "opts": ["swimming", "drilling into wood to find insects", "climbing rocks", "filtering water"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "Natural selection means organisms with helpful traits are more likely to ___.", "opts": ["choose their food", "survive and reproduce", "migrate south", "change color"], "ans": 1, "cat": "Science", "diff": 3},

        # diff 4 — properties and changes of matter
        {"q": "Which is a physical property of matter?", "opts": ["flammability", "color", "reactivity with acid", "ability to rust"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "Which is a chemical property of matter?", "opts": ["mass", "color", "shape", "flammability"], "ans": 3, "cat": "Science", "diff": 4},
        {"q": "A physical change ___.", "opts": ["creates a new substance", "changes the identity of matter", "changes size, shape, or state but not identity", "can never be reversed"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "A chemical change ___.", "opts": ["only changes shape", "produces a new substance with new properties", "changes only color of the same substance", "can always be easily reversed"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "Which is an example of a physical change?", "opts": ["burning wood", "rusting iron", "cutting paper", "baking a cake"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "Which is an example of a chemical change?", "opts": ["melting ice", "tearing cloth", "boiling water", "burning paper"], "ans": 3, "cat": "Science", "diff": 4},
        {"q": "What is density?", "opts": ["the amount of space an object takes up", "how heavy an object is", "mass per unit volume", "the temperature of an object"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "Which has greater density — iron or wood?", "opts": ["wood", "iron", "they are equal", "it depends"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "What is the difference between mass and weight?", "opts": ["they are the same", "mass is the amount of matter; weight depends on gravity", "weight measures matter; mass depends on gravity", "mass changes on the moon but weight does not"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "Which sign best indicates a chemical change has occurred?", "opts": ["an object is cut smaller", "a new gas is produced and color changes", "ice melts in the sun", "clay is reshaped"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "What is a mixture?", "opts": ["two substances that form a new compound", "substances physically combined that keep their own properties", "a pure substance", "a chemical change"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "How would you best separate a mixture of sand and iron filings?", "opts": ["heating it", "adding water", "using a magnet", "adding acid"], "ans": 2, "cat": "Science", "diff": 4},

        # diff 5 — Earth science (layers, volcanoes, earthquakes)
        {"q": "What are the four main layers of the Earth from surface to center?", "opts": ["crust, mantle, outer core, inner core", "ocean, rock, magma, center", "soil, rock, metal, gas", "sand, clay, rock, lava"], "ans": 0, "cat": "Science", "diff": 5},
        {"q": "What is the Earth's crust?", "opts": ["the liquid iron center", "the thinnest, outermost layer of Earth", "molten rock inside the Earth", "the mantle layer"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "What causes earthquakes?", "opts": ["water erosion", "tectonic plates shifting and releasing energy", "volcanoes cooling", "the moon's gravity"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "What is a volcano?", "opts": ["a crack in the ocean floor", "an opening in Earth's crust where magma erupts", "a mountain made of sedimentary rock", "a type of earthquake"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "What is magma?", "opts": ["molten rock inside the Earth", "lava that has cooled", "a type of sedimentary rock", "volcanic ash"], "ans": 0, "cat": "Science", "diff": 5},
        {"q": "What do we call magma after it reaches Earth's surface?", "opts": ["bedrock", "lava", "sediment", "still magma"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "Earth's surface is divided into large moving pieces called ___.", "opts": ["biomes", "ecosystems", "tectonic plates", "rock layers"], "ans": 2, "cat": "Science", "diff": 5},
        {"q": "Which scale measures the strength of an earthquake?", "opts": ["Celsius scale", "Beaufort scale", "Richter scale", "Mohs scale"], "ans": 2, "cat": "Science", "diff": 5},
        {"q": "What is the point underground where an earthquake originates called?", "opts": ["epicenter", "focus/hypocenter", "fault", "seismic wave"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "What is the point on Earth's surface directly above an earthquake's focus?", "opts": ["fault", "focus", "epicenter", "crater"], "ans": 2, "cat": "Science", "diff": 5},
        {"q": "What are seismic waves?", "opts": ["ocean waves caused by wind", "energy waves that travel through Earth during an earthquake", "sound waves in the atmosphere", "light waves from eruptions"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "Where are most volcanoes and earthquakes found?", "opts": ["at the center of tectonic plates", "along the boundaries of tectonic plates", "in the middle of oceans only", "near polar regions only"], "ans": 1, "cat": "Science", "diff": 5},
    ],

    # ── Grade 5 ──────────────────────────────────────────────────────────────
    5: [
        # diff 1 — cell basics (plant vs. animal)
        {"q": "What is the basic unit of life?", "opts": ["organ", "tissue", "cell", "organism"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "Which organelle controls what enters and leaves the cell?", "opts": ["nucleus", "cell membrane", "mitochondria", "ribosome"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "What does the nucleus do?", "opts": ["produces energy", "controls cell activities and contains DNA", "makes proteins", "stores water"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "Which organelle is called the powerhouse of the cell?", "opts": ["nucleus", "ribosome", "mitochondria", "vacuole"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "Which structure is found in plant cells but NOT in animal cells?", "opts": ["nucleus", "cell membrane", "mitochondria", "cell wall"], "ans": 3, "cat": "Science", "diff": 1},
        {"q": "What does the cell wall do in a plant cell?", "opts": ["produces food", "provides rigid support and protection", "controls the nucleus", "stores DNA"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "Which organelle is the site of photosynthesis in plant cells?", "opts": ["mitochondria", "ribosome", "chloroplast", "vacuole"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "What is the function of ribosomes?", "opts": ["to produce energy", "to store water", "to make proteins", "to control the cell"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "Which organelle stores water, waste, or nutrients?", "opts": ["ribosome", "mitochondria", "nucleus", "vacuole"], "ans": 3, "cat": "Science", "diff": 1},
        {"q": "Cells are too small to see with the naked eye — they are ___.", "opts": ["macroscopic", "microscopic", "visible", "transparent"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "What is the clear, jelly-like fluid that fills the cell?", "opts": ["plasma", "cytoplasm", "blood", "chlorophyll"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "Which scientist first observed cells using a microscope?", "opts": ["Darwin", "Einstein", "Robert Hooke", "Pasteur"], "ans": 2, "cat": "Science", "diff": 1},

        # diff 2 — photosynthesis and cellular respiration
        {"q": "What is photosynthesis?", "opts": ["cells breaking down food for energy", "plants making food using sunlight, water, and CO2", "animals eating plants for energy", "the water cycle process"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "What gas do plants take in during photosynthesis?", "opts": ["oxygen", "nitrogen", "carbon dioxide", "hydrogen"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "What gas do plants release during photosynthesis?", "opts": ["carbon dioxide", "nitrogen", "oxygen", "hydrogen"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "Where does photosynthesis occur in a plant?", "opts": ["roots", "stem", "leaves (chloroplasts)", "flowers"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "What is the green pigment in leaves that absorbs sunlight?", "opts": ["cellulose", "glucose", "chlorophyll", "starch"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "What sugar do plants produce during photosynthesis?", "opts": ["fructose", "lactose", "glucose", "sucrose"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "What process do cells use to release energy from glucose?", "opts": ["photosynthesis", "cellular respiration", "transpiration", "condensation"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "What gas do animals breathe out during cellular respiration?", "opts": ["oxygen", "nitrogen", "water vapor only", "carbon dioxide"], "ans": 3, "cat": "Science", "diff": 2},
        {"q": "The summary equation for photosynthesis is:", "opts": ["glucose + O2 → CO2 + H2O + energy", "CO2 + H2O + light → glucose + O2", "O2 + food → CO2 + water", "sunlight + O2 → glucose + H2O"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "Why are leaves often green?", "opts": ["they reflect red light", "chlorophyll reflects green light", "they absorb green light", "they have no pigment"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "During photosynthesis, plants absorb water through their ___.", "opts": ["leaves", "flowers", "roots", "stem only"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "Why do plants need sunlight?", "opts": ["to reproduce seeds", "to provide energy for photosynthesis", "to attract insects", "to produce carbon dioxide"], "ans": 1, "cat": "Science", "diff": 2},

        # diff 3 — chemical vs. physical changes (in depth)
        {"q": "Which is a sign of a chemical change?", "opts": ["melting", "dissolving in water", "production of a new gas or odor", "changing shape"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "Mixing vinegar and baking soda produces bubbles. This is a ___.", "opts": ["physical change", "chemical change", "state change", "simple mixture"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "Which is a physical change?", "opts": ["wood burning", "iron rusting", "sugar dissolving in water", "bread baking"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "Iron rusting is a ___ change.", "opts": ["physical", "chemical", "state", "mixture only"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "Which change is usually irreversible?", "opts": ["ice melting", "water evaporating", "wood burning", "salt dissolving"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "What do we call the starting materials in a chemical reaction?", "opts": ["products", "reactants", "compounds", "mixtures"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "What do we call the new substances formed in a chemical reaction?", "opts": ["reactants", "mixtures", "products", "elements"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "A chemical change that releases energy as heat and light is called ___.", "opts": ["dissolution", "condensation", "combustion", "filtration"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "What stays constant during both physical and chemical changes?", "opts": ["mass (Law of Conservation of Mass)", "color", "temperature", "state of matter"], "ans": 0, "cat": "Science", "diff": 3},
        {"q": "Photosynthesis is an example of a ___ change.", "opts": ["physical", "chemical", "state", "phase transition"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "Which evidence best suggests a chemical change occurred?", "opts": ["change in size", "gas produced, color change, and heat released", "change in shape only", "dissolving in liquid"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "What type of change occurs when you cut a piece of paper?", "opts": ["chemical change", "combustion", "physical change", "chemical reaction"], "ans": 2, "cat": "Science", "diff": 3},

        # diff 4 — forces and motion
        {"q": "What is a force?", "opts": ["a type of energy stored in objects", "a push or pull that causes changes in motion", "the speed of an object", "an object's weight"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "What is friction?", "opts": ["the force of gravity on an object", "a force that opposes motion between surfaces", "the acceleration of an object", "air resistance only"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "What is speed?", "opts": ["distance multiplied by time", "distance divided by time", "time divided by distance", "force multiplied by mass"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "What is acceleration?", "opts": ["constant speed", "a change in speed or direction", "the total distance traveled", "the force applied"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "What force pulls objects toward the center of the Earth?", "opts": ["friction", "magnetic force", "gravity", "tension"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "Given the same force, which object accelerates more?", "opts": ["the heavier one", "they are equal", "the lighter one", "neither moves"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "Newton's First Law of Motion is also called the law of ___.", "opts": ["acceleration", "action-reaction", "inertia", "gravity"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "Inertia means an object tends to ___.", "opts": ["fall to the ground", "stay at rest or keep moving unless a force acts on it", "speed up over time", "lose energy"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "10 N right and 6 N left act on an object. What is the net force?", "opts": ["4 N to the left", "16 N to the right", "4 N to the right", "0 N"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "Which force slows a falling parachute?", "opts": ["gravity", "friction", "air resistance", "magnetic force"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "A ball rolls on a surface and slows down. What force acts on it?", "opts": ["gravity pulling it up", "friction from the surface", "air pressure", "magnetism"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "Balanced forces are forces that cause ___.", "opts": ["acceleration", "speeding up", "no change in motion", "direction change only"], "ans": 2, "cat": "Science", "diff": 4},

        # diff 5 — ecosystems, human impact, and environmental science
        {"q": "What is the term for variety of living things in an ecosystem?", "opts": ["habitat", "food chain", "biodiversity", "population"], "ans": 2, "cat": "Science", "diff": 5},
        {"q": "How do humans most negatively impact ecosystems?", "opts": ["by planting more trees", "through pollution, deforestation, and overhunting", "by creating national parks", "by reducing plastic use"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "What is deforestation?", "opts": ["planting forests in new areas", "large-scale clearing of forest land", "a natural forest fire", "the growth of tree populations"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "In ecology, what is an organism's niche?", "opts": ["a type of habitat", "its role and way of life in the ecosystem", "the area where it lives", "a type of food chain"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "What is ecological succession?", "opts": ["migration of animals", "adaptation of a species", "gradual change in an ecosystem's species over time", "evolution of a single animal"], "ans": 2, "cat": "Science", "diff": 5},
        {"q": "What is a limiting factor in an ecosystem?", "opts": ["an organism that helps others", "a resource that limits population size", "a type of predator", "a chemical in soil only"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "What is the greenhouse effect?", "opts": ["plants growing in greenhouses", "heat from the sun trapped by atmospheric gases", "plants producing oxygen", "ocean cooling processes"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "Carbon dioxide is a ___ that traps heat in the atmosphere.", "opts": ["reactant in respiration only", "greenhouse gas", "gas that blocks sunlight", "substance that cools Earth"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "Sustainable resource use means ___.", "opts": ["using resources as fast as possible", "using resources without depleting them for future generations", "using only non-renewable resources", "cutting forests carefully"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "What is the carbon cycle?", "opts": ["a type of food chain", "movement of carbon through organisms, air, water, and soil", "the life cycle of carbon-based animals", "a chemical reaction in plants only"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "An invasive species harms an ecosystem by ___.", "opts": ["providing food for native species", "competing with and displacing native species", "cleaning polluted water", "helping native plants grow"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "What is the role of decomposers in an ecosystem?", "opts": ["to hunt prey", "to make food from sunlight", "to break down dead organisms and recycle nutrients", "to filter water"], "ans": 2, "cat": "Science", "diff": 5},
    ],

    # ── Grade 6 ──────────────────────────────────────────────────────────────
    6: [
        # diff 1 — cell organelles (detailed)
        {"q": "What is the endoplasmic reticulum's main function?", "opts": ["energy production", "transporting proteins and lipids within the cell", "controlling cell division", "storing DNA"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "What does the Golgi apparatus do?", "opts": ["produces energy", "processes and packages proteins for transport", "stores genetic information", "controls cell respiration"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "What is the function of lysosomes?", "opts": ["producing energy", "making proteins", "breaking down waste materials and cellular debris", "carrying oxygen"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "Which organelle is unique to plant cells and performs photosynthesis?", "opts": ["mitochondria", "ribosome", "chloroplast", "lysosome"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "Which organelle produces energy through cellular respiration?", "opts": ["nucleus", "chloroplast", "ribosome", "mitochondria"], "ans": 3, "cat": "Science", "diff": 1},
        {"q": "What is the function of the cell membrane?", "opts": ["to produce energy", "to control what enters and exits the cell", "to store genetic information", "to synthesize proteins"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "Where is DNA stored in a eukaryotic cell?", "opts": ["cytoplasm", "mitochondria", "nucleus", "ribosome"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "What do ribosomes do?", "opts": ["produce energy", "synthesize (build) proteins", "digest waste", "transport lipids"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "What is the main difference between eukaryotic and prokaryotic cells?", "opts": ["eukaryotes have DNA; prokaryotes do not", "eukaryotes have a membrane-bound nucleus; prokaryotes do not", "prokaryotes are larger", "prokaryotes have more organelles"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "What is the central vacuole's role in plant cells?", "opts": ["energy production", "DNA storage", "storing water and maintaining turgor pressure", "protein synthesis"], "ans": 2, "cat": "Science", "diff": 1},
        {"q": "Which structure gives plant cells their rigid shape?", "opts": ["cell membrane", "cell wall (made of cellulose)", "large vacuole", "chloroplast"], "ans": 1, "cat": "Science", "diff": 1},
        {"q": "The smooth ER is primarily responsible for ___.", "opts": ["protein synthesis", "lipid synthesis and detoxification", "packaging proteins for export", "storing DNA"], "ans": 1, "cat": "Science", "diff": 1},

        # diff 2 — genetics basics
        {"q": "What molecule carries genetic information in cells?", "opts": ["RNA only", "protein", "DNA", "glucose"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "What is a gene?", "opts": ["a type of cell", "a segment of DNA that codes for a specific trait", "a strand of protein", "a type of organelle"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "What is heredity?", "opts": ["the study of cells", "the passing of traits from parents to offspring", "the change of species over time", "the function of DNA"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "What are chromosomes?", "opts": ["structures made of proteins only", "structures in the nucleus that carry genes (DNA)", "organelles that produce energy", "cell membranes"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "What is a dominant trait?", "opts": ["expressed only when two copies are present", "always expressed when at least one copy is present", "a trait that skips generations", "a recessive trait"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "What is a recessive trait?", "opts": ["expressed with one copy", "always visible", "expressed only when two recessive alleles are present", "a dominant factor"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "What is an allele?", "opts": ["a type of cell", "one version of a gene", "a strand of RNA", "a type of chromosome"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "A person with two identical alleles for a trait is called ___.", "opts": ["heterozygous", "homozygous", "recessive", "dominant"], "ans": 1, "cat": "Science", "diff": 2},
        {"q": "A person with two different alleles for a trait is called ___.", "opts": ["homozygous", "recessive", "dominant", "heterozygous"], "ans": 3, "cat": "Science", "diff": 2},
        {"q": "Which scientist is known as the father of genetics?", "opts": ["Darwin", "Hooke", "Mendel", "Watson"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "If B = brown eyes (dominant) and b = blue, what is the eye color of genotype Bb?", "opts": ["blue", "green", "brown", "hazel"], "ans": 2, "cat": "Science", "diff": 2},
        {"q": "How many chromosomes are in a typical human body cell?", "opts": ["23", "46", "48", "22"], "ans": 1, "cat": "Science", "diff": 2},

        # diff 3 — chemical reactions (in depth)
        {"q": "What is a chemical equation?", "opts": ["a math formula for density", "a representation of a chemical reaction using symbols and formulas", "a recipe for mixing chemicals", "a diagram of an atom"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "In a balanced chemical equation, what must be equal on both sides?", "opts": ["the number of compounds", "the number of atoms of each element", "the volume of substances", "the temperature"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "What do we call a reaction that releases heat?", "opts": ["endothermic", "exothermic", "photosynthetic", "condensation"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "What do we call a reaction that absorbs heat from its surroundings?", "opts": ["exothermic", "combustion", "endothermic", "neutralization"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "What does the pH scale measure?", "opts": ["temperature", "density", "acidity or alkalinity of a solution", "electrical charge"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "A pH of 7 is considered ___.", "opts": ["acidic", "alkaline", "neutral", "basic"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "What is an acid?", "opts": ["a substance with pH greater than 7", "a substance with pH less than 7", "a neutral substance", "a substance with pH of exactly 7"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "What is a base/alkali?", "opts": ["a substance with pH less than 7", "a substance with pH greater than 7", "a neutral substance", "a substance that burns"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "What type of reaction occurs between an acid and a base?", "opts": ["combustion", "decomposition", "neutralization", "synthesis"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "What gas is produced when an acid reacts with a metal?", "opts": ["oxygen", "carbon dioxide", "hydrogen", "nitrogen"], "ans": 2, "cat": "Science", "diff": 3},
        {"q": "What is a catalyst?", "opts": ["a substance that slows reactions", "a substance that speeds up reactions without being consumed", "a product of a reaction", "a type of acid"], "ans": 1, "cat": "Science", "diff": 3},
        {"q": "Which represents a synthesis reaction?", "opts": ["AB → A + B", "A + BC → AC + B", "A + B → AB", "AB + CD → AD + CB"], "ans": 2, "cat": "Science", "diff": 3},

        # diff 4 — Newton's Laws (detailed application)
        {"q": "What does Newton's First Law state?", "opts": ["Force equals mass times acceleration", "For every action there is an equal and opposite reaction", "An object at rest stays at rest unless an unbalanced force acts on it", "Objects fall at the same rate regardless of mass"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "What does Newton's Second Law state?", "opts": ["Objects at rest stay at rest", "For every action there is an equal and opposite reaction", "Force equals mass times acceleration (F=ma)", "Gravity acts equally on all objects"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "What does Newton's Third Law state?", "opts": ["F = ma", "Objects in motion stay in motion", "For every action, there is an equal and opposite reaction", "Acceleration is inversely proportional to mass"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "Using F=ma, if mass = 5 kg and acceleration = 3 m/s², what is the force?", "opts": ["2 N", "8 N", "15 N", "0.6 N"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "A rocket launches by pushing exhaust gas downward. This illustrates Newton's ___ law.", "opts": ["first", "second", "third", "zero"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "Two objects receive the same force. Which accelerates more?", "opts": ["the heavier one", "they are equal", "the lighter one", "neither moves"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "If force doubles and mass stays constant, acceleration ___.", "opts": ["is halved", "stays the same", "doubles", "is quadrupled"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "What is momentum?", "opts": ["force divided by mass", "mass times velocity", "acceleration times time", "force times distance"], "ans": 1, "cat": "Science", "diff": 4},
        {"q": "A ball bouncing off a wall illustrates Newton's ___ law.", "opts": ["first", "second", "third", "gravitational"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "What is the SI unit of force?", "opts": ["kilogram", "joule", "newton", "watt"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "A 10 kg object accelerates at 2 m/s². What force is applied? (F=ma)", "opts": ["5 N", "12 N", "20 N", "0.2 N"], "ans": 2, "cat": "Science", "diff": 4},
        {"q": "In physics, work equals ___.", "opts": ["force in any direction times time", "force times distance in the direction of force", "mass times acceleration", "power divided by time"], "ans": 1, "cat": "Science", "diff": 4},

        # diff 5 — Earth and space science (advanced)
        {"q": "What is the Sun classified as?", "opts": ["a planet", "a moon", "a star", "a comet"], "ans": 2, "cat": "Science", "diff": 5},
        {"q": "What force keeps planets in orbit around the Sun?", "opts": ["magnetism", "friction", "gravity", "electrical force"], "ans": 2, "cat": "Science", "diff": 5},
        {"q": "What is the correct order of the first four planets from the Sun?", "opts": ["Mercury, Venus, Earth, Mars", "Venus, Mercury, Earth, Mars", "Earth, Mercury, Venus, Mars", "Mars, Earth, Venus, Mercury"], "ans": 0, "cat": "Science", "diff": 5},
        {"q": "What is a light year?", "opts": ["the time Earth takes to orbit the Sun", "the distance light travels in one year", "the brightness of a star", "the speed of a planet"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "What is a galaxy?", "opts": ["a system of planets", "a cloud of gas in space", "a vast system of stars, gas, and dust held together by gravity", "a type of nebula"], "ans": 2, "cat": "Science", "diff": 5},
        {"q": "Our solar system is in the ___ galaxy.", "opts": ["Andromeda", "Triangulum", "Milky Way", "Whirlpool"], "ans": 2, "cat": "Science", "diff": 5},
        {"q": "What is a black hole?", "opts": ["a dark space with no stars", "a region with gravity so strong nothing can escape, not even light", "a cold dead planet", "a type of dark nebula"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "What is the Big Bang Theory?", "opts": ["Earth formed from a collision", "the universe began from an extremely hot, dense point ~13.8 billion years ago", "stars explode to form new planets", "galaxies rotate around black holes"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "Rocky, icy objects orbiting the Sun with tails of gas are called ___.", "opts": ["asteroids", "meteors", "comets", "moons"], "ans": 2, "cat": "Science", "diff": 5},
        {"q": "What determines the color of a star?", "opts": ["its size", "its distance from Earth", "its surface temperature", "its age only"], "ans": 2, "cat": "Science", "diff": 5},
        {"q": "What is a nebula?", "opts": ["a type of planet", "a cloud of gas and dust in space where stars form", "a dead star", "a type of comet"], "ans": 1, "cat": "Science", "diff": 5},
        {"q": "The outer planets (Jupiter, Saturn, Uranus, Neptune) are called ___.", "opts": ["terrestrial planets", "rocky planets", "gas giants", "dwarf planets"], "ans": 2, "cat": "Science", "diff": 5},
    ],
}

# ─── Uhyun secret-stage questions (factorial math) ──────────────────────────
UHYUN_QS = [
    {
        "q":    "Factor:  2x^3 - 3x^2 + 6x - 9",
        "opts": ["(2x-3)(x^2+3)", "(x-3)(2x^2+3)", "(2x+3)(x^2-3)", "Prime"],
        "ans":  0,
    },
    {
        "q":    "Factor:  x^3*y - x^2*y^2 + x - y",
        "opts": ["(x+y)(x^2*y+1)", "(x-y)(x^2*y+1)", "(x-y)(x^2*y-1)", "x*y(x-y)"],
        "ans":  1,
    },
    {
        "q":    "Factor:  (a^2+b^2-c^2)^2 - 4a^2*b^2",
        "opts": ["(a-b-c)(a-b+c)(a+b-c)(a+b+c)", "(a^2-b^2-c^2)^2", "(a+b-c)^2", "Prime"],
        "ans":  0,
    },
    {
        "q":    "Factor:  5x^2 + 2x(y+1) - 3(y+1)^2",
        "opts": ["(5x+3y+3)(x-y-1)", "(5x-3y-3)(x+y+1)", "(5x-3)(x+y)", "Prime"],
        "ans":  1,
    },
    {
        "q":    "Factor:  x^6 - 7x^3 - 8",
        "opts": ["(x^3-8)(x^3+1)", "(x^3+8)(x^3-1)", "(x^2-7)(x^4+8)", "Prime"],
        "ans":  0,
    },
]

# ─── Bonus round questions ──────────────────────────────────────────────────
BONUS_POOL = [
    {"q": "Unscramble: E-L-P-P-A",            "opts": ["APPLE", "PAPER", "PANEL"],                             "ans": 0},
    {"q": "Next in sequence: 2, 4, 6, 8, ?",  "opts": ["9", "10", "12"],                                       "ans": 1},
    {"q": "The sun ___ in the east.",          "opts": ["sets", "rises", "falls"],                              "ans": 1},
    {"q": "7 x 7 + 1 = ?",                    "opts": ["48", "50", "56"],                                      "ans": 1},
    {"q": "Antonym of 'brave':",               "opts": ["Bold", "Cowardly", "Strong"],                          "ans": 1},
    {"q": "Fix: 'She don't know.'",            "opts": ["She doesn't know.", "She not know.", "She no know."],   "ans": 0},
    {"q": "Largest planet in our solar system?", "opts": ["Earth", "Saturn", "Jupiter"],                        "ans": 2},
    {"q": "Unscramble: R-D-I-F-E-N",           "opts": ["FINDER", "FRIEND", "FRIDGE"],                         "ans": 1},
]

# ─── Per-level door/key configuration ───────────────────────────────────────
LEVEL_CFG = {
    1: {"locked": [],        "keys": []},
    2: {"locked": [],        "keys": []},
    3: {"locked": [],        "keys": []},
    4: {"locked": [1],       "keys": [(400, 320, 1)]},
    5: {"locked": [1, 3],    "keys": [(350, 290, 1), (760, 420, 3)]},
    6: {"locked": [1, 2, 3], "keys": [(300, 290, 1), (590, 430, 2), (770, 290, 3)]},
}

# ─── Subject pool lookup ────────────────────────────────────────────────────
_SUBJECT_POOL = {
    1: GRAMMAR_QS,
    2: VOCAB_QS,
    3: SCIENCE_QS,
}


def get_door_question(door_num: int, grade: int,
                      stage: int = 1, used_ids: set = None) -> dict:
    """Return a question for *door_num* matching *grade* and *stage* difficulty.

    Questions at the current stage difficulty are preferred; if none are fresh
    the pool falls back to any question for the grade.  Chosen question ids are
    added to *used_ids* so they won't repeat in the same run.
    """
    import random
    pool = _SUBJECT_POOL.get(door_num, GRAMMAR_QS)
    grade_qs = pool.get(min(max(grade, 1), 6), [])
    diff = min(max(stage, 1), 5)
    eligible = [q for q in grade_qs if q.get("diff", 3) == diff]
    if not eligible:
        eligible = list(grade_qs)
    if used_ids:
        fresh = [q for q in eligible if id(q) not in used_ids]
        if fresh:
            eligible = fresh
    chosen = random.choice(eligible)
    if used_ids is not None:
        used_ids.add(id(chosen))
    return chosen
