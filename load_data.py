# -*- coding:utf-8 -*-
import sys
from database import StarInfo
from database import StarImage
from database import VideoInfo

def loadStarInfo():
    starInfo = StarInfo()
    data_set =[
        (None, 'fbb', '范冰冰', '明星'),
        (None, 'ls', '李晟', '演员'),
        (None, 'lc_1', '李晨', '主持人'),
        (None, 'ym', '杨幂', '演员')
    ]
    starInfo.insertAll(data_set)
def loadStarImage():
    starImage = StarImage()
    data_set = [
        (None, 'fbb', 'fbb1', 'img1', None),
        (None, 'ym', 'ym1', 'img1', None),
        (None, 'lc_1', 'lc1', 'img2', None)
    ]

    starImage.insertAll(data_set)

def loadVideoInfo():
    videoInfo = VideoInfo()
    data_set = [
        (None, '变形金刚', '2000', '动作/惊险', 'fbb#ym', '范冰冰#杨幂','http://www.baidu.com'),
        (None, '变形金刚1', '2002', '动作/冒险', 'fbb#lc1', '范冰冰#李晨','http://www.sina.com'),
        (None, '变形金刚2', '2006', '动作/爱情', 'ym#ls', '杨幂#李晟','http://www.baidu.com')
    ]
    videoInfo.insertAll(data_set)

if __name__=="__main__":
    loadStarInfo()
    loadStarImage()
    loadVideoInfo()
    starImage = StarImage()
    res = starImage.getAllFeatId()
    print res
