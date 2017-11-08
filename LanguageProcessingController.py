from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

class LanguageProcessingController:

    def __init__(self, text):
        # Input text is a string
        self.text = word_tokenize(text)
        self.filter_stopwords()
        self.tag_data = self.parts_of_speech_tag()

    def filter_stopwords(self):
        """Filter text using default stopwords"""
        stop_words = set(stopwords.words("english"))
        filtered_sentence = [w for w in self.text if w not in stop_words]
        self.text = filtered_sentence

    def parts_of_speech_tag(self):
        """Label text with parts of speech"""
        try:
            tagged = nltk.pos_tag(self.text)
            return tagged
        except Exception as e:
            print(str(e))

LPC = LanguageProcessingController("There was a dog that use to play games. Blah you now")
chunkGram = r"""Chunk: {<VB.?>*<NN.?>*}"""
chunkParser = nltk.RegexpParser(chunkGram)
chunked = chunkParser.parse(LPC.tag_data)
chunked.draw()


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

