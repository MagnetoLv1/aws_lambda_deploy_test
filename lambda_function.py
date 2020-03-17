import pymysql
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re


# MySQL Connection 연결12
conn = pymysql.connect(host='database-1.chilgjy3o3zp.ap-northeast-2.rds.amazonaws.com', user='admin', password='epdlxjqpdltm-1',
                       db='innodb', charset='utf8')

# Connection 으로부터 Cursor 생성

domain = 'http://www.slrclub.com'

regex = re.compile(r'^([0-9]{2}):([0-9]{2}):([0-9]{2})$')


def getExtractData(soup):
    is_break = False
    data = []
    table = soup.find('table', id='bbs_list')
    trs = table.tbody.find_all('tr')
    next_url = soup.find('table', id='bbs_foot').find(
        'a', class_="next1")['href']

    for tr in trs:
        if tr.find('td', class_='list_num') == None:
            continue
        if tr.find('td', class_='list_num').string == None:
            continue

        num = tr.find('td', class_='list_num').string
        title = tr.find('td', class_='sbj').a.string
        url = domain + tr.find('td', class_='sbj').a['href']
        sbj = list(tr.find('td', class_='sbj').children)
        comment_cnt = str(
            sbj[len(sbj)-1].string).replace('[', '').replace(']', '').replace(' ', '')
        comment_cnt = 0 if comment_cnt == '' else comment_cnt
        writer = tr.find('td', class_='list_name').span.string
        list_date = tr.find('td', class_='list_date').string
        view_cnt = tr.find('td', class_='list_click').string

        if regex.match(list_date) is None:
            next_url = None
            break
        else:
            writed_at = datetime.today().strftime('%Y-%m-%d ') + list_date

        data.append((
            1,
            num,
            title,
            '',
            url,
            '',
            0,
            view_cnt,
            comment_cnt,
            writer,
            writed_at
        ))

    save(data)
    return next_url


def save(data):
    curs = conn.cursor()
    sql = "insert into posts (site,num, title,description,url,image,like_cnt,view_cnt,comment_cnt,writer, writed_at) values (%s, %s, %s, %s,%s, %s, %s,%s, %s, %s, %s) ON DUPLICATE KEY UPDATE view_cnt = VALUES(view_cnt), comment_cnt = VALUES(comment_cnt)"
    curs.executemany(sql, data)
    conn.commit()
    curs.close()


def lambda_handler(event, context):

    # TODO implement
    next_url = '/bbs/zboard.php?id=free&page=714465'

    while True:
        url = domain + next_url
        print(url)
        req = requests.get(url,
                           headers={'User-agent': 'AdsBot-Google (+http://www.google.com/adsbot.html)'})
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        next_url = getExtractData(soup)
        if next_url == None:
            break

    conn.close()

    return {'statusCode': 200}


if __name__ == '__main__':
    lambda_handler(None, None)
