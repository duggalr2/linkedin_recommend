

def tuple_append(lst):
    start = 0
    while start < len(lst):
        new_index = start
        while new_index < len(lst):
            if lst[start][0] == lst[new_index][0]:
                if lst[start][1] != lst[new_index][1]:
                    lst[start].append(lst[new_index][1])
                    del lst[new_index]
                    new_index -= 1
            new_index += 1
        start += 1


# if __name__ == "__main__":
#     lines = open('job_classified').readlines()
#     lines = [line.replace('\n', '') for line in lines]
#     job_list, job_class, big_list = [], [], []
#     test = []
#     for line in lines:
#         new_line = line.split(', ')
#         if len(new_line) == 1:
#             test.append(new_line[0])
#         else:
#             job_class.append(new_line[-1])
#             job_list.append(new_line[:-1])
#             big_list.append(list((' '.join(new_line[:-1]), new_line[-1])))
#
#     print(big_list)
#     tuple_append(big_list)
#     for i in big_list:
#         print(i)