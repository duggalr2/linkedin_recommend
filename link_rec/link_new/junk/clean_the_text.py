import string

############################################################################################
        # Remove's filler words and additional words based on the problem
############################################################################################

# translator = str.maketrans('', '', string.punctuation)

# TODO: Removing integers...
# TODO: Remove the chinese characters...

# def remove_filler_words(li, problem_type=None):
#     """
#     Remove's all filler words
#     Parameter: -li: parameter should be 1D list
#                -Problem_type: If Linkedin/Book, if None, will do common stop words only
#     """
#     book_stop_words = [] # TODO: fix this...
#     stop_words = ['degree', 'name', 'field', 'of', 'study', 'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for',
#                   'from', 'has', 'he', 'in', 'is', 'it', 'its', 'if', 'of', 'on', 'that', 'the', 'to', 'was', 'were',
#                   'where', 'will', 'with', 'llc', 'edition', 'grade', 'cgpa', 'gpa', 'cumulative', 'ltd', 'inc', 'itg',
#                   '(', ')', '-', '&', '|', '’', '--', 'grade', 'bcs', 'phd', 'coop']
#     # symbol = [':', '.', '(', ')', ',', '-', '&', '|', '’']
#     new_list = [i.lower().split() for i in li]
#     new_list = [y for i in new_list for y in i]
#     new_list = [i.translate(translator) for i in new_list]
#     new_list = [i for i in new_list if i not in stop_words and len(i) > 2 and i.isdigit() != True]
#     for i in new_list:
#         yield i
#
# def convert_key(items_dict, key):
#     """
#     Convert's specificed key to clean format for cosine similarity; Returns 1D list with words removing stop words, etc.;
#     Remove's url from the key if present
#     Parameter: -key: default is set to header, if key doesn't exist in dict, return's empty list
#     """
#     key_list = []
#     for i in items_dict:
#         y = i.get(key)
#         if key == 'header':
#             y = [y[1]] # TODO: what if the second one is not the header info or what if it's a url/name...
#         if y != None:
#             z = remove_filler_words(y)
#             for w in z:
#                 key_list.append(w)
#     return key_list
