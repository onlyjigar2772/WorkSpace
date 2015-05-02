#!/usr/bin/python
# __author__ = 'Jigar'
import random
import urllib.request


def download_web_image(url):
    name = random.randrange(1, 1000)
    full_name = str(name) + ".jpg"
    urllib.request.urlretrive(url, full_name)

download_web_image("https://www.thenewboston.com/photos/users/47625/resized/8332441c73850beed5ec89c0eb96c522.jpg")





