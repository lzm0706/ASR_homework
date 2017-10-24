import sys
import re
from collections import Counter
#import collections
from itertools import combinations
from math import log

'''
def smoothing(data):
    #print(len(data))
    smdata=data
    for key in smdata.keys():
        smdata[key]=smdata[key]+1
    return smdata
'''

traintext=sys.argv[2]
lmlist=sys.argv[1]

wordsobject=open(traintext)
dictobject=open(lmlist)


dicts=Counter()
for line in dictobject.readlines():
    #print(line)
    dictArr=re.sub('\n','',line).split()
    #print(dictArr)
    dicts.update(dictArr)
dd=dict(dicts)
#print(dd)
#print(len(dd))
ngram1d=len(dd)
print('1-grams in dict =',ngram1d)

words=[]
words2=[]
words3=[]
dict1=Counter()
dict2=Counter()
dict3=Counter()

for line in wordsobject.readlines():
    wordArr=re.sub('\n','',line).split(' ')
    dict1.update(wordArr)
    words.extend(wordArr)
    for i in range(0,len(wordArr)-1):
        word2=[str(wordArr[i]+' '+wordArr[i+1])]
        #print(word2)
        if i<len(wordArr)-2:
            word3=[str(wordArr[i]+' '+wordArr[i+1]+' '+wordArr[i+2])]
            #print(word3)
            
            dict3.update(word3)
        dict2.update(word2)
d1=dict(dict1)#uni-gram字典(训练语料得出的)
d2=dict(dict2)#bi-gram字典
d3=dict(dict3)#tri-gram字典
ngram1=len(dict(dict1))
ngram2=len(dict(dict2))#bi-gram种数
ngram3=len(dict(dict3))#tri-gram种数

#print(d2)
#print(d3)
print('1-grams=',len(dict(dict1)))
print('2-grams=',len(dict(dict2)))
print('3-grams=',len(dict(dict3)))

n11=0
n12=0
for key in d1:
    if d1[key]==1:
        n11+=1
    if d1[key]==2:
        n12+=1
db1=n11/(n11+2*n12)


n21=0
n22=0
for key in d2:
    if d2[key]==1:
        n21+=1
    if d2[key]==2:
        n22+=1
db2=n21/(n21+2*n22)

n31=0
n32=0
for key in d3:
    if d3[key]==1:
        n31+=1
    if d3[key]==2:
        n32+=1
db3=n31/(n31+2*n32)

#计算Pkn(wi)
def pwi(wi):
    xwi=0
    wix=0
    global db2
    global db1
    for key in d2:
        #print('***',key)
        if key[(len(key)-len(wi)-1):len(key)]==str(' '+wi):
            xwi=xwi+1#*wi出现次数
        if key[0:(len(wi)+1)]==str(wi+' '):
            wix=wix+1#wi*出现次数
    if wi=='<s>':
        p1=1
    elif (xwi==0 and wi!='<s>'):
        p1=db1/(ngram1d*ngram2)
    else:
        p1=(xwi)/(ngram2)
    arpap1=log(p1,10) #以10为底取对数
    if wix==0:
        print('***',wi)
        bp1=1
    else:
        bp1=(db2/(d1[wi]))*wix
        #print(wi,bp1)
    arpabp1=log(bp1,10)
    return arpap1,arpabp1
#print(pwi('d'))

#计算Pkn(wi|wi-1)
def  pwi_1wi(wi_1wi):
    global db2
    global db3
    wi_1wix=0
    wi_1wi_a=wi_1wi.split(' ')[0]
    wi_1wi_b=wi_1wi.split(' ')[1]

    for key in d3:
        if key[0:(len(wi_1wi))]==wi_1wi:
            wi_1wix=wi_1wix+1#wi_1wi*出现次数

    p2=(max((d2[wi_1wi]-db2),0))/(d1[wi_1wi_a])
    bp2=(db3/(d2[wi_1wi]))*wi_1wix
    
    arpap2=log(p2,10) #以10为底取对数
    if bp2==0:
        print('***',wi_1wi)
        return arpap2,' '
    else:
        arpabp2=log(bp2,10)
        return arpap2,arpabp2
#print(pwi_1wi('a b'))

#计算Pkn(wi|wi-2wi-1)
def pwi_2wi_1wi(wi_2wi_1wi):
    global db3
    wi_2wi_1wi_a=str(wi_2wi_1wi.split(' ')[0]+' '+wi_2wi_1wi.split(' ')[1])
    wi_2wi_1wi_b=str(wi_2wi_1wi.split(' ')[1]+' '+wi_2wi_1wi.split(' ')[2])

    p3=max((d3[wi_2wi_1wi]-db3),0)/(d2[wi_2wi_1wi_a])
    arpap3=log(p3,10) #以10为底取对数
    return arpap3
#print(pwi_2wi_1wi('a b c'))

def arpa(address):
    arpaname=address
    arpaobject= open(arpaname, "w")
    print('\n',end='',file=arpaobject)
    print('\data\\',file=arpaobject)
    print('ngram 1=',ngram1d,sep='',file=arpaobject)
    print('ngram 2=',ngram2,sep='',file=arpaobject)
    print('ngram 3=',ngram3,sep='',file=arpaobject)
    print('\n\\1 - grams:',file=arpaobject)
    for key in dicts:
        if key=='</s>':
            print(pwi(key)[0],key,file=arpaobject)
            print(pwi(key)[0],key)
        else:
            print(pwi(key)[0],key,pwi(key)[1],file=arpaobject)
            print(pwi(key)[0],key,pwi(key)[1])
    print('\n\\2 - grams:',file=arpaobject)
    for key in d2:
        if key[(len(key)-len('</s>')):len(key)]=='</s>':
            print(pwi_1wi(key)[0],key,file=arpaobject)
            print(pwi_1wi(key)[0],key)
        else:
            print(pwi_1wi(key)[0],key,pwi_1wi(key)[1],file=arpaobject)
            print(pwi_1wi(key)[0],key,pwi_1wi(key)[1])
    print('\n\\3 - grams:',file=arpaobject)
    for key in d3:
        print(pwi_2wi_1wi(key),key,file=arpaobject)
        print(pwi_2wi_1wi(key),key)
    arpaobject.close
    
arpa(sys.argv[3])

wordsobject.close
dictobject.close