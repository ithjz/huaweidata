#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
''' fucking the terrible encode and decode  '''
def joindictlst(lst):
    '''合并两个字典，在这里是合并计数器，for example {"a":2,"b":3}+{"a":1,"c":4}={"a":3,"b":3,"c":4}'''
    counnt=lst[0]
    for cut in lst[1::]:
        for key in cut.keys():
            if key in counnt:
                counnt[key]+=cut[key]
            else:
                counnt[key]=cut[key]
    return counnt

def dictfind(key,amap):
    ''' 反方向dict，根据vlau找到相应的键值'''
    for i in amap.keys():
        if amap[i]==key:
            return i
    

if __name__=='__main__':
    sun={i:str(i) for i in range(4)}
    print dictfind('19',sun)
    print sorted([[1,2],[3,4],[2,-1],[3,6]],func=rulesort)