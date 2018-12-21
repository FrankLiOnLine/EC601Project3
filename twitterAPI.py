#!/usr/bin/env python
# encoding: utf-8

import tweepy
import os
import requests
import shutil
import subprocess
import videoAnalysis as VA
from PIL import Image
from tqdm import tqdm
from ffmpy import FFmpeg

def read_keys():
    path = os.getcwd()
    path = path + '/keys.txt'
    f = open(path)
    data = f.readlines()
    key = []
    for line in data:
        key.append(line.replace('\n', ''))
    return key

def get_all_tweets(screen_name, n):

    key = read_keys()
    consumer_key = key[0]
    consumer_secret = key[1]
    access_key = key[2]
    access_secret = key[3]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    alltweets = []

    new_tweets = api.user_timeline(screen_name=screen_name, count=1)

    alltweets.extend(new_tweets)

    oldest = alltweets[-1].id - 1
    img_list = []
    pbar = tqdm(total=100)
    while len(new_tweets) > 0:
        new_tweets = api.user_timeline(screen_name=screen_name, count=1, max_id=oldest)
        try:
            data = new_tweets[0].entities.get('media',[])
            if data != []:
                img_add = data[0].pop('media_url')
                last_four = img_add[-4:]
                if last_four != '.jpg':
                    pass
                img_list.append(img_add)
                pbar.update(100/n)
        except AttributeError:
            pass
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        if (len(img_list) > n):
            break
    pbar.close()
    file = open('img_list.txt', 'w')
    for i in img_list:
        file.write(i)
        file.write('\n')
    print("Done")
    file.close()

    return img_list

def download_img(img_list):
    try:
        shutil.rmtree('pictures_downloaded')
    except FileNotFoundError:
        pass
    finally:
        path = os.getcwd()
        path = path + '/pictures_downloaded'
        folder = os.mkdir(path)
    counter = 0
    for i in img_list:
        img = requests.get(i).content
        if counter < 10:
            open(path + '/' + '0' + str(counter) + '.jpg', 'wb').write(img)
            counter += 1
        else:
            open(path + '/' + str(counter) + '.jpg', 'wb').write(img)
            counter += 1
    return path

def resize_img(path):
    names = os.listdir(path)
    for i in names:
        img = Image.open(path + '/' + i)
        out = img.resize((500,500))
        out.save(path + '/' + i)

def covert_to_video():
    subprocess.run(['ffmpeg', '-r', '1', '-i', 'pictures_downloaded/%02d.jpg', '-c:v', 'mpeg4', 'converted.mp4'])
    print('process done!')

def main(screen_name, n):
    img_list = get_all_tweets(screen_name, n)
    path = download_img(img_list)
    path = os.getcwd() + '/pictures_downloaded'
    resize_img(path)
    covert_to_video()
    time_offset = VA.main()
    return time_offset




if __name__ == '__main__':
    main("@nbc", 40)