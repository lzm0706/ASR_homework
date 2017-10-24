import sys
n_sub=int(sys.argv[3])
n=0
traintext=sys.argv[1]
traintext_sub=sys.argv[2]

traintextob=open(traintext)
traintext_subob=open(traintext_sub,'w')

for line in traintextob.readlines():
    n+=1
    if (n%n_sub)==0:
        print(line,end='',file=traintext_subob)

traintextob.close
traintext_subob.close