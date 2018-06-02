# -*- coding: utf-8 -*-
import scrapy
from bilibili.settings import UAPOOL
from bilibili.items import BilibiliItem
from scrapy.http import Request
from scrapy.http import FormRequest
import json
import time
import urllib.request
import urllib.error
import random

class BiliSpider(scrapy.Spider):
    name = 'bili'
    allowed_domains = ['bilibili.com']

    def start_requests(self):
        url1='https://space.bilibili.com/ajax/member/GetInfo'
        
        for uid in range(50000,200000):        
            headers={
                    'User-Agent':random.choice(UAPOOL),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
                    'Connection': 'keep-alive',
                    'Referer':'http://space.bilibili.com/'+str(uid),
                    'X-Requested-With': 'XMLHttpRequest',
                    'Origin': 'http://space.bilibili.com',
                    'Host': 'space.bilibili.com',
                    'Accept-Encoding':'gzip, deflate, br',
                    'Content-Type':'application/x-www-form-urlencoded'
                    }
            postdata={'mid': str(uid),'csrf':'',}        
            #处理基本信息
            yield scrapy.FormRequest(url1,headers=headers,formdata=postdata,\
                                 callback=self.user1_parse)
        
    def user1_parse(self, response):
        item=BilibiliItem()
        datas=json.loads(response.body)
        if response.status==200 and datas['status']!=False:
            data=datas['data']
            item["birthday"]=str(data["birthday"]) if "birthday" in data.keys() else "null"
            item["userid"]=data["name"] if "name" in data.keys() else "null"
            item["sex"]=data["sex"] if "sex" in data.keys() else "null"
            item["level"]=str(data["level_info"]["current_level"]) if "level_info" in data.keys() else "null"
            item["coins"]=str(data["coins"]) if "coins" in data.keys() else "null"
            item["vipType"] = str(data['vip']['vipType']) if "vip" in data.keys() else "null"
            item["vipStatu"] = str(data['vip']['vipStatus']) if "vip" in data.keys() else "null"
            if "regtime" in data.keys():               
                regtimestamp=data['regtime'] 
                regtime_local = time.localtime(regtimestamp)
                regtime = time.strftime("%Y-%m-%d %H:%M:%S",regtime_local)
                item["register_time"]=regtime
            else:
                item["register_time"]="null"
            item["UID"]=str(data["mid"]) if "mid" in data.keys() else "null"
            #opener
            opener=urllib.request.build_opener()
            opener.addheaders=[('User-Agent',random.choice(UAPOOL)),\
                               ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),\
                               ('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4'),\
                               ('Connection', 'keep-alive'),\
                               ('Referer','http://space.bilibili.com/'+str(data["mid"])),\
                               ('X-Requested-With', 'XMLHttpRequest'),\
                               ('Origin', 'http://space.bilibili.com'),\
                               ('Host', 'space.bilibili.com'),\
                               ('Accept-Encoding','gzip, deflate, br'),\
                               ('Content-Type','application/x-www-form-urlencoded')]
            urllib.request.install_opener(opener)
            
            #处理关注数和粉丝数
            url2='https://api.bilibili.com/x/relation/stat?vmid='+str(data["mid"])
            try:
                datas2=json.loads(urllib.request.urlopen(url2).read())
                item["follows"]=str(datas2['data']['following']) if "following" in datas2["data"].keys() else "null"
                item["fans"]=str(datas2['data']['follower'])  if "follower" in datas2["data"].keys() else "null"
            except urllib.error.URLError as e:
                item["follows"]='null'
                item["fans"]='null'
                if hasattr(e,"code"):
                    print(e.code)
                if hasattr(e,"reason"):
                    print(e.reason)

            #处理播放数
            url3='https://api.bilibili.com/x/space/upstat?mid='+str(data["mid"])
            try:
                datas3=json.loads(urllib.request.urlopen(url3).read())
                item["play_num"]=str(datas3['data']['archive']['view']) if "archive" in datas3["data"].keys() else "null"
            except urllib.error.URLError as e:
                item["play_num"]='null'
                if hasattr(e,"code"):
                    print(e.code)
                if hasattr(e,"reason"):
                    print(e.reason)
            #测试数据类型
            #print("userid:",type(item["userid"]))
            #print("sex:",type(item["sex"]))
            #print("level:",type(item["level"]))
            #print("vipType:",type(item["vipType"]))
            #print("vipStatu:",type(item["vipStatu"]))
            #print("coins:",type(item["coins"]))
            #print("follows:",type(item["follows"]))
            #print("fans:",type(item["fans"]))
            #print("play_num:",type(item["play_num"]))
            #print("UID:",type(item["UID"]))
            #print("register_time:",type(item["register_time"]))
            #print("birthday:",type(item["birthday"]))
            yield item
        else:
            return None

