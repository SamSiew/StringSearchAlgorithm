"""
StudentID: 28098552
Name: Ming Shern,Siew
"""
#!/usr/bin/python
import sys
sys.path.append('..')
from z_algorithm import buildZArray

def wildSearch(text,pat):
    """
    :param text: string represent text
    :param pat: string represent pattern
    :return: array represent binary number if start index of substring is a pattern
    """
    n = len(text)
    m = len(pat)
    #memorization for skipping continuous wild '?' character.
    wildCardMemo = buildZArray(('?'*m)+pat)
    subpointer = 0
    currentstr = ""
    #list of substring and length of the substring to allow wild pattern search.
    substring = [None for i in range(m)]
    while subpointer < m:
        if wildCardMemo[m+subpointer] == 0:
            currentstr += pat[subpointer]
            subpointer += 1
        if subpointer == m or wildCardMemo[m+subpointer] != 0:
            if len(currentstr) > 0:
                substring[subpointer-len(currentstr)] = [len(currentstr),currentstr]
                currentstr = ""
            #skips continous '?' character
            if subpointer < m:
                subpointer += wildCardMemo[m+subpointer]
    #mastermemo is memorization of previou best solution but will accompanied with slavememo for current best solution.
    masterMemo = [0 for i in range(n)]
    #k is a pointer which will iterate trough the text but seperated by '?'
    k = 0
    #while k is < m:
    # if current k is wild card -> go through mastermemo[0..n] if value is length of previous prefix[1..k],
    #     then add the value by longeest number of continous '?'
    #
    # if current k is not wild card -> go through mastermemo[0..n] if value is length of previous prefix[1..k],
    #     then add the value by longest suffix[k..n] which matches prefix[k..n].
    #
    # t + (m - k) <= n condition allows faster termination when suffix of text is obviously shorter than length of pattern.
    # for example, pat = aabbaa, txt = aabbaabbaa. (....abbaa) suffix is not be check in first t comparison,
    # works well on large and collection suffix of txt
    while k < m:
        if wildCardMemo[m + k] != 0:
            t = 0
            while t < n and t + (m - k) <= n:
                if masterMemo[t] == k:
                    masterMemo[t] += wildCardMemo[m + k]
                t += 1
            k += wildCardMemo[m + k]
        else:
            slaveMemo = buildZArray(substring[k][1] + '$' + text)
            t = 0
            while t < n and t + (m - k) <= n:
                if masterMemo[t] == k:
                    masterMemo[t] += slaveMemo[substring[k][0] + 1 + t + k]
                t += 1
            k += substring[k][0]

    #reconstruct solution so that we can find out start index of substring which matches pattern
    for i in range(n):
        if masterMemo[i] == m:
            masterMemo[i] = 1
        else:
            masterMemo[i] = 0

    return masterMemo

if __name__== "__main__":
    string = open(sys.argv[1]).read()
    pattern = open(sys.argv[2]).read()
    output = wildSearch(string,pattern)
    with open('output_wildcard_matching.txt', 'w') as outFile:
        for index in range(len(output)):
            if output[index] == 1:
                outFile.write(str(index + 1) + "\n")
        outFile.close()