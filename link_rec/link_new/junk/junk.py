def parse(filename):
    f = open(filename)
    lines = f.readlines()
    lines = [line.replace('\n', '').split() for line in lines]
    lines = [line[1:-1] for line in lines]
    # i = lines.index(['Data', 'Analytics', 'Chief', 'Scientist'])
    # y = lines.index(['Statistical', 'Clerk'])
    # z = lines.index(['Research', 'Analyst'])
    # for line in lines[:i]:
    #     line.append('software')
    # for line in lines[i:z]:
    #     line.append('data')
    # for line in lines[z:]:
    #     line.append('research')

    with open('experience_classification', 'a') as b:
        for line in lines:
            z = ' '.join(line[:-1])
            label = ''.join(line[-1])
            b.write(z + ', ' + label + '\n')

    with open(filename, 'w'):
        pass

# if __name__ == '__main__':
    # parse('random')



# def trainingSet_applyFreqSelection(data, labels):
#     """
#     """
#     split_category = t.split_atrributes_category(data, labels)
#     best_feature_category = t.frequency_based_feature(split_category)
#     new_data = []
#     new_label = []
#     for i in best_feature_category:
#         category_list = split_category.get(i)
#         for w in category_list:
#             z = [y for y in w if y in best_feature_category[i]]
#             if len(z) == 0: # ASSUMPTION: If none, assume that it is 'other' (actually is most of the time..)
#                 z = [best_feature_category.get('other')[0]]
#             new_data.append(z)
#             new_label.append(i)
#     return new_data, new_label
#
# def applyFreqSelection(test_data, data, labels):
#     """
#     """
#     split_category = t.split_atrributes_category(data, labels)
#     best_feature_category = t.frequency_based_feature(split_category)
#     set_best_words = [y.lower() for i in best_feature_category for y in set(best_feature_category[i])]
#     new_data = []
#     for w in test_data:
#         x = [y for y in w if y in set_best_words]
#         if len(x) == 0:  # ASSUMPTION: If none, assume that it is 'other' (actually is most of the time..)
#             x = [best_feature_category.get('other')[0]]
#         new_data.append(x)
#     return new_data
#
# def trainingSet_classification(clean_attributes, clean_labels, k=3):
#     """
#     """
#     vocabSet = c.vocabSet(clean_attributes)
#     bagOfWords = [c.bag_of_words(vocabSet, i) for i in clean_attributes]
#     errCount = 0
#     for i in range(len(bagOfWords)):
#         x = classify(np.array(bagOfWords[i]), np.array(bagOfWords), clean_labels, k)
#         print(clean_attributes[i], x, clean_labels[i])
#         if x != clean_labels[i]: errCount += 1
#     return (errCount / len(bagOfWords)) * 100
#
# def classification(clean_test_data, clean_attributes, clean_labels, k=3):
#     """
#     """
#     vocabSet = c.vocabSet(clean_attributes)
#     vocabSet = [i.lower() for i in vocabSet]
#     bagOfWords = [c.bag_of_words(vocabSet, i) for i in clean_test_data]
#     tBg = [c.bag_of_words(vocabSet, i) for i in clean_attributes]
#     errCount = 0
#     for i in range(len(bagOfWords)):
#         x = classify(np.array(bagOfWords[i]), np.array(tBg), clean_labels, k)
#         print(clean_test_data[i], x)
#         if x != clean_labels[i]: errCount += 1
#     return (errCount / len(bagOfWords)) * 100
#
# if __name__ == '__main__':
#     t = TextProcessing()
#     c = CosineSimilarity()
#
#     data, labels = trainSet_cleanFile('experience_classification')
#     # stemmed_data = [t.stem(row) for row in data]
#     new_data, new_labels = trainingSet_applyFreqSelection(data, labels)
#     # for i in range(len(new_data)):
#     #     print(new_data[i], new_labels[i])
#     # print(trainingSet_classification(new_data, new_labels))
#
#     test_data = cleanFile('experience_unclassified')
#     new_test_data = applyFreqSelection(test_data, new_data, new_labels)
#     # for i in range(len(new_test_data)):
#     #     print(test_data[i], new_test_data[i])
#     classification(new_test_data, new_data, new_labels)