import json
import requests
from bs4 import BeautifulSoup


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
        writer = tr.find('td', class_='list_name').span.string
        tm = tr.find('td', class_='list_date').string
        viewCnt = tr.find('td', class_='list_click').string
        #num = tr.prettify()

        data.append({
            'num': num,
            'title': title,
            'writer': writer,
            'tm': tm,
            'viewCnt': viewCnt
        })

    copy = soup.find('div', id='copy').prettify()
    sitename = soup.find('span', class_='sitename').string

    return {
        'statusCode': 200,
        'copy': copy,
        'body': sitename,
        'data': data,
    }
