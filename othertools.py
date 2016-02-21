#coding=utf-8

def joindictlst(lst):
    counnt=lst[0]
    for cut in lst[1::]:
        for key in cut.keys():
            if key in counnt:
                counnt[key]+=cut[key]
            else:
                counnt[key]=cut[key]
    return counnt

def dictfind(key,amap):
    for i in amap.keys():
        if amap[i]==key:
            return i.encode('gb2312')

if __name__=='__main__':
    sun={i:str(i) for i in range(4)}
    print dictfind('3',sun)