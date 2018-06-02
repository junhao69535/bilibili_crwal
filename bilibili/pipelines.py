# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class BilibiliPipeline(object):
    def __init__(self):
        self.conn=pymysql.connect(host="127.0.0.1",user="root",password="123456",db="bilibili")
        
    def process_item(self, item, spider):
        userid=item["userid"]
        sex=item["sex"]
        level=item["level"]
        vipType=item["vipType"]
        vipStatu=item["vipStatu"]
        coins=item["coins"]
        follows=item["follows"]
        fans=item["fans"]
        play_num=item["play_num"]
        UID=item["UID"]
        register_time=item["register_time"]
        birthday=item["birthday"]
        sql="insert into mybili(userid,sex,level,vipType,vipStatu,coins,follows,fans,play_num,UID,register_time,birthday) VALUES('"+userid+"','"+sex+"','"+level+"','"+vipType+"','"+vipStatu+"','"+coins+"','"+follows+"','"+fans+"','"+play_num+"','"+UID+"','"+register_time+"','"+birthday+"')"
        self.conn.query(sql)
        self.conn.commit()
        
        return item

    def close_spider(self,spider):
        self.conn.close()
