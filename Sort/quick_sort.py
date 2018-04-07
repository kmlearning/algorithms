
def quick_sort(array):
    """ 
    Given a list of numerical values, 
    returns their sorted list using quick sort algorithm
    """
    length = len(array)

    if length > 1:

        pivot = array[0]
        left = 1
        right = length - 1

        while right > (left - 1):

            while array[left] < pivot and left < right:
                left += 1
            while array[right] >= pivot and right > (left - 1):
                right -= 1
            if left < pivot and right >= pivot:
                array[left], array[right] = array[right], array[left]
            else:
                array[right], array[0] = array[0], array[right]                

                array[:left] = quick_sort(array[:left])
                array[left:] = quick_sort(array[left:])
                return array

    else:
        return array
