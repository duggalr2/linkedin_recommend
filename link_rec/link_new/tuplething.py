

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


def searchBS(big_list):
    start_index = 0
    # end_index = len(big_list)
    new_end_index = 1
    new_big_list = [list(i) for i in big_list]

    while start_index < new_end_index:

        new_end_index = len(new_big_list)
        duplicate = []

        for index in range(start_index, new_end_index):
            item = new_big_list[index]
            if item[0] == new_big_list[start_index][0] and item[-1] != new_big_list[start_index][
                -1] and index != start_index:
                new_big_list[start_index].append(item[-1])
                duplicate.append(new_big_list[index])

        for item in duplicate:
            i = new_big_list.index(item)
            del new_big_list[i]

        start_index += 1
    return new_big_list

if __name__ == "__main__":
    # lst = [[1,1], [2,2], [3,3], [1,2], [2,3], [4,5]]
    # print(lst)
    # tuple_append(lst)
    # print(lst)
    lines = open('job_classified').readlines()
    lines = [line.replace('\n', '') for line in lines]
    job_list, job_class, big_list = [], [], []
    for line in lines:
        new_line = line.split(', ')
        job_class.append([new_line[-1]])
        job_list.append(new_line[:-1])
        big_list.append((new_line[:-1], new_line[-1]))

    print(searchBS(big_list))
