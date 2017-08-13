import urllib
import time
import os
import sys
import skimage.io
import numpy as np
import shutil
from PIL import Image


class WebUtil:


    @staticmethod
    def download_image(url, resfile):
        try:
            image_on_web = urllib.urlopen(url)
            tempfile = '%s.%d.temp' % (resfile, time.time())
            urllib.urlretrieve(url, tempfile)
        except:
            print sys.exc_info()[0]
            return 0
        try:   
            im = Image.open(tempfile)
            im.save(tempfile, 'JPEG')
            #img = skimage.img_as_float(skimage.io.imread(tempfile)).astype(np.float32)
            shutil.move(tempfile, resfile)
            return 1
        except:
            print sys.exc_info()[0]
            return 0

if __name__ == '__main__':
    #url = 'http://tpu.eku.cc/swsj/dt/g2_107.jpg'
    #url = 'http://img1.imgtn.bdimg.com/it/u=2055999166,1091979507&fm=15&gp=0.jpg'
    url='http://tp2.sinaimg.cn/1687445117/180/5753326109/0'
    WebUtil.download_image(url, 'img1.jpg')
    
        
