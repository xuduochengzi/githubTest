# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import requests
import time
import json


header = {
    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4'
}

url = 'http://bj.xiaozhu.com/search-duanzufang-p1-0/'

mb_data = requests.get(url, header)
soup = BeautifulSoup(mb_data.text, 'lxml')
images = soup.select('img[class="lodgeunitpic"]')
titles = soup.select('div.result_btm_con.lodgeunitname > div > a > span')
prices = soup.select('span[class="result_price"]')
ownerurls = soup.select('a.="search_result_gridsum"')
locationurls = soup.select('a[class="resule_img_a"]')
info = []
for image, title, price, ownerurl, locationurl in zip(images, titles, prices, ownerurls, locationurls):
        data = {
            'image': image.get('lazy_src'),
            'title': title.get_text(),
            'price': price.get_text(),
            'ownerurl': ownerurl.get('href'),
            'locationurl': locationurl.get('href')
        }
        location_url = data['locationurl']
        location_data = requests.get(location_url, header)
        location_soup = BeautifulSoup(location_data.text, 'lxml')
        locations = location_soup.select('span[class="pr5"]')
        for location in locations:
            locationdata={
                'location':  location.get_text().rstrip()
            }
        data.update(locationdata)


        owner_url = data['ownerurl']
        owner_data = requests.get(owner_url,header)
        owner_soup = BeautifulSoup(owner_data.text, 'lxml')
        owner_images = owner_soup.select('body > div.contentFD > div.left_sider.clearfix > div.person_infor > div.fd_img > img')
        owner_sexs = owner_soup.select('li[class="naborT"]')
        owner_names = owner_soup.select('div[class="fd_name"]')
        #print owner_images
        #print owner_sexs
        #print owner_names
        '''
        for owner_image,owner_sex,owner_name in zip(owner_images,owner_sexs,owner_names):
            owner_data2 = {
                'owner_image': owner_image.get('src'),
                'owner_sex' : owner_sex.get_text(),
                'owner_name': owner_name.get_text()
                }
        data.update(owner_data2)
        '''
        info.append(data)
print json.dumps(info, encoding="UTF-8", ensure_ascii=False)







