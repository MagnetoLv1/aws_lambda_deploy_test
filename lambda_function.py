import pymysql
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time


# MySQL Connection 연결12
conn = pymysql.connect(host='database-1.chilgjy3o3zp.ap-northeast-2.rds.amazonaws.com', user='admin', password='epdlxjqpdltm-1',
                       db='innodb', charset='utf8')

# Connection 으로부터 Cursor 생성
curs = conn.cursor()

domain = 'http://www.slrclub.com'


def lambda_handler(event, context):

    # TODO implement
    req = requests.get('http://www.slrclub.com/bbs/zboard.php?id=free')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', id='bbs_list')

    trs = table.tbody.find_all('tr')

    data = []
    for tr in trs:
        if tr.find('td', class_='list_num') == None:
            continue

        num = tr.find('td', class_='list_num').string
        title = tr.find('td', class_='sbj').a.string
        url = domain + tr.find('td', class_='sbj').a['href']
        # comment222 = list(tr.find('td', class_='sbj').children)
        sbj = list(tr.find('td', class_='sbj').children)
        comment_cnt = str(
            sbj[len(sbj)-1].string).replace('[', '').replace(']', '').replace(' ', '')
        comment_cnt = 0 if comment_cnt == '' else comment_cnt
        writer = tr.find('td', class_='list_name').span.string
        list_date = tr.find('td', class_='list_date').string
        view_cnt = tr.find('td', class_='list_click').string

        writed_at = datetime.today().strftime('%Y-%m-%d ') + list_date

        data.append((
            1,
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

    sql = "insert into posts (site,title,description,url,image,like_cnt,view_cnt,comment_cnt,writer, writed_at) values (%s, %s, %s,%s, %s, %s,%s, %s, %s, %s)"

    # print(data)
    curs.executemany(sql, data)
    conn.commit()
    curs.close()
    conn.close()

    return {'statusCode': 200}


if __name__ == '__main__':
    lambda_handler(None, None)
