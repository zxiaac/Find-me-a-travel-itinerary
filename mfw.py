#!/usr/bin/env python3
# -*- coding: utf-8 -*

import base64
import configparser
import hashlib
import json
import logging
import re
import time
import random
from io import BytesIO

import exifread
import pymysql
import requests
from bs4 import BeautifulSoup

'''
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='weibo.log',
                    filemode='a')
'''

conn = pymysql.connect(host='cs336.cxonjz7sctxh.us-east-2.rds.amazonaws.com', user='Esther', password='938991Lsx', port=3306,  db='Travel',charset='utf8')

cursor = conn.cursor()


#insert_blog_sql = (
#    "INSERT IGNORE INTO gulangyu.mafengwo_blog(user_name, create_time, blog, star, comment_id, scenery) VALUES('{user_name}', '{create_time}','{blog}','{star}','{comment_id}', '{scenery}')"
#)

#insert_pic_sql = (
#    "INSERT IGNORE INTO gulangyu.mafengwo_pics(pic_url, pic_bin, md5, exif, scenery) VALUES ('{pic_url}','{pic_bin}','{md5}','{exif}', '{scenery}')"
#)

#insert_relationship_sql = (
#    "INSERT IGNORE INTO gulangyu.mafengwo_relationship(id, md5, scenery) VALUES ('{id}','{md5}', '{scenery}')"
#)
'''
url = 'http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?callback=jQuery18105332634542482972_1511924148475&params=%7B%22poi_id%22%3A%22{href}%22%2C%22page%22%3A{num}%2C%22just_comment%22%3A1%7D'
'''
#url ='http://www.mafengwo.cn/ajax/router.php?sAct=KMdd_pagelet_commentApi%7CDelComment'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
Connection = 'keep-alive'
cookie = 'mfw_uuid=5db6cdad-c611-a123-f224-0a89714255dd; __omc_chl=; UM_distinctid=16e12137d2c21c-0252e19c46dac-b363e65-1fa400-16e12137d2d96e; uva=s%3A150%3A%22a%3A4%3A%7Bs%3A13%3A%22host_pre_time%22%3Bs%3A10%3A%222019-10-28%22%3Bs%3A2%3A%22lt%22%3Bi%3A1572261294%3Bs%3A10%3A%22last_refer%22%3Bs%3A23%3A%22https%3A%2F%2Fwww.google.com%2F%22%3Bs%3A5%3A%22rhost%22%3Bs%3A14%3A%22www.google.com%22%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1572261294%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A14%3A%22www.google.com%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=5db6cdad-c611-a123-f224-0a89714255dd; PHPSESSID=a0gahmfdmpk417rs8fuogr7fk5; mafengwo=20417a1c317c4b6290108b94d5d771be_64521739_5db820f93ff104.73094306_5db820f93ff137.57173562; mfw_uid=64521739; oad_n=a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222019-11-03+10%3A47%3A23%22%3B%7D; _r=csdn; _rp=a%3A2%3A%7Bs%3A1%3A%22p%22%3Bs%3A49%3A%22blog.csdn.net%2Fu011291072%2Farticle%2Fdetails%2F81266372%22%3Bs%3A1%3A%22t%22%3Bi%3A1572749476%3B%7D; __mfwothchid=referrer%7Cblog.csdn.net; __mfwc=referrer%7Cblog.csdn.net; __mfwa=1572261297343.38275.9.1572696425862.1572749479319; __mfwlv=1572749479; __mfwvn=8; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1572409487,1572620240,1572696428,1572749480; CNZZDATA30065558=cnzz_eid%3D533296727-1572259954-null%26ntime%3D1572747844; __omc_r=; Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1572749533; uol_throttle=64521739; RT="sl=0&ss=1572696445351&tt=0&obo=0&sh=&dm=mafengwo.cn&si=1e793c74-80bf-4d3b-bc56-18dd247785d0&r=http%3A%2F%2Fwww.mafengwo.cn%2Fjd%2F10065%2Fgonglve.html&ul=1572750779464&hd=1572750780369"; __mfwb=59891d71d52e.3.direct; __mfwlt=1572750776'

#headers = {
#    'User-Agent': user_agent,
#    'Cookie': cookie,
#    'Connection': Connection
#}
headers ={
'Host': 'www.mafengwo.cn',
'Connection': 'keep-alive',
'Content-Length': '101',
'Accept': 'application/json, text/javascript, */*; q=0.01',
'Origin': 'http://www.mafengwo.cn',
'X-Requested-With': 'XMLHttpRequest',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Referer': 'http://www.mafengwo.cn/jd/10065/gonglve.html',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cookie': 'mfw_uuid=5db6cdad-c611-a123-f224-0a89714255dd; __omc_chl=; UM_distinctid=16e12137d2c21c-0252e19c46dac-b363e65-1fa400-16e12137d2d96e; uva=s%3A150%3A%22a%3A4%3A%7Bs%3A13%3A%22host_pre_time%22%3Bs%3A10%3A%222019-10-28%22%3Bs%3A2%3A%22lt%22%3Bi%3A1572261294%3Bs%3A10%3A%22last_refer%22%3Bs%3A23%3A%22https%3A%2F%2Fwww.google.com%2F%22%3Bs%3A5%3A%22rhost%22%3Bs%3A14%3A%22www.google.com%22%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1572261294%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A14%3A%22www.google.com%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=5db6cdad-c611-a123-f224-0a89714255dd; PHPSESSID=a0gahmfdmpk417rs8fuogr7fk5; mafengwo=20417a1c317c4b6290108b94d5d771be_64521739_5db820f93ff104.73094306_5db820f93ff137.57173562; mfw_uid=64521739; oad_n=a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222019-11-03+10%3A47%3A23%22%3B%7D; _r=csdn; _rp=a%3A2%3A%7Bs%3A1%3A%22p%22%3Bs%3A49%3A%22blog.csdn.net%2Fu011291072%2Farticle%2Fdetails%2F81266372%22%3Bs%3A1%3A%22t%22%3Bi%3A1572749476%3B%7D; __mfwothchid=referrer%7Cblog.csdn.net; __mfwc=referrer%7Cblog.csdn.net; __mfwa=1572261297343.38275.9.1572696425862.1572749479319; __mfwlv=1572749479; __mfwvn=8; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1572409487,1572620240,1572696428,1572749480; CNZZDATA30065558=cnzz_eid%3D533296727-1572259954-null%26ntime%3D1572747844; __omc_r=; Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1572749533; uol_throttle=64521739; RT="sl=0&ss=1572696445351&tt=0&obo=0&sh=&dm=mafengwo.cn&si=1e793c74-80bf-4d3b-bc56-18dd247785d0&r=http%3A%2F%2Fwww.mafengwo.cn%2Fjd%2F10065%2Fgonglve.html&ul=1572750779464&hd=1572750780369"; __mfwb=59891d71d52e.3.direct; __mfwlt=1572750776'
}



def handle_pic(pic_url):
    try:
        large_bin = requests.get(pic_url, timeout=(10, 10))
        return large_bin.content
    except:
        logging.warning('img not get')
        print('img not get')
        return None


def get_param():
    total = []
    router_url = 'http://www.mafengwo.cn/ajax/router.php'
    base_url = 'http://www.mafengwo.cn'
    for num in range(1, 6):
        params = {
            'sAct': 'KMdd_StructWebAjax|GetPoisByTag',
            'iMddid': 10065,
            'iTagId': 0,
            'iPage': num
        }
        #pos = requests.post(url=router_url, data=params, headers=headers).json()
        pos = requests.post(url=router_url,data=params,headers=headers)
        print(pos.status_code)
        if pos.content:
            print(pos.text)
            pos = pos.json()
            soup_pos = BeautifulSoup(pos['data']['list'], 'lxml')

            result = [{'scenery': p['title'], 'href': re.findall(re.compile(r'/poi/(\d+).html'), p['href'])[0]} for p in
                  soup_pos.find_all('a')]
            total.extend(result)

    return total

#######
def get_dl_info(infos, info_name):
    for info in infos:
        if None != info.dt:
            info_title = info.dt.text
            if info_name in info_title:
                return info.dd.text
    return ''



def get_comment(href, num, name):
    new_url = url.format(href=href, num=num)
    req = requests.get(new_url, headers=headers)
    print(req.status_code)
    back = req.content.decode('utf-8')
    p = re.compile('\((.*?)}}\)')
    html = json.loads(p.findall(back)[0] + "}}")['data']['html']

    soup = BeautifulSoup(html, 'lxml')

    #################
    html_context = urlrequest.urlopen(poi_url).read()
    soup = BeautifulSoup(html_context, 'html.parser')  
    poi_summary = ''
    if None != soup.find(class_="summary"):
        poi_summary = soup.find(class_="summary").text.replace(" ", "")

    poi_time = ''
    if None != soup.find(class_="item-time"):
        poi_time = soup.find(class_="item-time").text


    infos = soup.findAll({'dl'})

    poi_traffic = get_dl_info(infos, '交通')

    poi_ticket = get_dl_info(infos, '门票')

    poi_open_time = get_dl_info(infos, '开放时间')

    sql = "insert into attraction(id,name) values('"+str(num)+"','" +name+"')"
    cursor.execute(sql)
    conn.commit()
    ####################
    '''
    star_all = soup.find_all('span', {'class': re.compile(r's-star s-star\d')})
    blog_all = soup.find_all('p', {'class': 'rev-txt'})
    create_time_all = soup.find_all('span', {'class': 'time'})
    comment_id_all = soup.find_all('textarea')

    for i in range(len(star_all)):
        star = star_all[i]['class'][1][-1]
        blog = blog_all[i].text.replace('\'', '\'\'')
        create_time = create_time_all[i].text
        comment_id = comment_id_all[i]['data-comment_id']
        user_name = comment_id_all[i]['data-comment_username']

        print(insert_blog_sql.format(user_name=user_name, create_time=create_time, blog=blog, star=star,
                                     comment_id=comment_id, scenery=name))

        cursor.execute(insert_blog_sql.format(user_name=user_name, create_time=create_time, blog=blog, star=star,
                                              comment_id=comment_id, scenery=name))
        conn.commit()


    include_img = [img.next_sibling.next_sibling for img in blog_all if
                   img.find_next_sibling('div')['class'][0] == 'rev-img']

    have_img_uid = [img.find_previous_siblings('a')[1]['data-id'] for img in blog_all if
                    img.find_next_sibling('div')['class'][0] == 'rev-img']

    for index in range(len(have_img_uid)):
        pic_urls = [i.img['src'] for i in include_img[index].find_all('a')]
        id = have_img_uid[index]

        for pic_url in pic_urls:

            print(pic_url)
            pic_bin = handle_pic(pic_url)
            if pic_bin == None:
                pass
            else:

                pic_file = BytesIO(pic_bin)  
                tag1 = exifread.process_file(pic_file, details=False, strict=True)
                tag = {}
                for key, value in tag1.items():
                    if key not in (
                            'JPEGThumbnail', 'TIFFThumbnail', 'Filename',
                            'EXIF MakerNote'):  
                        tag[key] = str(value)
                tags = json.dumps(tag)  

                MD5 = hashlib.md5(pic_file.read()).hexdigest()

                judge_pics = (
                    "SELECT md5 FROM gulangyu.mafengwo_pics WHERE md5 = '{md5}' LIMIT 1"
                )

                cursor.execute(judge_pics.format(md5=MD5))
                pic_md5 = cursor.fetchone()

                if pic_md5 is None:
                    cursor.execute(
                        insert_pic_sql.format(
                            pic_url=pic_url,
                            pic_bin=str(base64.b64encode(pic_bin))[2:-1], md5=MD5,
                            exif=tags, scenery=name))
                else:
                    logging.warning("Duplicate  " + pic_md5[0])

                cursor.execute(insert_relationship_sql.format(id=id, md5=MD5, scenery=name))
                conn.commit()
	'''

if __name__ == '__main__':
    result = get_param()

    for data in result:
        href = data['href']
        name = data['scenery']
        for i in range(1, 340):
            time.sleep(random.choice(range(1, 5)))
            get_comment(href=href, name=name, num=i)
