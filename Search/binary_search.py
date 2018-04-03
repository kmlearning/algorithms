def binary_search(my_list, value):
    """
    Find a value in an ordered list

    Keyword args:
    mylist -- an ordered list
    value -- value to search for in my_list

    Returns the index of the value if found, else returns None
    """

    found = False
    start = 0
    end = len(my_list) -1

    while start <= end and not found:
        midpoint = (start + end) // 2
        # found value
        if my_list[midpoint] == value:
            return midpoint
        else:
            # search left half
            if value < my_list[midpoint]:
                end = midpoint -1
            # search right half
            else:
                first = midpoint + 1
    # did not find value in my_list
    return None