from cosine_similarity import CosineSimilarity
from preprocess_text import TextProcessing
from file_handler import FileProcessor
import numpy as np
from kNN import classify

########################################
    # kNN Model-Based Classifier:
########################################

# TODO: Make sure to fix all the Docstrings!
# TODO: model construction is really inefficient...
# TODO: Right now, seems like an overfitting issue, won't work well for randomized cases; need to have more categories
# TODO: Will user be allowed to add categories?
    # TODO: how will this be affected when there are more categories? <-- Something to think about later?


def model_construction(data, global_words, sorted_neighbours):
    """
    Defines all the data points as representatives of each category (using global and general instances)
    There are no Disjoint sets returned
    Parameters: -
    """
    generalized_instance = []
    for i in sorted_neighbours:
        x = sorted_local_neighbours[i]
        y = [i for i in x if i[1]>=2]
        y = sorted(y, key=lambda x: x[1], reverse=True)
        generalized_instance.append(y)

    g = [y for i in generalized_instance for y in i]
    g_dict = {}
    for i in g:
        g_dict[i[0]] = i[1]

    words = [i[0] for i in g]

    new_data = []
    for row in data:
        y = [word for word in row if word in global_words] # global representatives
        if len(y) == 0: # go to next representative word in generalized instance
            y = [w for w in row if w in words]
            if len(y) != 0:
                s = [g_dict.get(i) for i in y]
                max_values = [i for i in s if i > 2]
                if len(max_values) != 0:
                    indexes = [s.index(max_value) for max_value in max_values]
                    y = [y[index] for index in indexes]

            elif len(y) == 0: # default other
                y = ['electrical'] # TODO: other global rep shouldn't be hardcoded like this
        new_data.append(y)

    return new_data

def training_classification(data, label, bagOfWords, k=3):
    """
    kNN Model Based Classifier for the Training Set data;
    Parameters: -
    """
    errCount = 0
    for i in range(len(bagOfWords)):
        x = classify(np.array(bagOfWords[i]), np.array(bagOfWords), label, k)
        # print(data[i], x, label[i])
        if x != label[i]:
            errCount += 1
            print(data[i], x, label[i])
    return (errCount / len(bagOfWords)) * 100

def classification(test_data, test_bagOfWords, original_data, original_labels, original_bagOfWords, k=3):
    """
    kNN Model Based Classifier for test data (actual data)
    """
    for i in range(len(test_bagOfWords)):
        x = classify(np.array(test_bagOfWords[i]), np.array(original_bagOfWords), original_labels, k)
        print(test_data[i], x)

if __name__ == '__main__':
    c = CosineSimilarity()
    t = TextProcessing()
    f = FileProcessor('experience_classification', 'train')
    data, label = f.cleanFile()
    feature_in_category = t.get_feature_in_category(data, label)
    local_neighbour = t.get_local_neighbours(feature_in_category)
    global_neighbour = t.get_global_neighbours(feature_in_category)
    global_words = [global_neighbour[i][0] for i in global_neighbour]
    sorted_local_neighbours = t.get_local_neighbours_sorted(feature_in_category)
    # for i in sorted_local_neighbours:
    #     print(sorted_local_neighbours[i])

    ## Training Data: 4-6%
    revised_data = model_construction(data, global_words, sorted_local_neighbours)
    # for i in revised_data:
    #     print(i)
    vocabSet = c.vocabSet(revised_data)
    bagOfWords = [c.bag_of_words(vocabSet, i) for i in revised_data]
    # print(training_classification(revised_data, label, bagOfWords, k=3))

    ## Test Data: 4-6%
    test_file = FileProcessor('experience_unclassified', 'test')
    test_data = test_file.cleanFile()
    revised_test_data = model_construction(test_data, global_words, sorted_local_neighbours)
    # test_vocabSet = c.vocabSet(revised_data)
    test_bagOfWords = [c.bag_of_words(vocabSet, i) for i in revised_test_data] # the test bag of words still uses original vocabset
    # print(classification(revised_test_data, test_bagOfWords, revised_data, label, bagOfWords))

