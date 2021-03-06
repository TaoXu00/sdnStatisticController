import matplotlib
matplotlib.use('Agg')
import sys
import time
from datetime import datetime
import calendar
import matplotlib.pyplot as plt
import MySQLdb
import numpy as np
import os

#import mysql.connector

def timeConvert(indate):
    dt=datetime.strptime(indate,"%Y-%m-%d %H:%M:%S")
    dt_now=datetime.now()
    dt=dt.replace(year=dt_now.year,month=dt_now.month,day=dt_now.day)
    t1=calendar.timegm(dt.utctimetuple())
    return t1
    
def dataXY(record,basetime,t,s):
    oneM=1000000
    indate=record[1]
    relativetime=timeConvert(indate)-basetime
   # print ("relativetime %d",relativetime)
    t.append(relativetime)
    if record[2]==0:
        r3=0
    else:
        r3=record[3]
    s.append((record[2]+r3)/(oneM*1.0))
def excuteSql(sql,conn):
    #print sql
    cursor=conn.cursor()
    cursor.execute(sql)
    return cursor
def cumulation_func(record,basetime,t_cumulation,cumulation,accum):
    kb=1000*8  #bits
    indate=record[1]
    relativetime=timeConvert(indate)-basetime
    t_cumulation.append(relativetime)
    if record[2]==0:
        rs=0
    else:
        rs=record[3]
    acc=((record[2]+rs)/kb)*3+accum
    cumulation.append(acc)	   #unit is bits
    return acc
def movefile(time,tile):
	newFolder="/home/xu/SDN_APP/"+time+"s"
	os.system("mkdir newFolder")
	graph1="/home/xu/SDN_APP/"+titleName+".png"
	graph2="/home/xu/SDN_APP/"+titleName+"_cumulation.png"
	file1="/home/xu/SDN_APP/"+"cumulation.txt"
	com1="mv "+graph1+" "+newFloder
	com2="mv "+graph2+" "+newFloder
	com3="mv "+file1+" "+newFloder
	os.system(com1) 
	os.sytem(com2)
	os.system(com3)
    
t=[]
s=[]
t1=[]
s1=[]
t_cumulation=[]
cumulation=[]     #here only record the cumulation of migration src host
accum=0
SMALL_SIZE=15
MEDIUM_SIZE=18
BIGGER_SIZE=25

currentDT=str(datetime.now()).replace(" ","")
titleName=sys.argv[3]+"-"+sys.argv[4]+"_"+sys.argv[5]+"s"+"#"+currentDT
#conn=MySQLdb.connect(user="root",passwd="123",db="SDN",unix_socket="/opt/lampp/var/mysql/mysql.sock") 
conn = MySQLdb.connect(user="root",
                       passwd="123",
                       host="localhost",
                       db="SDN")
for j in range(len(sys.argv)-4):
    sql='SELECT * FROM %s' % sys.argv[j+1]
    cursor=excuteSql(sql,conn)
    rowNum=cursor.rowcount
    rec=cursor.fetchone()
    basetime=timeConvert(rec[1])
    if j == 0:
           dataXY(rec,basetime,t,s)
           t_cumulation.append(0)
           cumulation.append(0)

    else:
           dataXY(rec,basetime,t1,s1)  
   # print basetime
    for i in range(rowNum-1):
        record=cursor.fetchone()
        if j == 0:
           dataXY(record,basetime,t,s)
           acc=cumulation_func(record,basetime,t_cumulation,cumulation,accum)
           accum=acc
        else:
           dataXY(record,basetime,t1,s1)
#f=open("/home/xu/thesis_file/plot/cumulation.txt","w")

f=open("plot/"+titleName+"_cumulation.txt","w")
for i in range(len(t_cumulation)):
    f.write('%d %d\n' %(t_cumulation[i],cumulation[i]))
plt.rc('axes',labelsize=BIGGER_SIZE)
plt.rc('legend',fontsize=SMALL_SIZE)
plt.rc('xtick',labelsize=MEDIUM_SIZE)
plt.rc('ytick',labelsize=MEDIUM_SIZE)
#plt.rc('figure',titlesize=BIGGER_SIZE)
print "size of s: "
print len(s)
print " size of s1:"
print len(s1)
lines=plt.plot(t,s,'-r',t1,s1,'--b')
plt.setp(lines,linewidth=2.0)
plt.axis([min(t),200,min(min(s),min(s1)),max(max(s),max(s1))])
#plt.xticks(np.arange(mcain(t),250,50.0))
plt.xticks([10,50,100,150,200])
plt.legend(['source host','destination host'],loc='upper right')
plt.xlabel("time(s)")
plt.ylabel("bandwidth consumption(Mbps)")
#plt.suptitle("bandwidth policy",fontsize=BIGGER_SIZE)
#plt.suptitle(titleName,fontsize=BIGGER_SIZE)
#plt.savefig("/home/xu/thesis_file/plot/"+titleName+".png",bbox_inches='tight')
plt.savefig("plot/"+titleName+".png",bbox_inches='tight')
plt.show()
plt.clf()
plt.xlabel("time(s)")
plt.ylabel("cumulation throughput(kb)")
plt.plot(t_cumulation,cumulation,"-b")
plt.setp(lines,linewidth=3.0)
#plt.savefig("/home/xu/thesis_file/plot/"+titleName+"_cumulation.png",bbox_inches='tight')
plt.savefig("plot/"+titleName+"_cumulation.png",bbox_inches='tight')
f.close()
plt.show()


    
