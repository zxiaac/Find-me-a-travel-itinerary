#!/usr/bin/python3 
       
import urllib.request
import re
import csv
import pymysql
import math

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
nameUrl=[]
curr=0
for j in range(1, 201):
	baseUrl = "http://travel.qunar.com/p-cs299914-beijing-jingdian-1-"+str(j)
	pagedata1 = urllib.request.urlopen(baseUrl).read().decode("utf-8", "ignore")
	nameUrlPat = '<a data-beacon="poi" target="_blank" class="titlink" href="(.*?)"><span class="cn_tit">(.*?)<span class="en_tit">(.*?)</span>'
  
	nameUrl += re.compile(nameUrlPat, re.S).findall(pagedata1)

	
	for i in range(curr, len(nameUrl)):
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
		startTime = -1
		endTime = -1
		if not len(nameUrl3)==0:		
			tempt = str(nameUrl3[0])
			if not bool(re.search(r'\d', tempt)): startTime=-1
			if tempt == '全天开放':
				startTime = 0
				endTime = 24
			
			ind = -1
			while True:
				#print(ind)
				ind = tempt.find('日',ind+1)
				if ind==-1:
					break
				elif tempt[ind+1]>='0' and tempt[ind+1]<='9' and tempt[ind+2]==':':
					startTime = int(tempt[ind+1])
					endTime = int(tempt[ind+6])*10+int(tempt[ind+7])
					break
				elif tempt[ind+1]>='0' and tempt[ind+1]<='9'and not tempt[ind+2]==':':
					startTime = int(tempt[ind+1])*10+int(tempt[ind+2])
					endTime = int(tempt[ind+7])*10+int(tempt[ind+8])
					break
				else:
					continue
			ind = -1
			if startTime==-1:
				while True:
					#print(ind)
					ind = tempt.find('）',ind+1)
					if ind==-1:
						break
					elif tempt[ind+1]>='0' and tempt[ind+1]<='9' and tempt[ind+2]==':':
						startTime = int(tempt[ind+1])
						endTime = int(tempt[ind+6])*10+int(tempt[ind+7])
						break
					elif tempt[ind+1]>='0' and tempt[ind+1]<='9'and not tempt[ind+2]==':':
						startTime = int(tempt[ind+1])*10+int(tempt[ind+2])
						endTime = int(tempt[ind+7])*10+int(tempt[ind+8])
						break
					else:
						continue
			ind = -1
			if startTime==-1:
				while True:
					#print(ind)
					ind = tempt.find('五',ind+1)
					if ind==-1:
						break
					elif tempt[ind+1]>='0' and tempt[ind+1]<='9' and tempt[ind+2]==':':
						startTime = int(tempt[ind+1])
						endTime = int(tempt[ind+6])*10+int(tempt[ind+7])
						break
					elif tempt[ind+1]>='0' and tempt[ind+1]<='9'and not tempt[ind+2]==':':
						startTime = int(tempt[ind+1])*10+int(tempt[ind+2])
						endTime = int(tempt[ind+7])*10+int(tempt[ind+8])
						break
					else:
						continue
			ind = -1
			if startTime==-1:
				while True:
					#print(ind)
					ind = tempt.find('间',ind+1)
					if ind==-1:
						break
					elif tempt[ind+1]>='0' and tempt[ind+1]<='9' and tempt[ind+2]==':':
						startTime = int(tempt[ind+1])
						endTime = int(tempt[ind+6])*10+int(tempt[ind+7])
						break
					elif tempt[ind+1]>='0' and tempt[ind+1]<='9'and not tempt[ind+2]==':':
						startTime = int(tempt[ind+1])*10+int(tempt[ind+2])
						endTime = int(tempt[ind+7])*10+int(tempt[ind+8])
						break
					else:
						continue
			if startTime==-1:
				if tempt[0]>='0' and tempt[0]<='9' and tempt[1]==':':
					startTime = int(tempt[0])
					endTime = int(tempt[5])*10+int(tempt[6])
				elif tempt[0]>='0' and tempt[0]<='9' and not tempt[1]==':':
					startTime = int(tempt[0])*10+int(tempt[1])
					endTime = int(tempt[6])*10+int(tempt[7])
		#opening hours

		nameUrlPat4 = '<dd class="e_now_price" ><span class="e_price_txt"><i class="rmb">&yen;</i>(.*?)</span>'
		nameUrl4 = re.compile(nameUrlPat4, re.S).findall(pagedata2)
		price = -1
		if len(nameUrl4)==0:
			price = 0
		else:
			price = int(nameUrl4[0])
		#price		

		
		#popularity	
		popularity = '<div class="ranking">.*?景点排名第<span class="sum">(.*?)</span>'
		popu = int(re.compile(popularity,re.S).findall(pagedata2)[0])
		pop = math.exp(-popu)

		
		
		db = pymysql.connect(host='cs336.cxonjz7sctxh.us-east-2.rds.amazonaws.com', user='Esther', password='938991Lsx', port=3306,  db='Travel',charset='utf8')
		

		cursor = db.cursor()
		#sql0 =" alter table attraction change attraction name varchar(45) character utf8;"
		'''
		if len(nameUrl4)==0 and len(nameUrl3)==0:
			sql = "insert into attraction(id,name,duration, city) values('"+str(i)+"','" +nameUrl[i][1]+"','" +str(dura[0])+"','" +"Beijing"+"')"	
		
		else:
			sql = "insert into attraction(id,name,duration, city,price, startTime,endTime) values('"+str(i)+"','" +nameUrl[i][1]+"','" +str(dura[0])+"','" +"Beijing"+"','" +str(nameUrl4[0])+"','" +startTime+"','" +endTime+"')"

		
		try:
			#cursor.execute(sql0)
			cursor.execute(sql)
			db.commit()
		except:
			db.rollback()
		db.close()'''
	curr =len(nameUrl)		

