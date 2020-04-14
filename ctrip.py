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
for j in range(0, 336):
	baseUrl = "https://you.ctrip.com/sight/beijing1/s0-p"+str(j)+".html"
	pagedata1 = urllib.request.urlopen(baseUrl).read().decode("utf-8", "ignore")
	nameUrlPat = '<dt>\n.*?<a target="_blank" href="(.*?)" title=".*?">(.*?)</a>'
	nameUrlPat2 = '<dt>\n.*?<dd class="ellipsis">(.*?)</dd>'
  
	nameUrl = re.compile(nameUrlPat, re.S).findall(pagedata1)
	nameUrl2 = re.compile(nameUrlPat2, re.S).findall(pagedata1)


	with open('a.csv','w',newline='') as csv_file:    
		csv_writer = csv.writer(csv_file)  
		for i in range(0, len(nameUrl)):
			opener2 = urllib.request.build_opener()
			opener2.addheaders = [headers]
			urllib.request.install_opener(opener2)
			baseUrl2 = "https://you.ctrip.com"+nameUrl[i][0]
			#nameUrl[i][0]
			

			pagedata2 = urllib.request.urlopen(baseUrl2).read().decode("utf-8", "ignore")
			nameUrlPat3 = '</em><span data-reactid="51">(.*?)</span>'
			nameUrl3 = re.compile(nameUrlPat3, re.S).findall(pagedata2)
			#opening hours
			nameUrlPat4 = '</dfn><strong class="ttd-fs-24" data-reactid=.*?>(.*?)</strong>'
			nameUrl4 = re.compile(nameUrlPat4, re.S).findall(pagedata2)
			#price			

			print(nameUrl[i][1])
			print(nameUrl2[i])
			if len(nameUrl3)!=0:
				print(nameUrl3[0])
			if len(nameUrl4)!=0:
				print(nameUrl4[0])
			
			db = pymysql.connect(host='cs336.cxonjz7sctxh.us-east-2.rds.amazonaws.com', user='Esther', password='938991Lsx', port=3306,  db='Travel',charset='utf8')
			cursor = db.cursor()
			#sql0 =" alter table attraction change attraction name varchar(45) character utf8;"
			sql = "insert into attraction(id,name,duration,startTime,price) values('"+str(i)+"','" +nameUrl[i][1]+"','" +nameUrl3[i]+"','" +nameUrl4[i]+"')"
			try:
				#cursor.execute(sql0)
				cursor.execute(sql)
				db.commit()
			except:
				db.rollback()
			db.close()
			#csv_writer.writerow(nameUrl[i][1]+" "+nameUrl2[i][1])

