#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
''' fucking the terrible encode and decode  '''
'''
冗余1：若A->C,AB->C同时存在，抑制AB->C；
冗余2：若A->B,B->A同时存在，只取置信度高一个；
冗余3：若A->B,A->C,A->BC同时存在，抑制A->BC；
冗余4：若A->B,B->A同时存在且干掉B->A，那么不在生成类似BC->A；
冗余5：若AB->C,AC->B,BC->A同时出现，只取其中置信度最高的一个；
冗余6：若A->B,AC->D,BC->D同时出现，抑制BC->D
冗余7：若AB->G,G->H,AB->H同时存在，抑制AB->H
冗余8：若AC->D,BC->D同时出现，没有出现A->B但出现A*->B，抑制BC->D'''
import logging
def testin(alst,blst):
      '''判定前件与后件是否包含与issubset'''
      if set(alst).issubset(set(blst)):
         return True
      else:
         return False
   
testrule=[((1,),(1,2),0.8),((1,3),(1,2,3),0.8),((3,),(3,4,),0.8),((4,),(3,4),1.0),((5,),(5,6,),0.75),((5,),(5,7,),0.9),((7,8),(7,8,9),0.9),((1,),(1,9,),0.7),((1,7),(1,6,7),0.8),((0,4),(0,4,5),0.4),((0,5),(0,5,4),0.3),((4,5),(4,5,0),0.9),((10,11),(10,11,13),0.7),((13,),(13,14),0.5),((10,11),(10,11,14),0.65),((21,),(21,22,),0.6),((21,24),(21,24,25),0.7),((22,24),(22,24,25),0.8)]

'''for rule in testrule:
      print rule[0],rule[1]'''
def filterrules(testrule):
      logging.basicConfig(filename='D:/example.log',level=logging.DEBUG) #将取出的信息输出到log文件中
      '''传入规则序列，返回去冗余后的新序列'''
      flag={rule_1:True for rule_1 in testrule} #初始化标记，初始化为ture
      groupby_1_1=[rule for rule in testrule if len(rule[0])==1 and len(rule[1])==2]
      groupby_2_1=[rule for rule in testrule if len(rule[0])==2 and len(rule[1])==3]
      print groupby_1_1
      print groupby_2_1
      print u'去除第一种冗余，若A->C,AB->C同时存在，抑制AB->C'
      #logging.debug(u'去除第一种冗余，若A->C,AB->C同时存在，抑制AB->C')
      for item_1 in groupby_1_1:
                         for x in groupby_2_1:
                               if testin(item_1[0],x[0]) and testin(item_1[1],x[1]):
                                      flag[x]=False
                                      print 'exists',item_1,'kill',x
                                      
      print u'冗余2：若A->B,B->A同时存在，只取置信度高一个'
      #logging.debug(u'冗余2：若A->B,B->A同时存在，只取置信度高一个')
      for x in groupby_1_1[:]:
            for other in groupby_1_1:
                  if set(list(x[0])+list(x[1]))==set(list(other[0])+list(other[1])):
                      if x[-1]<other[-1]:
                           flag[x]=False
                           print 'exists ',other,'kill',x
      print u'冗余5：若AB->C,AC->B,BC->A同时出现，只取其中置信度最高的一个'
      for item_2 in groupby_2_1[:]:
            count=0
            con=[]
            for y in groupby_2_1:
                  if set(list(y[0])+list(y[1]))==set(list(item_2[0])+list(item_2[1])):
                        count+=1
                        con.append(y)
            if count==3:
                  print u'发现',con
                  maxcon=max(con,key=lambda x:x[-1])
                  for i in con:
                        if i!=maxcon:
                              print 'kill',i
                              flag[i]=False
      print u'冗余6：若A->B,AC->D,BC->D同时出现，抑制BC->D'
      protected=[]
      for item_1_1 in groupby_1_1[:]:
            A=item_1_1[0] #(1,)
            B=tuple(set(item_1_1[1])^set(A))
            for item_2_1 in groupby_2_1[:]:
                  if testin(A,item_2_1[0]):  #(1,) belongs to (1,2)
                        C=tuple(set(item_2_1[0])^set(A))
                        D=tuple(set(item_2_1[1])^set(item_2_1[0]))
                        for item_3 in groupby_2_1[:]:
                              if testin(D,item_3[1]) and testin(C,item_3[0]) and testin(B,item_3[0]):
                                  if (A,C) not in protected:  #保护，防止ac被删除掉，当B—A也存在是
                                    flag[item_3]=False 
                                    print 'kill',(A,B),(A,C),D,'-',(B,C),D
                                    protected.append((A,C))
                                    
                                    
                        
      print u'冗余7：若AB->G,G->H,AB->H同时存在，抑制AB->H'
      for find in groupby_2_1[:]:
            AB=find[0]
            tag=0
            g=list(set(find[0])^set(find[1]))[0]
            for k1 in groupby_1_1[:]:
                  if g in k1[0]:
                        h=list(set(k1[0])^set(k1[1]))[0]
                        
                        for other in groupby_2_1[:]:
                           if other[0]==AB and h in other[1]:
                                flag[AB]=False
                                print 'find ',AB,g,g,h,AB,h
                                print 'kill',AB,h                
            
                     
            
      print  'ok'                            
      return filter(lambda x:flag[x],testrule)


if __name__=='__main__':
      print filterrules(testrule)
      