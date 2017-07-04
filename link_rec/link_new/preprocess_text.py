import string, operator
from nltk.stem import *
from cosine_similarity import CosineSimilarity

#################################################################################################################
        # Text Processing for handling simple and general pre-processing and feature selection;
#################################################################################################################

# from bs4 import BeautifulSoup
# from urllib.request import urlopen
# def parse_stop_words():
#     """
#     Function used to parse majority of stop words off http://www.lextek.com/manuals/onix/stopwords1.html
#     Stop Words are now written in a txt file: 'stop_words'
#     (shouldn't be used again...)
#     """
#     url = 'http://www.lextek.com/manuals/onix/stopwords1.html'
#     soup = BeautifulSoup(urlopen(url))
#     stop_words = soup.find('pre').text.split()
#     stop_words = [i for i in stop_words if i != '#']
#     with open('stop_words', 'a') as f:
#         for word in stop_words:
#             f.write(word + '\n')

# parse_stop_words()


class TextProcessing(object):
    """
    Does Basic Text Processing (tokenize, stop words, punctuation) and some feature selection for text categorization
    """

    def __init__(self):
        f = open('/Users/Rahul/Desktop/Main/Side_projects/project_2/lifeline/Scripts/link_new/stop_words')
        lines = f.readlines()
        self.translator = str.maketrans('', '', string.punctuation)
        self.stop_words = [line.replace('\n', '').lower().translate(self.translator) for line in lines]

    def lower_text_in_list(self, data):
        """
        Return a list with lowered text
        """
        assert type(data) == list
        return [word.lower() for word in data]

    def tokenize(self, line):
        """
        Tokenize's a line
        """
        return line.split()

    def remove_stop_words_list(self, data):
        """
        Remove's all common stop words from a list
        """
        assert type(data) == list
        return [i for i in data if i not in self.stop_words]

    def remove_stop_words_line(self, line):
        """
        Remove's all common stop words from a sentence
        """
        line = self.tokenize(line)
        return self.remove_stop_words_list(line)

    def remove_punctuation_list(self, data):
        """
        Remove's punctuation from a list: Handles 1D and 2D list
        """
        assert type(data) == list
        # return (row.translate(self.translator) for row in data)
        try:
            for row in data:
                assert type(row) == str
            return [row.translate(self.translator) for row in data]
        except:
            for row in data:
                assert type(row) == list
            return [y.translate(self.translator) for row in data for y in row]

    def remove_punctuation_line(self, line):
        """
        Remove's punctuation from a line
        """
        line = self.tokenize(line)
        return self.remove_punctuation_list(line)

    def stem(self, data):
        """
        Word Stemming, ex: labeling --> label, introduction --> introduct
        """
        stemmer = PorterStemmer()
        return [stemmer.stem(plural) for plural in data]

    # TODO: Need to do this...
    def csvFile_to_text(self):
        """Converts a CSV File to a txt file first """
        pass

    # def __all_categories(self, lines):
    #     """
    #     Return's a list of all the different categories exists for the text classification problem
    #     Assumption: the last word in a line is the class label
    #     Parameter: -filename should be a txt file
    #     """
    #     labels = []
    #     for line in lines:
    #         line = line.replace('\n', '')
    #         line = self.tokenize(line)
    #         line = self.remove_punctuation_line(line[-1])
    #         for i in line:
    #             labels.append(i)
    #     return labels
    #
    # def __all_training(self, lines):
    #     """
    #     Returns list of all the feature's
    #     """
    #     data = []
    #     for line in lines:
    #         line = line.replace('\n', '')
    #         line = self.tokenize(line)
    #         line = [line[:-1]]
    #         line = self.remove_punctuation_list(line)
    #         for i in line:
    #             data.append(i)
    #     data = [self.remove_stop_words_list(i) for i in data]
    #     return data

    def get_feature_in_category(self, data, label):
        """
        """
        category_di = {}
        set_category = list(set(label))
        for category in set_category:
            li = []
            for i in range(len(label)):
                if category == label[i]:
                    li.append(data[i])
                    category_di[label[i]] = li
        return category_di

    def count_for_1D(self, data):
        """ Return's a dict with key (item) and number of times it appears in 1D list """
        assert type(data) == list
        main_di = {}
        for i in data:
            if i in main_di:
                main_di[i] += 1
            else:
                main_di[i] = 1
        return main_di

    def count_for_2D(self, data):
        """ Return's a dict with key (item) and number of times it appears in 2D list """
        assert type(data) == list
        main_di = {}
        for i in data:
            assert type(data) == list
            for y in i:
                if y in main_di:
                    main_di[y] += 1
                else:
                    main_di[y] = 1
        return main_di

    def get_local_neighbours(self, data):
        """
        Return's the most frequent used words in each class; (def: frequent > 1...)
        Parameter: -data: should be dict from get_feature_in_category
        """
        assert type(data) == dict
        max_words = {}
        for i in data:
            c = []
            y = self.count_for_2D(data.get(i))
            for z in y:
                if y[z] > 1:
                    c.append(z)
            max_words[i] = c
        return max_words

    def get_local_neighbours_sorted(self, data):
        """
        Return's Dict of list's with sorted (highest to lowest) local neighbours in each category
        """
        assert type(data) == dict
        max_words = {}
        for i in data:
            y = self.count_for_2D(data.get(i))
            sorted_y = sorted(y.items(), key=operator.itemgetter(1), reverse=True)
            max_words[i] = sorted_y
        return max_words

    def get_global_neighbours(self, data):
        """
        Return's the most frequent used word in each class; (word with highest frequency)
        Parameter: -data: should be dict from get_feature_in_category
        """
        assert type(data) == dict
        global_words = {}
        for i in data:
            y = self.count_for_2D(data.get(i))
            max_word = max(y.items(), key=operator.itemgetter(1))
            global_words[i] = max_word
        return global_words

    # TODO: helper functions to add the feature selection should be here...

    def entropy(self):
        """ Calculation of entropy """
        pass

    def information_gain(self, data):
        """ Calculation of information gain """
        assert type(data) == list

# if __name__ == '__main__':
    ### Just testing it to make sure it works
    # t = TextProcessing()
    # c = CosineSimilarity()
    # test_list = ["Free;s's", 'Lower!.', 'BS!!;][', 'and', 'of']
    # test_sentence = 'They! refuse, to/ permit[])_ us-- to. obtain the refuse permit'
    # t.lower_text_in_list(test_list)
    # t.tokenize(test_sentence)
    # t.remove_stop_words_list(test_list)
    # t.remove_punctuation_list(test_list)
    # t.remove_stop_words_line(test_sentence)
    # t.remove_punctuation_line(test_sentence)
    # plurals = ['caresses', 'flies', 'dies', 'mules', 'denied', 'died', 'agreed', 'owned', 'humbled', 'sized',
    #         'meeting', 'stating', 'siezing', 'itemization', 'sensational', 'traditional', 'reference', 'colonizer',
    #         'plotted']
    # t.stem(plurals)

