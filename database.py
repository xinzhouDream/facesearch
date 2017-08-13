# -*- coding:utf-8 -*-
import sys
import sqlite3
from datetime import datetime

dbfile = 'facesearch.db'

class DBConnector:
    def __init__(self):
        self.dbfile = 'facesearch.db'
        self.conn = sqlite3.connect(self.dbfile)
        self.conn.text_factory = str
        self.cursor = self.conn.cursor()
    def getCursor(self):
        return self.cursor
    def commit(self):
        self.conn.commit()
    def close(self):
        self.conn.close()
# star_info
class StarInfo:
    def __init__(self):
        self.table_name = 'star_info'
        self.insert_sql = '''insert into %s VALUES (?,?,?,?)''' % (self.table_name)
        self.columns = {'id':'star_id', 'name':'star_name', 'des':'star_description'}
    def insert(self, data):
        conn = DBConnector()
        cursor = conn.getCursor();
        cursor.execute(self.insert_sql, data)
        conn.commit()
        conn.close()
    def insertAll(self, data_set):
        conn = DBConnector()
        cursor = conn.getCursor()
        if data_set is not None:
            for data in data_set:
                cursor.execute(self.insert_sql, data)
        conn.commit()
        conn.close()
    def getStarInfoById(self, star_id):
        info = []
        conn = DBConnector()
        cursor = conn.getCursor()
        sql = 'select * from %s where %s = ? ' % (self.table_name, self.columns['id'])
        cursor.execute(sql, (star_id,))
        res = cursor.fetchall()
        if len(res) > 0:
            info.append((res[0][2], res[0][3]))
        conn.close()
        return info

    def getStarInfoByName(self, star_name):
        info = []
        conn = DBConnector()
        cursor = conn.getCursor()
        sql = '''select * from %s where %s = ? ''' % (self.table_name, self.columns['name'])
        cursor.execute(sql, (star_name,))
        res = cursor.fetchall()
        for item in res:
            info.append((item[1], item[2]))
        conn.close()
        return info
# star_image
class StarImage:
    def __init__(self):
        self.table_name = 'star_image'
        self.insert_sql = ''' insert into %s values (?,?,?,?,?)''' % (self.table_name)
        self.columns={'id':'star_image_id', 'star_id':'star_id', 'image_id':'image_id', 'feat_id':'image_feat_id', 'path':'path'}
    def insert(self, data):
        conn = DBConnector()
        cursor = conn.getCursor()()
        cursor.execute(self.insert_sql, data)
        conn.commit()
        conn.close()
    def insertAll(self, data_set):
        conn = DBConnector()
        cursor = conn.getCursor()
        if data_set is not None:
            for data in data_set:
                cursor.execute(self.insert_sql, data)
        conn.commit()
        conn.close()
    def getAllFeatId(self):
        feats = []
        conn = DBConnector()
        cursor = conn.getCursor()
        sql = ''' select * from %s ''' % (self.table_name)
        cursor.execute(sql)
        res = cursor.fetchall()
        for item in res:
            feats.append(item[3])
        conn.close()
        return feats
    def getRowByFeatId(self, feat_id):
        conn = DBConnector()
        cursor = conn.getCursor()
        sql = ''' select * from %s where %s = ? ''' % (self.table_name, self.columns['feat_id'])
        cursor.execute(sql, (feat_id,))
        res = cursor.fetchall()
        conn.close()
        if len(res) > 0:
            item = res[0]
            star_id = item[1]
            image_id = item[2]
            feat_id = item[3]
            path = item[4]
            return (star_id, image_id, feat_id, path)
        else:
            return None
# video_info
class VideoInfo:
    def __init__(self):
        self.table_name = 'video_info'
        self.insert_sql = '''insert into %s values (?,?,?,?,?,?,?)''' % (self.table_name)
    def insert(self, data):
        conn = DBConnector()
        cursor = conn.getCursor()
        cursor.execute(self.insert_sql, data)
        conn.commit()
        conn.close()
    def insertAll(self, data_set):
        conn = DBConnector()
        cursor = conn.getCursor()
        if data_set is not None:
            for data in data_set:
                cursor.execute(self.insert_sql, data)
        conn.commit()
        conn.close()
    def getVideoInfoByStarId(self, star_id):
        videos = []
        conn = DBConnector()
        cursor = conn.getCursor()
        sql = "select * from " + self.table_name + " where star_id like '%#" + str(star_id) + "#%'" + " or star_id like '"+str(star_id)+ \
              "#%'" + " or star_id like '%#" + str(star_id) + "'"
        cursor.execute(sql)
        res = cursor.fetchall()
        for item in res:
            name = item[1]
            year = item[2]
            type = item[3]
            star_id = item[4]
            star_name = item[5]
            link = item[6]
            videos.append((name, year, type, star_name, link))
        conn.close()
        return videos

def insert(dbfile, record):
    try:
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO images (date,ip,url,score,sent,feat) VALUES (?,?,?,?,?,?)',
               (str(datetime.now()), record['ip'], record['url'], 0, 'null', 0))
        _id = cursor.lastrowid
        conn.commit()
        conn.close()
        return _id
    except Exception, e:
        print e
        return -1

def update(dbfile, record):
    try:
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()
        cursor.execute('UPDATE images SET score=?, sent=?, feat=? WHERE id=?', (record['score'], record['sent'], record['feat'], record['id']))
        conn.commit()
        conn.close()
        return 1
    except:
        print sys.exc_info()[0]
        return -1
   
def add_feedback(dbfile, record):
    try:
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()
        cursor.execute('UPDATE images SET user_rank=?, user_caption=? WHERE id=?', (record['user_rank'], record['user_caption'], record['id']))
        conn.commit()
        conn.close()
        return 1
    except:
        print sys.exc_info()[0]
        return -1

def getNewId(dbfile):
    try:
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()
        cursor.execute('select * from images')
        for row in cursor:
            if 'null' != row[5]:
                _id = row[0]
        print _id,cursor
    except:
        print sys.exc_info()[0]
    return _id



def browse(dbfile):
    res = []
    try:
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()
        cursor.execute('select * from images')
        for row in cursor:
            if 'null' != row[5]:
                res.append({'id':row[0], 'url':row[3], 'sent':row[5], 'user_rank':row[7],'user_caption':row[8]})
        conn.close()
        res.reverse()
    except:
        print sys.exc_info()[0]
    return res
        
        
if __name__ == '__main__':
    dbfile = 'facesearch.db'
    ''' 
    record = {'ip':'127.0.0.1', 'url':'http://222.29.193.170:9090/images/3960747333.jpg', 'sent':'hello world', 'score':1,'feat':'0'}
    _id = insert(dbfile, record)
    print _id
    record['id'] = _id
    #record['user_rank'] = '1'
    okay = update(dbfile, record)
    print '>'*5, okay
    print '*'*10
    print browse(dbfile)'''
    video = VideoInfo()
    res = video.getVideoInfoByStarId(2)
    print res
