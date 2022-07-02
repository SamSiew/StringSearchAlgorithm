"""
StudentID: 28098552
Name: Ming Shern,Siew
"""
#!/usr/bin/python
import sys
sys.path.append('..')
from z_algorithm import buildZArray

def buildR(pattern):
    """
    build R array from pattern
    :param pattern: string represent pattern
    :return: 2d array which for rightmost occurances in pattern in character of pattern
    """
    R = [[] for i in range(128)]
    # at most (128*pattern) space and time will be used to allocate leftmost value.
    for i in range(len(pattern)):
        if len(R[ord(pattern[i])]) == 0:
           R[ord(pattern[i])] = [0 for i in range(len(pattern))]
        j = i
        # each element of R will only accessed once and can be proven with average case.
        # allocate the left side array with value on right.
        while j >= 0 and R[ord(pattern[i])][j] == 0:
           R[ord(pattern[i])][j] = i + 1
           j -= 1
    return R

def buildMatchedSuffix(z):
    """
    build matched suffix array from z array but it is just a reverse version of matched prefix
    :param z: z array
    :return: matched suffix[0...len(z)-1] which build from z array
    """
    m = len(z)
    matchprefix = [0 for i in range(m)]
    for p in range(m - 1, -1, -1):
        if p == m - 1 or z[p] + p == m:
            matchprefix[m-(p+1)] = z[p]
        else:
            matchprefix[m-(p+1)] = matchprefix[m-(p+1)-1]
    return matchprefix

def buildGoodPrefix(z):
    """
    build good prefix array from z array
    :param z: z array
    :return: good suffix[0...len(z)-1] which build from z array
    """
    goodsuffix = [0 for i in range(len(z)+ 1)]
    for p in range(len(z)-1,0,-1):
        if z[p] > 0:
            j = z[p] - 1
            goodsuffix[j] = p
    return goodsuffix

def badCharacterRule(R,asciicode,mismatchposition,patternLength):
    """
    get amount of shift required from bad character rule
    :param R: 2d array which for rightmost occurances in pattern in character of pattern
    :param asciicode: asciii code of bad character
    :param mismatchposition: location of mismatch
    :param patternLength: length of pattern
    :return: amount of shift required from bad character rule
    """
    if len(R[asciicode]) == 0 or R[asciicode][mismatchposition] == 0:
        return max(1,patternLength-mismatchposition)
    else:
        return max(1,(R[asciicode][mismatchposition] - 1) - mismatchposition)

def boyermoore(text,pattern):
    """
    This algorithm employ boyer moore but with mirrored version accompany with galil rule for fast implementation.
    gallil rule make use of let say box [i...j] which is a substring that matches prefix and will not be computed.
    It scan left to right, good prefix replace good suffix and matched suffix replaced matched prefix
    :param text: string represent text
    :param pattern: strring represent pattern
    :return: [0...len(text)-1] 1 if subtring[i...len(text-1] matches pattern
    """
    n = len(text)
    m = len(pattern)
    k = n - 1
    z = buildZArray(pattern)
    goodsuffix = buildGoodPrefix(z)
    matchedprefix = buildMatchedSuffix(z)
    r = buildR(pattern)
    #variables which allows skipping for good suffix shift in k-1 iteration for gallil rule
    qStop = m
    qResume = m
    #memo which can help in indicating start index of substring is a pattern
    memo = [0 for i in range(len(text))]
    while k >= m - 1 and m <= n:
        #qpointer is moving pointer for pattern
        qPointer = 0
        #kpointer is moving pointer for text
        kPointer = k - (m-1)
        #explicit comparison from left to right
        while qPointer < m and pattern[qPointer] == text[kPointer]:
            #when qpointer reach [i..j] which matches prefix of previous iteration, no need to compared.
            if qPointer == qStop:
                qPointer = qResume
                kPointer = kPointer + (qResume - qStop)
            qPointer += 1
            kPointer += 1
        #when qpointer is less than m, we know there's a mismatch
        if qPointer < m:
            #good prefix shift only apply when [i..m] the pointer stop but index 0 will never be emloyed since
            #bad character rule is perform faster on index = 0.
            goodPreShift = 0
            badCharShift = badCharacterRule(r,ord(text[kPointer]),qPointer,m)
            if qPointer > 0:
                if goodsuffix[qPointer - 1] > 0:
                    goodPreShift = goodsuffix[qPointer - 1]
                    qStop = goodsuffix[qPointer - 1]
                    qResume = qStop + qPointer - 1
                else:
                    goodPreShift = m - matchedprefix[qPointer-1]
                    qStop = m - matchedprefix[qPointer-1]
                    qResume = m - 1
            #favors goodprefix shift to exploit galil rule for fast termination.
            if goodPreShift >= badCharShift:
                k -= goodPreShift
            else:
                k -= badCharShift
                qStop = m
        # when qpointer is not less than m, we know there's not a mismatch
        else:
            #shift till it reach longest suffix which matches prefix of previous iteration, then purposely terminate faster
            goodPreShift = m - matchedprefix[(m-1)-1]
            memo[k-(len(pattern)-1)] = 1
            k -= goodPreShift
            qStop = m - matchedprefix[(m-1)-1]
            qResume = m - 1
    return memo

if __name__=="__main__":
    string = open(sys.argv[1]).read()
    pattern = open(sys.argv[2]).read()
    output = boyermoore(string,pattern)
    with open('output_mirrored_boyermoore.txt', 'w') as outFile:
        for index in range(len(output)):
            if output[index] == 1:
                outFile.write(str(index + 1) + "\n")
        outFile.close()