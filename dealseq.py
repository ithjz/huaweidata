#coding=utf-8
import itertools
import  collections
from collections import namedtuple
import random

def itertolst(iters):
   con=[]
   for i in iters:
      con.append(i)
   return con
   
def make():
   for i in range(100):
      name=random.choice(range(5))
      time=i+3
      yield (name,time)

def slidingwindow(seq,start,length,n):
     step=length/n
     con=[]
     end=start+length
     for item in seq:
         if start<item[1]<end:
            con.append(item)
         else:
            yield list(set(con))  #元素去重复
            #yield con
            #print con
            #start=end-step
            start=item[1]-step  # 防止出现时间间隔太大序列的情况，如[A,B,B,C,D,A,C,D,V,] ->[A,B,C,D,V] 去除重复元素，但是没有顺序
            end=start+length
            s1=itertools.dropwhile(lambda x:x[1]<start,con)
            con=itertolst(s1)
            con.append(item)

def countwindow(wind,seqcount):
   namelst=[i[0] for i in wind]  # like this format [1,2,3,2,1,3]
   countdict={i:namelst.count(i) for i in set(namelst)}   # like{1:2,2:3,3:5}
   setname=sorted(list(set(namelst)))
   for k in range(1,4): #生成1到3项集合
      pinfanji=list(itertools.combinations(setname,k)) #[(1,2),(3,4)]
      for jihe in pinfanji:
          count=min([countdict.get(x,0) for x in jihe]) #取每种组合最小值，
          if jihe in seqcount:
             seqcount[jihe]+=count
          else:
             seqcount[jihe]=count
   

def seqdcit(seq,start,length,n):   #START 要足够小，否则报错,传入参数为序列，窗口长度，n,返回该序列的在一定长度下的所有候选集
   countall={}
   print start,length
   windows=slidingwindow(seq,start,length,n)
   for part in windows:
         countwindow(part,countall)
         
    
   return countall


def rulemake(count_1,support,config):
     #print "making rules"
     cunt_new={key:value for key,value in count_1.items() if value>=support} #频繁集生成候选集
     kpin=[sorted([key for key in cunt_new.keys() if len(key)==i]) for i in range(1,4)]
     rule1=[(k1,k2,float(cunt_new[k2])/cunt_new[k1]) for k1 in kpin[0] for k2 in kpin[1] if float(cunt_new[k2])/cunt_new[k1]>=config and (k1[0] in k2)]
     rule2=[(k2,k3,float(cunt_new[k3])/cunt_new[k2]) for k2 in kpin[1] for k3 in kpin[2] if float(cunt_new[k3])/cunt_new[k2]>=config and  k3[0:2]==k2]
     rule3=[(k1,k3,float(cunt_new[k3])/cunt_new[k1]) for k1 in kpin[0] for k3 in kpin[2] if float(cunt_new[k3])/cunt_new[k1]>=config and  k1[0] in k3]
     #print 'sorted dict',cunt_new 测试的输出语句，测试的时候可以启用
     #print "testing rules"
     #print rule1
     #print rule3
     return rule1+rule2+rule3

if __name__ =="__main__":  
  
  
  sun=make()
  test=seqdcit(sun,1,9,3)
  print test.items()
  print sum(test.values())
  print test.keys()
  rulemake(test,12,0.4)
  
   