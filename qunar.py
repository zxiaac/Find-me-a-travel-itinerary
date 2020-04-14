#!/usr/bin/python3 
       
import urllib.request
import re
import csv
import pymysql

config={
'host':'18.217.213.49',
'user':'Esther',
'password':'938991Lsx',
'db':'Travel',
'charset':'utf8'
}

course={}
       
headers = ("User-Agent",
"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400")
opener = urllib.request.build_opener()
opener.addheaders = [headers]
urllib.request.install_opener(opener)
for j in range(0, 200):
	baseUrl = "http://travel.qunar.com/p-cs299914-beijing-jingdian-1-"+str(j)
	pagedata1 = urllib.request.urlopen(baseUrl).read().decode("utf-8", "ignore")
	nameUrlPat = '<a data-beacon="poi" target="_blank" class="titlink" href="(.*?)"><span class="cn_tit">(.*?)<span class="en_tit">(.*?)</span>'
  
	nameUrl = re.compile(nameUrlPat, re.S).findall(pagedata1)


	with open('a.csv','w',newline='') as csv_file:    
		csv_writer = csv.writer(csv_file)  
		for i in range(0, len(nameUrl)):
			opener2 = urllib.request.build_opener()
			opener2.addheaders = [headers]
			urllib.request.install_opener(opener2)
			baseUrl2 = nameUrl[i][0]
			pagedata2 = urllib.request.urlopen(baseUrl2).read().decode("utf-8", "ignore")
			#pagedata2 = urllib.request.urlopen(baseUrl2)
			
			#duration
			duration = '<div class="time">建议游玩时间：(.*?)</div>'
			dura = re.compile(duration,re.S).findall(pagedata2)

			nameUrlPat3 = '<dt>开放时间:</dt>.*<dd><span><p>(.*?)</p></span></dd>'
			nameUrl3 = re.compile(nameUrlPat3, re.S).findall(pagedata2)
			#opening hours

			nameUrlPat4 = '<dd class="e_now_price" ><span class="e_price_txt"><i class="rmb">&yen;</i>(.*?)</span>'
			nameUrl4 = re.compile(nameUrlPat4, re.S).findall(pagedata2)
			#price			

			
			
			db = pymysql.connect(host='cs336.cxonjz7sctxh.us-east-2.rds.amazonaws.com', user='Esther', password='938991Lsx', port=3306,  db='Travel',charset='utf8')
			

			cursor = db.cursor()
			#sql0 =" alter table attraction change attraction name varchar(45) character utf8;"
			
			if len(nameUrl4)!=0:
				sql = "insert into attraction(id,name,duration, city, startTime) values('"+str(i)+"','" +nameUrl[i][1]+"','" +str(dura[0])+"','" +"Beijing"+"','" +nameUrl3[0]+"')"
			if len(nameUrl3)!=0:
				sql = "insert into attraction(id,name,duration, city,price) values('"+str(i)+"','" +nameUrl[i][1]+"','" +str(dura[0])+"','" +"Beijing"+"','" +str(nameUrl4[0])+"')"			
			
			sql = "insert into attraction(id,name,duration, city,price, startTime) values('"+str(i)+"','" +nameUrl[i][1]+"','" +str(dura[0])+"','" +"Beijing"+"','" +str(nameUrl4[0])+"','" +nameUrl3[0]+"')"
			try:
				#cursor.execute(sql0)
				cursor.execute(sql)
				db.commit()
			except:
				db.rollback()
			db.close()
			#csv_writer.writerow(nameUrl[i][1]+" "+nameUrl2[i][1])

