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
for j in range(1, 51):
	baseUrl = "http://travel.qunar.com/p-cs299878-shanghai-jingdian-1-"+str(j)
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
		
		#entit
		engliName = '<span class="entit">(.*?)</span>'
		engli = re.compile(engliName,re.S).findall(pagedata2)
		if len(engli)==0:
			entit = ''
		else:
			entit = engli[0]
		
		#duration
		duration = '<div class="time">建议游玩时间：(.*?)</div>'
		dura = re.compile(duration,re.S).findall(pagedata2)
		du = -1
		if not len(dura) == 0:
			du = dura[0]

		nameUrlPat3 = '<dt>开放时间:</dt>.*<dd><span><p>(.*?)</p></span></dd>'
		nameUrl3 = re.compile(nameUrlPat3, re.S).findall(pagedata2)
		startTime = -1
		endTime = -1
		if not len(nameUrl3)==0:		
			tempt = str(nameUrl3[0])
			if not bool(re.search(r'\d', tempt)): startTime=-1
			if tempt == '全天开放' or tempt == '24小时':
				startTime = 0
				endTime = 24
			
			if startTime==-1:
				if tempt[0]>='0' and tempt[0]<='9' and tempt[1]==':':
					startTime = int(tempt[0])
					if tempt[ind+6]=='-':
						endTime = int(tempt[6])*10+int(tempt[7])
					else:	
						endTime = int(tempt[5])*10+int(tempt[6])
				elif tempt[0]>='0' and tempt[0]<='9' and tempt[2]==':':
					startTime = int(tempt[0])*10+int(tempt[1])
					endTime = int(tempt[6])*10+int(tempt[7])
			
			ind = -1
			while True:
				#print(ind)
				ind = tempt.find('日',ind+1)
				if ind==-1:
					break
				elif tempt[ind+1]>='0' and tempt[ind+1]<='9' and tempt[ind+2]==':':
					startTime = int(tempt[ind+1])
					if tempt[ind+6]=='-':
						endTime = int(tempt[ind+7])*10+int(tempt[ind+8])
					else:	
						endTime = int(tempt[ind+6])*10+int(tempt[ind+7])
					break
				elif tempt[ind+1]>='0' and tempt[ind+1]<='9'and tempt[ind+3]==':':
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
					elif tempt[ind+1]>='0' and tempt[ind+1]<='9'and tempt[ind+3]==':':
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
					elif tempt[ind+1]>='0' and tempt[ind+1]<='9'and tempt[ind+3]==':':
						startTime = int(tempt[ind+1])*10+int(tempt[ind+2])
						endTime = int(tempt[ind+7])*10+int(tempt[ind+8])
						break
					else:
						continue
			
			ind = -1
			if startTime==-1:
				while True:
					#print(ind)
					ind = tempt.find('月',ind+1)
					if ind==-1:
						break
					elif tempt[ind+1]>='0' and tempt[ind+1]<='9' and tempt[ind+2]==':':
						startTime = int(tempt[ind+1])
						endTime = int(tempt[ind+6])*10+int(tempt[ind+7])
						break
					elif tempt[ind+1]>='0' and tempt[ind+1]<='9'and tempt[ind+3]==':':
						startTime = int(tempt[ind+1])*10+int(tempt[ind+2])
						endTime = int(tempt[ind+7])*10+int(tempt[ind+8])
						break
					else:
						continue

			ind = -1
			if startTime==-1:
				while True:
					#print(ind)
					ind = tempt.find(' ',ind+1)
					if ind==-1:
						break
					elif tempt[ind+1]>='0' and tempt[ind+1]<='9' and tempt[ind+2]==':':
						startTime = int(tempt[ind+1])
						endTime = int(tempt[ind+6])*10+int(tempt[ind+7])
						break
					elif tempt[ind+1]>='0' and tempt[ind+1]<='9'and tempt[ind+3]==':':
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
					elif tempt[ind+1]>='0' and tempt[ind+1]<='9'and tempt[ind+3]==':':
						startTime = int(tempt[ind+1])*10+int(tempt[ind+2])
						endTime = int(tempt[ind+7])*10+int(tempt[ind+8])
						break
					else:
						continue

			
		#opening hours

		nameUrlPat4 = '<dd class="e_now_price" ><span class="e_price_txt"><i class="rmb">&yen;</i>(.*?)</span>'
		nameUrl4 = re.compile(nameUrlPat4, re.S).findall(pagedata2)
		price = -1
		if len(nameUrl4)==0:
			price = 0
		else:
			price = int(float(nameUrl4[0]))
		#price		

		
		#popularity	
		popularity = '<div class="ranking">.*?景点排名第<span class="sum">(.*?)</span>'
		popu = re.compile(popularity,re.S).findall(pagedata2)
		pp = 10000000
		if not len(popu)==0:
			pp = int(popu[0])
		pop = math.exp(-pp)
		
		#natural
		nature = 0
		if 'Mountain' in entit:
			nature = 1
		if 'Wild' in entit:
			nature = 1
		if 'Natural' in entit:
			nature = 1
		if 'Forest' in entit:
			nature =1
		if 'Country' in entit:
			nature = 1
		if 'Park' in entit:
			nature = 1
		if 'Reservoir' in entit:
			nature = 1
		if 'Scenic' in entit:
			nature = 1
		if 'Lake' in entit:
			nature = 1
		if 'Gorge' in entit:
			nature = 1
		if 'Landscape' in entit:
			nature = 1
		if 'Hills' in entit:
			nature = 1
		if 'Farm' in entit:
			nature = 1
		if 'shan' in entit:
			nature = 1
		if 'Ridge' in entit:
			nature = 1
		if 'Grassland' in entit:
			nature = 1
		if 'Sea' in entit:
			nature = 1
		if 'Canyon' in entit:
			nature = 1
		if 'Reserve' in entit:
			nature = 1
		if 'Flower' in entit:
			nature = 1
		if 'Harbor' in entit:
			nature = 1
		if 'Island' in entit:
			nature = 1
		if 'Ecological' in entit:
			nature = 1
		
		#history
		history = 0
		if 'City' in entit:
			history = 1
		if 'Wall' in entit:
			history = 1
		if 'Square' in entit:
			history = 1
		if 'Palace' in entit:
			history = 1
		if 'xiang' in entit:
			history = 1
		if 'Town' in entit:
			history = 1
		if 'Old' in entit:
			history = 1
		if 'Temple' in entit:
			history = 1
		if 'Hutong' in entit:
			history =1
		if 'hai' in entit:
			history =1
		if 'Mansion' in entit:
			history = 1
		if 'Tombs' in entit:
			history = 1
		if 'Museum' in entit:
			history = 1
		if 'Ruins' in entit:
			history = 1
		if 'Mu' in entit:
			history = 1
		if 'Memorial' in entit:
			history = 1
		if 'Cave' in entit:
			history = 1
		if 'Ancient' in entit:
			history = 1

		#culture
		culture = 0
		if 'City' in entit:
			culture = 1
		if 'Wall' in entit:
			culture = 1
		if 'Palace' in entit:
			culture = 1
		if 'xiang' in entit:
			culture = 1
		if 'Town' in entit:
			culture = 1
		if 'Old' in entit:
			culture = 1
		if 'Street' in entit:
			culture = 1
		if 'Temple' in entit:
			culture = 1
		if 'Tower' in entit:
			culture = 1
		if 'Museum' in entit:
			culture = 1
		if 'Art' in entit:
			culture = 1
		if 'Hutong' in entit:
			culture = 1
		if 'Gallery' in entit:
			culture = 1
		if 'hai' in entit:
			culture = 1
		if 'Mansion' in entit:
			culture = 1
		if 'Park' in entit:
			culture = 1
		if 'cun' in entit:
			culture = 1
		if 'Alley' in entit:
			culture = 1
		if 'University' in entit:
			culture = 1
		if 'Village' in entit:
			culture = 1
		if 'National' in entit:
			culture = 1
		if 'Bridge' in entit:
			culture = 1
		if 'Memorial' in entit:
			culture = 1
		if 'Church' in entit:
			culture = 1
		if 'Lane' in entit:
			culture = 1
		if 'Bund' in entit:
			culture = 1
		if 'fang' in entit:
			culture = 1
		if 'Television Tower' in entit:
			culture = 1
		if 'Nong' in entit:
			culture = 1
		if 'Road' in entit:
			culture = 1
		if 'Cultural' in entit:
			culture = 1
		if 'Square' in entit:
			culture = 1
		if 'Sinan' in entit:
			culture = 1
		if 'Fengqing' in entit:
			culture = 1
		

		#outdoor
		outdoor = 0
		if 'Great Wall' in entit:
			outdoor = 1
		if 'Mountain' in entit:
			outdoor = 1
		if 'Happy Valley' in entit:
			outdoor = 1
		if 'Wetland' in entit:
			outdoor = 1
		if 'Gorge' in entit:
			outdoor = 1
		if 'Hills' in entit:
			outdoor = 1
		if 'shan' in entit:
			outdoor = 1
		if 'Forest' in entit:
			outdoor = 1
		if 'Grassland' in entit:
			outdoor = 1


		#amusement
		amuse = 0
		if 'Happy Valley' in entit:
			amuse = 1
		if 'Zoo' in entit:
			amuse = 1
		if 'Botanical Garden' in entit:
			amuse = 1
		if 'Wildlife' in entit:
			amuse = 1
		if 'World Park' in entit:
			amuse = 1
		if 'Sea World' in entit:
			amuse = 1
		if 'Madame Tussauds' in entit:
			amuse = 1
		if 'Garden' in entit:
			amuse = 1
		if 'Amusement' in entit:
			amuse = 1
		if 'Aquarium' in entit:
			amuse = 1
		if 'Underwater' in entit:
			amuse = 1
		if 'Disney' in entit:
			amuse = 1
		if 'Ocean Park' in entit:
			amuse = 1
		if 'Wild Animal' in entit:
			amuse = 1
		if 'Ocean World' in entit:
			amuse = 1
		

		#shopping
		shopping = 0
		if 'Street' in entit:
			shopping = 1
		if 'Sanlitun' in entit:
			shopping = 1
		if 'Wangfujing' in entit:
			shopping = 1
		if 'Commercial' in entit:
			shopping = 1
		if 'Bund' in entit:
			shopping = 1
		if 'Lujiazui' in entit:
			shopping = 1
		if 'Pedestrian' in entit:
			shopping = 1
		if 'Financial Center' in entit:
			shopping = 1


		#activity
		activity = 0
		if 'Cruise' in entit:
			activity = 1

		#other
		other = 0
		if nature ==0 and history ==0 and culture ==0 and outdoor ==0 and amuse==0 and shopping ==0 and activity ==0:
			other = 1
		
		
		db = pymysql.connect(host='cs336.cxonjz7sctxh.us-east-2.rds.amazonaws.com', user='Esther', password='938991Lsx', port=3306,  db='Travel',charset='utf8')
		
		
		cursor = db.cursor()
		#sql0 =" alter table attraction change attraction name varchar(45) character utf8;"
		print(str(i)+','+nameUrl[i][1])
	
		sql = "insert into ShanghaiAttr(id,name,duration, city,price, startTime,endTime,popularity,nature,history,culture,outdoor,amusementPark,shopping,acitivity,other) values('"+str(i)+"','" +nameUrl[i][1]+"','" +str(du)+"','" +"Shanghai"+"','" +str(price)+"','" +str(startTime)+"','" +str(endTime)+"','" +str(pop)+"','" +str(nature)+"','" +str(history)+"','" +str(culture)+"','" +str(outdoor)+"','" +str(amuse)+"','" +str(shopping)+"','" +str(activity)+"','" +str(other)+"')"

		
		try:
			#cursor.execute(sql0)
			cursor.execute(sql)
			
			db.commit()
		except:
			db.rollback()
		db.close()

	curr =len(nameUrl)		

