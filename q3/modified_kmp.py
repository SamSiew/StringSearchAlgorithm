"""
StudentID: 28098552
Name: Ming Shern,Siew
"""
#!/usr/bin/python
import sys
sys.path.append('..')
from z_algorithm import buildZArray

def buildSPArray(pattern):
    """
    build Given a pattern pat[1...m], SPi (for each position i in pat) as the length of the longest proper suffix of pat[1...i]
    that matches a preﬁx of pat with the extra condition that pat[SPi(x)+1] = x
    :param pattern: string represent pattern
    :return: 2d array which represent SPi (for each position i in pat) as the length of the longest proper suffix of pat[1...i]
    that matches a preﬁx of pat with the extra condition that pat[SPi(x)+1] = x
    """
    z = buildZArray(pattern)
    m = len(pattern)
    SP  = [[0 for i in range(128)] for i in range(m)]
    for j in range(m-1,0,-1):
        i = j + z[j] - 1
        x = pattern[z[j]]
        SP[i][ord(x)]= z[j]
    return SP

def kmp(text,pat):
    """
    perform kmp algorithm for string matching on text and pattern
    :param text: string represent text
    :param pat: string represent pattern
    :return: array represent binary number if start index of substring is a pattern
    """
    m = len(pat)
    n = len(text)
    sp = buildSPArray(pat)
    #memorisation to indicate start index of subtring is a pattern
    memo = [0 for i in range(n)]
    textpos = 0
    patpos = 0
    #run till text has finish scanning and and terminate smartly when suffix of text is shorter than suffix of pattern
    while textpos < n and (n-textpos) >= (m-patpos):
        #when text[i] == pat[j], increment by 1 for both pointer and if pat has reach its length, then
        #indicate in memo with start index is pat and if textpos is still not finish, then shift patpos
        #by longest suffix that matches prefix with consideration of pat[sp[i]+1] == text [j].
        if text[textpos] == pat[patpos]:
            textpos += 1
            patpos += 1
            if patpos == m:
                memo[textpos-m] = 1
                if textpos < n:
                    char = text[textpos]
                    patpos = sp[patpos - 1][ord(char)]
        #when text[i] != pat[j], if patpos is at 0, shift text by 1 else:
        #shift pat to if(longest suffix matches prefix is 0) such that next iteration, start scan at 0 index
        #else: shift it by longest suffix matches prefix
        else:
            #patpos == 0 (deals with mismatch smartly)
            if patpos == 0:
                textpos += 1
            else:
                char = text[textpos]
                if sp[patpos - 1][ord(char)] == 0:
                    patpos = 0
                else:
                    patpos = sp[patpos - 1][ord(char)] + 1
                    textpos += 1
    return memo


if __name__=="__main__":
    string = open(sys.argv[1]).read()
    pattern = open(sys.argv[2]).read()
    output = kmp(string,pattern)
    with open('output_kmp.txt', 'w') as outFile:
        for index in range(len(output)):
            if output[index] == 1:
                outFile.write(str(index + 1) + "\n")
        outFile.close()