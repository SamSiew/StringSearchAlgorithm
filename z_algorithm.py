"""
StudentID: 28098552
Name: Ming Shern, Siew
"""
def buildZArray(pattern):
    """
    :param pattern: string representing pat
    :return: array with length of pat
    Time Complexity:
       Worst Case: O(m)
       where m is length of pat
       Z Array is computed m times because unnecessary comparison are removed using z-interval box.
    Space complexity:
       Worst Case: O(m)
       where m is length of pat
       Z Array with m space at most is created in algorithm.
    """
    zarray = [0 for i in range(len(pattern))]
    n = len(pattern)
    left, right, zvalue = 0, 0, 0
    zarray[0] = len(pattern)
    currentposition = 1
    while currentposition < n:
        #explicit check since there is no box for memorization
        if currentposition > right:
            left, right = currentposition, currentposition
            while right < n and pattern[right - left] == pattern[right]:
                right += 1
            zvalue = right - left
        else:
            #explicit check starting from right side since zarray[k:m] != zarray[k-l:m]:
            if zarray[currentposition - left] == right - currentposition + 1:
                left, right = currentposition, right + 1
                while right < n and pattern[right - currentposition] == pattern[right]:
                    right += 1
                zvalue = right - currentposition
            else:
                #smartly copy value since it is within the box or already over compute for k+1 iteration
                if zarray[currentposition - left] < right - currentposition + 1:
                    zarray[currentposition] = zarray[currentposition - left]
                else:
                    zarray[currentposition] = right - currentposition + 1
                currentposition += 1
                continue
        #only overwrite value when zarray has enough memorization.
        if zvalue > 0:
            zarray[currentposition] = zvalue
            right = right - 1
            left = currentposition
        currentposition += 1
    return zarray
