
# ------------------------------------------------
# to create a list include lists in it :

def group_list(input_list, size):
    grouped_list = list()
    for i in range(0, len(input_list), size):
        grouped_list.append(input_list[i: i + size])
    return grouped_list
