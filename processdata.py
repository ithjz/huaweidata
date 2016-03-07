#coding="utf-8"
import xlwt
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from othertools import joindictlst,dictfind          
from readsql import readdata,retalldata,groupinfo
import itertools as itl
import collections as col
from dealseq import *
import json
import pprint
import copy
from toexcel import filterrules
''' fucking the terrible encode and decode  '''

def translate_rule(rulelist_func,indexhouxu):
    '''将name从123反向映射到数据库中的名字，可以在这里处理译码问题，以及输出到文件中'''
    newrulelist=[]
    for arule in rulelist_func:
        front,back,confidence=arule
        front_new=[dictfind(key,Namemap) for key in front]
        back_new=[dictfind(key1,Namemap) for key1 in back]
        x_support=houxu[indexhouxu].get(front,'none')
        y_support=houxu[indexhouxu].get(back,'none')
        newrulelist.append([front_new,back_new,confidence,x_support,y_support])
    return newrulelist
        
def write_rule_excel(torulelist_func,name):
    '''尝试着将规则写入到xls文件中,不同网元的index不同'''
    workbook = xlwt.Workbook()    # 注意这里的Workbook首字母是大写
    sheet1=workbook.add_sheet('sheet_1')
    sheet1.write(0,0,u'前件')
    sheet1.write(0,1,u'x_support')
    sheet1.write(0,2,'back')
    sheet1.write(0,3,'y_support')
    sheet1.write(0,4,'confidence')
    row=1
    for amyrule in torulelist_func:
                    front,back,confidence,x_sum,y_sum=amyrule
                    front_text=' '.join(front)
                    back_text=' '.join(back)
                    confid=str(confidence)
                    sheet1.write(row,0,front_text)
                    sheet1.write(row,1,str(x_sum))
                    sheet1.write(row,2,back_text)
                    sheet1.write(row,3,str(y_sum))
                    sheet1.write(row,4,confid)
                    row+=1                            
    workbook.save(name+"test_excel.xls")
    
    
    
    
    
def write_rule_view(torulelist_func):
    '''尝试着将规则写入到txt文件中'''
    with open('D:/sun.txt','wb') as f:
        for amyrule in torulelist_func:
                front,back,confidence,x_count,y_count=amyrule
                for front_item in front:
                    print front_item,"--",
                print '\n'
                for back_item in back:
                        print back_item,
                print '\n'
                print confidence
                print x_count,y_count
                
                                 
def view():
    for ne in NEmap.values():
        for so in AlarmSmap.values():
            print len(structdata[ne][so])

def dealne(nename,structdata):
    '''统计不同网元的候选集数量，并合并不同的报警元下的计数器，alarmsource'''
    seqlst= [ i for i in structdata[nename].values() if len(i)>=2]  #限定元素个数至少为n个，否则舍弃该序列
    #counlst=map(seqdcit,seqlst)#可用进程加速，cpu密集型,错误，应用paitial
    cuntlst=[seqdcit(i,i[0][1]-5,60,4) for i in seqlst]  #在这里调节时间窗的length和重复n
    houxuanji=joindictlst(cuntlst)
    return houxuanji
    


if __name__=="__main__":
    try:
      database=readdata("test","uiop.123.123",'root')
      con1=database.connectsql()  #初始化数据库，数据库名为，编码默认为utf-8
      data=retalldata(con1)       #将数据库中的数据存到data变量，类型为嵌套的tuple，大概有5万条，为了测试可减少,建议测试数据为100条
      infos=groupinfo(con1)       #返回字典，包括如下信息分类情况，name，NE，alarmsource 的类型，方便映射到"1-n"     
      datatest=data
      #print len(datatest)          #将NE，Name，alarmsource映射到，1到200，如 MSCServer：0，CGPOMU ： 1
      print u'数据读取完成开始分析',len(data)
      NEmap=dict(zip(infos["NE"],xrange(len(infos["NE"])+2)) )
      Namemap=dict(zip(infos["Name"],xrange(len(infos["Name"])+2)))
      AlarmSmap=dict(zip(infos["AlarmSource"],xrange(len(infos["AlarmSource"])+2)))
      base1={i:col.deque() for i in AlarmSmap.values()}
      structdata={ne:copy.deepcopy(base1) for ne in NEmap.values()}
      count=0   #正常插入的数据个数
      errcount=0 #报错的个数
      houxu=[]  #用来存储每个网元下报警情况的字典，直接传入，不同网元计数器组成的列表，统计的时候在这里看候选集的数量
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
       
      print u'网元1候选集',len(houxu[1].keys())
      print 'items',houxu[1]==houxu[0]
      print count,"sucessful count",
      print errcount,"error count"
      rules=[rulemake(rudict,2,0.7) for rudict in houxu]   #支持度为2，置信度为0.7,返回由网元序号为index的规则，比如网元1->rule[1]
      print "dealing rules***"
      print len(rules),'NE in sum'
      print " ok no error deted"
      print u"trying to translate to chinese"
      #my_test_new_rule=translate_rule(sorted(rules[0],key=lambda x: x[-1]),0) #按照置信度进行排序
      #print houxu[0].values()
      #print my_test_new_rule
      #write_rule_view(my_test_new_rule)
      #write_rule_excel(my_test_new_rule,0) #写入excel测试成功！！
      rules=[filterrules(a_lst_rule) for a_lst_rule in rules]  #去除冗余项后的新规则
      print u'去除冗余成功'
      newrulelst=[]
      for index_g,rule_my in enumerate(rules):
          newrulelst.append(translate_rule(sorted(rule_my,key=lambda x: x[-1]),index_g))
      '''for NE_index,rule_new in enumerate(newrulelst):
          write_rule_excel(rule_new,NE_index)'''
      sun1=0
      for rule_ne in newrulelst:
          write_rule_excel(rule_ne,str(sun1))
          sun1+=1
          
      print 'stop running'                
                
     
      
    except Exception as e:
         print str(e)
    finally:
         con1.close()