'''
20190616 JiaYi Zhang
CYK algorithm with intersted non-terminal

Read input from stdin, parse input text with given grammar
return ranges of interested non-terminals
'''

from collections import defaultdict
from math import log,exp
import re

def debug(dp,span):
    for i in range(span):
        for j in range(span-i):
            print(dp[i][j],end='')
        print()

class Node:
    '''
    lchild and rchild should be a 3-tuple, representing an index in parse chart.
    '''
    def __init__(self, tag, lchild, rchild, prob):
        self.tag = tag
        self.lchild = lchild
        self.rchild = rchild
        self.prob = prob
    
    def __str__(self):
        return "{}|{},{}|{}".format(self.tag,self.lchild,self.rchild,self.prob)
    
    def __repr__(self):
        return "{}-{}".format(self.tag, self.prob)

class AmbiguousDatePicker:
    def __init__(self, grammarFile, interestfile):
        self.readRawGrammar(grammarFile)
        self.readInterest(interestfile)

    
    def PCYK(self, ipt):
        self.ipt_sentence = ipt
        span = len(ipt)
        dp = [[[] for j in range(span - i)] for i in range(span)]

        for i in range(span):
            for rule in self.unary_cfg.keys():
                m = re.match(rule,ipt[i])
                if not m is None:
                    #print(rule)
                    ks = list(self.unary_cfg[rule].keys())
                    for k in ks:
                        dp[0][i].append(Node(k,None,None,self.unary_cfg[rule][k]))

        for l in range(1,span):
            for s in range(span-l):
                for p in range(0,l):
                    lk = dp[p][s]
                    rk = dp[l-p-1][p+s+1]
                    for i in lk:
                        lk_tag = i.tag
                        for j in rk:
                            rk_tag = j.tag
                            if lk_tag in self.binary_cfg and rk_tag in self.binary_cfg[lk_tag]:
                                key_list = list(self.binary_cfg[lk_tag][rk_tag].keys())
                                for k in range(len(key_list)):
                                    if not key_list[k] in dp[l][s]:
                                        prob_l = dp[p][s][k].prob
                                        prob_r = dp[l-p-1][p+s+1][k].prob
                                        dp[l][s].append(Node(key_list[k],(p,s,k),(l-p-1,p+s+1,k),prob_l+prob_r))

        self.parse_tree = dp


    def readRawGrammar(self, files):
        binary = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0.0)))
        unary = defaultdict(lambda:defaultdict(lambda:0.0))

        symbol = defaultdict(lambda: False)

        tot = defaultdict(lambda:0.0)
        # Begin reading
        for fn in files:
            with open(fn) as f:
                for l in f:
                    parts = l.split()
                    lhs = parts[0]
                    proba = float(parts[-1])
                    argLength = len(parts)
                    if argLength == 5: # Binary
                        binary[parts[2]][parts[3]][lhs] += proba
                        symbol[parts[3]] = True
                        symbol[parts[2]] = True
                    elif argLength == 4: # Unary
                        #print(parts[2])
                        unary[parts[2]][lhs] += proba
                        symbol[parts[2]] = True
                    tot[lhs] += proba
                    symbol[lhs] = True
        # End reading
        # Begin normalizing
        for i in binary:
            for j in binary[i]:
                for k in binary[i][j]:
                    binary[i][j][k] = log(binary[i][j][k]) - log(tot[k])
        for i in unary:
            for j in unary[i]:
                unary[i][j] = log(unary[i][j]) - log(tot[j])
        # End normalizing
        # return binary,unary,symbol,tot
        self.binary_cfg = binary
        self.unary_cfg = unary
        self.symbol_dict = symbol


    def readInterest(self, filename):
        with open(filename) as f:
            c = f.read()
        l = c.split()
        self.interest_list = l

    def bt(self, pos,indent):
        curNode = self.parse_tree[pos[0]][pos[1]][pos[2]]
        # print("  "*indent,end='')
        # print(curNode.tag,pos[1])
        if curNode.lchild is None:
            self.tag_result.append(curNode.tag)
            return pos[1],pos[1]
        lp1,rp1 = self.bt(curNode.lchild,indent+1)
        lp2,rp2 = self.bt(curNode.rchild,indent+1)
        return lp1,rp2

    def backTrace(self,i,j,k):
        self.tag_result = []
        curPt = self.parse_tree[i][j][k]
        # print("#"*10)
        # print(curPt.tag,exp(curPt.prob))
        
        if curPt.lchild is None:
            # print("#"*10)
            self.tag_result.append(curPt.tag)
            return j,j
        lp1,rp1 = self.bt(curPt.lchild,1)
        lp2,rp2 = self.bt(curPt.rchild,1)
        # print("#"*10)
        return curPt.tag,lp1,rp2,curPt.prob

    def findInterestParse(self):
        parse_tree = self.parse_tree
        interest = self.interest_list
        span = len(parse_tree)
        res = []
        for i in range(span):
            for j in range(span-i):
                for n in range(len(parse_tree[i][j])):
                    if parse_tree[i][j][n].tag in self.interest_list:
                        roottag, l,r,p = self.backTrace(i,j,n)
                        res.append((roottag,self.tag_result,self.ipt_sentence[l:r+1],p))
        return res
    
    def ParseSentence(self, ipt):
        self.PCYK(ipt)
        res = self.findInterestParse()
        return res
