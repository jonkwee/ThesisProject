from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
import nltk

class LanguageProcessingController:

    def __init__(self, textlist):
        # Input text is a list of strings in a list
        self.textlist = textlist
        self.text = ""
        self.count_words = defaultdict(int)

        self.processed = self.process_list_of_text()
        self.chunked = self.chunking(self.parts_of_speech_tag())
        #self.tag_data = self.parts_of_speech_tag()

    def change_text(self, text):
        self.text = text

    def process_list_of_text(self):
        """Return list of text without stopwords and as tokens"""
        returnable_array = []
        for e in self.textlist:
            self.change_text(word_tokenize(e[0]))
            self.filter_stopwords()
            for w in self.text:
                self.count_words[w] += 1
            returnable_array.append(self.text)
        return returnable_array

    def filter_stopwords(self):
        """Filter text using default stopwords"""
        stop_words = set(stopwords.words("english"))
        filtered_sentence = [w for w in self.text if w not in stop_words]
        self.text = filtered_sentence

    def parts_of_speech_tag(self):
        """Label text with parts of speech"""
        returnable_array = []
        try:
            for e in self.processed:
                tagged = nltk.pos_tag(e)
                returnable_array.append(tagged)
        except Exception as e:
            print(str(e))
        finally:
            return returnable_array

    def chunking(self, POSarray):
        """Chunk text based on parts of speech"""
        returnable_array = []
        chunkGram = r"""C: {<VB.?>*<NN.?>*}"""
        chunkParser = nltk.RegexpParser(chunkGram)
        for e in POSarray:
            returnable_array.append(chunkParser.parse(e))
        return returnable_array


# LPC = LanguageProcessingController("There was a dog that use to play games. Blah you now")
# print(LPC.chunking())


# CC	coordinating conjunction
# CD	cardinal digit
# DT	determiner
# EX	existential there (like: "there is" ... think of it like "there exists")
# FW	foreign word
# IN	preposition/subordinating conjunction
# JJ	adjective	'big'
# JJR	adjective, comparative	'bigger'
# JJS	adjective, superlative	'biggest'
# LS	list marker	1)
# MD	modal	could, will
# NN	noun, singular 'desk'
# NNS	noun plural	'desks'
# NNP	proper noun, singular	'Harrison'
# NNPS	proper noun, plural	'Americans'
# PDT	predeterminer	'all the kids'
# POS	possessive ending	parent's
# PRP	personal pronoun	I, he, she
# PRP$	possessive pronoun	my, his, hers
# RB	adverb	very, silently,
# RBR	adverb, comparative	better
# RBS	adverb, superlative	best
# RP	particle	give up
# TO	to	go 'to' the store.
# UH	interjection	errrrrrrrm
# VB	verb, base form	take
# VBD	verb, past tense	took
# VBG	verb, gerund/present participle	taking
# VBN	verb, past participle	taken
# VBP	verb, sing. present, non-3d	take
# VBZ	verb, 3rd person sing. present	takes
# WDT	wh-determiner	which
# WP	wh-pronoun	who, what
# WP$	possessive wh-pronoun	whose
# WRB	wh-abverb	where, when

