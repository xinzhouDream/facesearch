from images import images
import web
import os, sys, time
import database
import json
from PIL import Image
import random
from images import images
import match

from im_feat import extract_hsv36
from knn_search import search

dbfile = 'images.db'

from constant import ROOT_PATH
rootpath = ROOT_PATH

config = json.load(open('config.json'))
collection = config['collection']
feature = config['feature']
max_hits = config['max_hits']
image_dir = '/data/wwwroot/default/VisualSearch/toydata/ImageData'

urls = (
    '/', 'index',
    '/search', 'ImageSearch',
    '/upload', 'Upload',
    '/generated','GetGenerated',
    '/images/(.*)', 'images',
    '/feedback', 'Feedback'
)
       
render = web.template.render('templates/')

class index:
    
    def GET(self):
        i = web.input(url=None,local=None)
        resp = {'load':{}, 'content':[]}
        if not i.url and not i.local:
            resp['status'] = 0
        if i.local:
            resp['status'] = 3
            if i.local == '-1':
                _id = database.getNewId(dbfile)
                _id = 1
            else:
                _id = int(i.local)
            resp['load']['url'] = 'local'
            resp['load']['id'] = _id

            local_image_path = "%s/%d.jpg" % (image_dir, _id)
            #resize_image_path = "%s/%d_resize.jpg" % (image_dir, _id)
            print 'from local:',local_image_path
            info_list = match.getSuggestion(local_image_path)
            resp['info_list']=info_list
            #print resp['info_list']
            try:
                im = Image.open(local_image_path)
                okay=True
            except:
                okay=False
            if okay:
                database.update(dbfile, {'id':_id, 'score':0, 'sent':'', 'feat':''})
 
                s_time = time.time()
                query_vec = extract_hsv36(local_image_path)
                feat_time = time.time() - s_time

                feat_file = os.path.join(rootpath, collection, 'FeatureData', feature, 'id.feature.txt')

                s_time = time.time()
                imlist = search(query_vec, feat_file, topk=max_hits)
                knn_time = time.time() - s_time

                resp['feat_time'] = '%.0f' % (feat_time *1000)
                resp['knn_time'] = '%.0f' % (knn_time * 1000)
                resp['status'] = 2

        
        if 0 == resp['status']:
            selected = random.sample(web.imset, max_hits) if len(web.imset)>max_hits else web.imset
            resp['content'] = [{'id':x, 'score':0} for x in selected] 
            
        if 2 == resp['status']:
            resp['content'] = [{'id':_id, 'score':_score} for (_id,_score) in imlist] 
	print resp
        return render.index(resp)



class Upload:

    def POST(self):
        print 'post in upload'
        i = web.input(file={})
        local_flag=False
        try:
            upload_file = i.file#upload_file
            filename = upload_file.filename
            if filename != '':
                local_flag=True
        except: 
            local_flag=False

        if local_flag:
            #_id = database.insert(dbfile, {'ip':'local_image', 'url':'local'})
            _id = 1
            local_image_path = "%s/%d.jpg" % (image_dir, _id)

            #print local_image_path
            fout = open(local_image_path,'wb')
            fout.write(upload_file.file.read())
            fout.close() 
            raise web.seeother('/?local=%d' % _id)
 
        else:
            raise web.seeother('/?url=%s' % i.url)

class GetGenerated:

    def POST(self):
        raise web.seeother('/?local=-1')


class Feedback:
    def POST(self):
        i = web.input()
        user_rank=0
        user_caption=''
        if i.optionsRadios:
            user_rank = int(i.optionsRadios) 
        if i.user_caption:
            user_caption = i.user_caption
        print i.imageid,user_rank,user_caption
        imageid = int(i.imageid)
        database.add_feedback(dbfile, {'id':imageid, 'user_rank':user_rank, 'user_caption':user_caption})
                
        raise web.seeother('/')


class ImageSearch:
    def POST(self):
        i = web.input()
        print i
        if i.url:
            raise web.seeother('/?url=%s' % i.url)
        elif 'local_file' in i:
            print 'local_file'
            local_file = i.local_file
            filename = local_file.filename
            _id = database.insert(dbfile, {'ip':'local_image', 'url':'local'})
            local_image_path = "%s/%d.jpg" % (image_dir, _id)

            #print local_image_path
            if 'upload_file' in i:
                fout = open(local_image_path,'wb')
                fout.write(i.local_file.file.read())
                fout.close()
            print 'raise web.seeother'
            raise web.seeother('/?local=%d' % _id)


if __name__ == "__main__":
    app = web.application(urls, globals())
    Extracted_image=os.path.join(rootpath,collection,'FeatureData',feature,'id.feature.txt')
    imset=[]
    for line in open(Extracted_image).readlines():
        elem = line.strip().split(' ')
        imset.append(elem[0])
    
    web.imset = imset
    app.run()
    
