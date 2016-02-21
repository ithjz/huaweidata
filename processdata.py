#coding="utf-8"
def view():
    for ne in NEmap.values():
        for so in AlarmSmap.values():
            print len(structdata[ne][so])

def dealne(nename,structdata):
    seqlst= [ i for i in structdata[nename].values() if len(i)>=0]  #限定元素个数至少为n个，否则舍弃该序列
    #counlst=map(seqdcit,seqlst)#可用进程加速，cpu密集型,错误，应用paitial
    cuntlst=[seqdcit(i,i[0][1]-5,60,3) for i in seqlst]  #在这里调节时间窗的length和重复n
    houxuanji=joindictlst(cuntlst)
    return houxuanji
    
from othertools import joindictlst,dictfind          
from readsql import readdata,retalldata,groupinfo
import itertools as itl
import collections as col
from dealseq import *
import json
import pprint

if __name__=="__main__":
    try:
      database=readdata("testsmall","uiop.123.123",'root')
      con1=database.connectsql()  #初始化数据库，数据库名为，编码默认为utf-8
      data=retalldata(con1)       #将数据库中的数据存到data变量，类型为嵌套的tuple，大概有5万条，为了测试可减少,建议测试数据为100条
      infos=groupinfo(con1)       #返回字典，包括如下信息分类情况，name，NE，alarmsource 的类型，方便映射到"1-n"     
      datatest=data
      #print len(datatest)          #将NE，Name，alarmsource映射到，1到200，如 MSCServer：0，CGPOMU ： 1
      NEmap=dict(zip(infos["NE"],xrange(200)))
      Namemap=dict(zip(infos["Name"],xrange(200)))
      AlarmSmap=dict(zip(infos["AlarmSource"],xrange(200)))
      base1={i:col.deque() for i in AlarmSmap.values()}
      structdata={ne:base1.copy() for ne in NEmap.values()}
      count=0   #正常插入的数据个数
      errcount=0 #报错的个数
      houxu=[]  #用来存储每个网元下报警情况的字典，直接传入，makerule
      for item in datatest:
            name,AlarmSource,OccurenceTime,NE=item[1],item[2],int(item[4]),item[6]
            iteminfo=(Namemap[name],OccurenceTime)
            try:
              structdata[NEmap[NE]][AlarmSmap[AlarmSource]].append(iteminfo)  #到此可以将数据正长存入。
              count+=1
            except Exception as e:
                errcount+=1
      for neid in sorted(NEmap.values()):
          houxu.append(dealne(neid,structdata))  #到此为止所有候选集都存在这列表中
       
      print len(houxu)
      print u'网元1候选集',len(houxu[1].keys())
      print 'items',sorted((houxu[1].items()))
      print 'sun values' ,houxu[0].values()
      sun1=[x for x in houxu[0].keys() if len(x)==1]
      sun2=[x for x in houxu[1].keys() if len(x)==1]
      print u"一项集的数目"
      print len(sun1),len(sun2)
      print "names from NEmap",len(Namemap.values())
      print "names from sql",len(infos["Name"])
      print count,"sucessful count",
      print errcount,"error count"
      rules=[rulemake(rudict,2,0.7) for rudict in houxu]   #支持度为2，置信度为0.7
      print "dumping rules***"
      fout=open("rules.json","w")
      strrules=rules[:] #a copy of rule
      for rulejihe in strrules: #尝试着译码，但是没成功
          for smallrule in rulejihe:
              front,back,confidece=smallrule
              strfront=[dictfind(i,Namemap) for i in front]
              strback=[dictfind(i,Namemap) for i in back]
              print >>fout,strfront,',',strback,',',confidece
      #json.dump(rules,fout)          
      print " ok no error deted"
    except Exception as e:
         print str(e)
    finally:
         con1.close()
         fout.close()