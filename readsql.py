#coding=utf-8
import MySQLdb
class readdata(): #connect函数返回该数据库的链接
    def __init__(self,db,passwd,user):
        self.db="testsmall"
        self.passwd="uiop.123.123"
        self.user="root"
        self.port=3306
    def connectsql(self,):
        try:
            con=MySQLdb.connect(host="127.0.0.1",user=self.user,db=self.db,port=self.port,passwd=self.passwd,charset="utf8")
            return con
        except Exception as e:
                print "got a error"
                print str(e)

def retalldata(mycon):  #返回数据库中的所有数据，格式为tuple
    course=mycon.cursor()
    try:
        sql="select * from original_data_new order by OccurrenceTime"
        course.execute(sql)
        rs=course.fetchall()
        return rs
    except Exception as e:
        print "get a error"
        print str(e)
    finally:
        course.close()
        
def groupinfo(con):
    course=con.cursor()
    try:
        infor={}
        sql1="select NE from original_data_new group by NE " 
        sql2="select Name from original_data_new group by Name"
        sql3="select AlarmSource from original_data_new group by AlarmSource" 
        course.execute(sql1)
        infor['NE']=[x[0] for x in course.fetchall()]
        course.execute(sql2)
        infor['Name']=[x[0] for x in course.fetchall()]
        course.execute(sql3)
        infor['AlarmSource']=[x[0] for x in course.fetchall()]
        
        return infor
        
        
    except Exception as e:
        print e
        print str(e)
    finally:
        course.close()
    
    
    
if __name__=="__main__":
    try:
      database=readdata("testsmall","uiop.123.123",'root')
      con1=database.connectsql()
      data=retalldata(con1)
      print len(data)
      print data[1]
      print data[2]
      infos=groupinfo(con1)
      print infos['AlarmSource']
    finally:
         con1.close()