"""
Merge sort implementation
Continually splits a list in half. Once down to sets of zero or 
one item, merge sets together by comparing smallest (first) of each set
and using the smallest of these to generate the next level list

Time
    Best O(n log n)
    Average O(n log n)
    Worst O(n log n)
Space 
    Worst O(n)
"""


def merge_sort(array):
    """
    Returns the ordered list of a list of numeric values
    """

    # if not at lowest level, continue to split
    if len(array) > 1:

        # split it
        mid = len(array) // 2
        left = array[:mid]
        right = array[mid:]

        left = merge_sort(left)
        right = merge_sort(right)

        # merge left and right
        return merge(left, right)
        
    else:
        return array

def merge(left, right):
    """ Merges two unosorted lists into a single, sorted list """
    sorted_list = []
    # add smallest item into sorted list until either empty
    while left and right:
        if left[0] < right[0]:
            sorted_list.append(left.pop(0))
        else:
            sorted_list.append(right.pop(0))
    # left half still has elements, add to end of sorted
    if left:
        sorted_list.extend(left)
    # right half still has elements, add to end of sorted
    elif right:
        sorted_list.extend(right)
    return sorted_list
