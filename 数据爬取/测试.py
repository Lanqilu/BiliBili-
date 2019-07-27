import json
import os

from functions.date_fuc import date
from functions.get_url_fuc import get_url

url = "http://www.bilibili.com/video/av60680876"
res = get_url(url, "text")
print(res)
# print(aid_change())
