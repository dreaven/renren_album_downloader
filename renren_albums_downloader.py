# -*- coding: utf-8 -*-
# renren_albums_downloader.py

''' a python 3 script to login to renren and download user's photos 
Quan Geng, gengquanshine@gmail.com
May 10, 2015
'''

import requests, re, shutil, os

renren_email = "YOUR_EMAIL_ADDRESS"        # the email address associated to your renren account
renren_password = "YOUR_PASSWORD"          # your renren login password, please fill in here
friend_id = "28735622"                     # your friend's renren account number. He/Her home page is http://www.renren.com/$friend_id
photo_folder = "."                         # this is the where you want to store the photos


payload = {"email": renren_email, "password": renren_password}
renren_login_url = "http://www.renren.com/PLogin.do"
s = requests.Session()         
a = s.post(renren_login_url, data=payload)

friend_info_url = "http://www.renren.com/" + friend_id + "/profile?v=info_timeline"
friend_albums_url = "http://photo.renren.com/photo/" + friend_id + "/albumlist/v7#"
albums_page = s.get(friend_albums_url)

album_name_id_list = re.findall(r'"albumName":"(?:[^"]|"")*","albumId":"(?:[^"]|"")*"',albums_page.text)
for line in album_name_id_list:
    quotes =  re.findall(r'"(?:[^"]|"")*"', line)
    album_name = quotes[1][1:(len(quotes[1])-1)]
    album_id = quotes[3][1:(len(quotes[3])-1)]
    album_url = "http://photo.renren.com/photo/" + friend_id +  "/album-" + album_id +"/v7"
    albums_page = s.get(album_url)

    print (album_name, album_id)

    folder_path= os.path.join(photo_folder, friend_id, album_name) 
    if not os.path.exists (folder_path) :
        os.makedirs(folder_path)

    photolist_block = re.findall("photoList\':.*.jpg\"}\],", albums_page.text)
    if not photolist_block:
        continue;
    photo_urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', photolist_block[0])
    print (folder_path)
    counter = -1
    for url in photo_urls:
        counter = counter + 1
        image_name = os.path.join(folder_path, 'img%d.jpg'%counter)
        print (image_name)
        if os.path.exists(image_name):
            continue;
        print (url)
        response = s.get(url, stream=True)
        with open(image_name, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)       
        del response
        
