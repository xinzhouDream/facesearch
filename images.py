import web
import os
import json

from constant import ROOT_PATH

config = json.load(open('config.json'))
collection = config['collection']

rootpath = ROOT_PATH
imagedata_dir = os.path.join(rootpath,collection,'ImageData')

class images:
    def GET(self,name):
        ext = name.split(".")[-1] # Gather extension
        imageid = name.split(".")[0]

        cType = {
            "png":"images/png",
            "jpg":"images/jpeg",
            "gif":"images/gif",
            "ico":"images/x-icon"            }

        imfile = os.path.join(imagedata_dir, '%s.jpg' % imageid)
        if not os.path.exists(imfile):
            imfile = os.path.join('Imagedata', '%s.jpg' % imageid)
        try:
            web.header("Content-Type", cType[ext]) # Set the Header
            #print imfile
            return open(imfile,"rb").read() # Notice 'rb' for reading images
        except:
            raise web.notfound()

if __name__ == '__main__':
    imagedata_dir = os.path.join(rootpath,collection,'ImageData')
    imagedata_dir = 'ImageData'
    im = images()
    im.GET('4.jpg')

