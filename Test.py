# coding=UTF-8

import nltk

from nltk.corpus import brown



# This is a fast and simple noun phrase extractor (based on NLTK)

# Feel free to use it, just keep a link back to this post

# http://thetokenizer.com/2013/05/09/efficient-way-to-extract-the-main-topics-of-a-sentence/

# Create by Shlomi Babluki

# May, 2013





# This is our fast Part of Speech tagger

#############################################################################

brown_train = brown.tagged_sents(categories='news')

regexp_tagger = nltk.RegexpTagger(

    [(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),

     (r'(-|:|;)$', ':'),

     (r'\'*$', 'MD'),

     (r'(The|the|A|a|An|an)$', 'AT'),

     (r'.*able$', 'JJ'),

     (r'^[A-Z].*$', 'NNP'),

     (r'.*ness$', 'NN'),

     (r'.*ly$', 'RB'),

     (r'.*s$', 'NNS'),

     (r'.*ing$', 'VBG'),

     (r'.*ed$', 'VBD'),

     (r'.*', 'NN')

])

unigram_tagger = nltk.UnigramTagger(brown_train, backoff=regexp_tagger)

bigram_tagger = nltk.BigramTagger(brown_train, backoff=unigram_tagger)

#############################################################################





# This is our semi-CFG; Extend it according to your own needs

#############################################################################

cfg = {}

cfg["NNP+NNP"] = "NNP"

cfg["NN+NN"] = "NNI"

cfg["NNI+NN"] = "NNI"

cfg["JJ+JJ"] = "JJ"

cfg["JJ+NN"] = "NNI"

#############################################################################





class NPExtractor(object):



    def __init__(self, sentence):

        self.sentence = sentence



    # Split the sentence into singlw words/tokens

    def tokenize_sentence(self, sentence):

        tokens = nltk.word_tokenize(sentence)

        return tokens



    # Normalize brown corpus' tags ("NN", "NN-PL", "NNS" > "NN")

    def normalize_tags(self, tagged):

        n_tagged = []

        for t in tagged:

            if t[1] == "NP-TL" or t[1] == "NP":

                n_tagged.append((t[0], "NNP"))

                continue

            if t[1].endswith("-TL"):

                n_tagged.append((t[0], t[1][:-3]))

                continue

            if t[1].endswith("S"):

                n_tagged.append((t[0], t[1][:-1]))

                continue

            n_tagged.append((t[0], t[1]))

        return n_tagged



    # Extract the main topics from the sentence

    def extract(self):



        tokens = self.tokenize_sentence(self.sentence)

        tags = self.normalize_tags(bigram_tagger.tag(tokens))



        merge = True

        while merge:

            merge = False

            for x in range(0, len(tags) - 1):

                t1 = tags[x]

                t2 = tags[x + 1]

                key = "%s+%s" % (t1[1], t2[1])

                value = cfg.get(key, '')

                if value:

                    merge = True

                    tags.pop(x)

                    tags.pop(x)

                    match = "%s %s" % (t1[0], t2[0])

                    pos = value

                    tags.insert(x, (match, pos))

                    break



        matches = []

        for t in tags:

            if t[1] == "NNP" or t[1] == "NNI":

            #if t[1] == "NNP" or t[1] == "NNI" or t[1] == "NN":

                matches.append(t[0])

        return matches





# Main method, just run "python np_extractor.py"

def main():



    sentence = "phrase analysis pycharm method may be static python class webcachev01.dat viewer webcachev01.dat database webcachev01.dat database how to open .dat file database how to open .dat file can't find webcache directory can't find webcache directory microsoft edge history database location microsoft edge cache folder location edge browser history file location edge browser history file location edge browser history file location key to encrypt edge history where does internet edge store history database where does internet edge store history when to reject null hypothesis t value when to reject null hypothesis monster hunter world wallpaper monster hunter wallpaper nintendo wallpaper nintendo wallpaper box whisker plot creator box whisker plot standard deviation from mean normal distribution values equation for attraction between masses hole through the earth tunnel through earth simple harmonic motion radius of earth in meters radius of earth gravity hole through earth nike adidas abject meaning war steel and germs http://scikit-learn.org/stable/modules/generated/sklearn.cluster.kmeans.html website categorization database how to categorize a website? machine learning how to categorize websites how to cluster websites tfidfvectorizer example python if idf python if idf k means clustering sklearn automatic web-page classification by using machine learning methods tsukada automatic web-page classification by using machine learning methods how to categorize websites through machine learning how to categorize websites through machine learning how to categorize websites through machine learnign tunnel through earth simple harmonic motion how is density calculated what is density drill hole through earth gravity is gravity stronger the closer you are to the center of the earth is gravity from the center of the earth cluster browsing history python sql like multiple sql like  sql in sql like keyword id in keyword_search_items google history database keyword id how to cluster websites based on content how tocluster websites based on content jimmy kimmel k means clustering for websites how to cluster websites analyze browsing history content python analyze browsing history content python analyze browsing history python trend analyze browsing history python analyze browsing history wingstop sites like facebook sites like facebook web scraping on a topic web scraping on a topic foundation girogio armani foundation georgia armani amz thor ragnarok silver spoon pig pokémon the movie: i choose you! trinity seven the movie: eternity library and alchemic girl 2017 blame! 2017 pretty cure dream stars! fate/kaleid liner prisma illya: oath under snow pokémon the movie: i choose you! kuroko's basketball: last game digimon adventure tri. 4 the irregular at magic high school the movie: the girl who calls the stars fate/stay night: heaven's feel mary and the witch's flower fate/stay night: heaven's feel best anime of 2017 nelson fastfoward internship simpsons he's already dead quote simpsons he's already dead quote simpsons he's already dead what is a period math what is a period weather in conway "

    np_extractor = NPExtractor(sentence)

    result = np_extractor.extract()

    print ("This sentence is about: %s" % ", ".join(result))



if __name__ == '__main__':

    main()