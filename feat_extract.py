import os, sys

from im_feat import extract_hsv36
from constant import ROOT_PATH


def feat_extract(collection, feat = 'hsv36', rootpath=ROOT_PATH):
    imsetfile = os.path.join(rootpath, collection,'id.imagepath.txt')
    outpath = os.path.join(rootpath,collection,'FeatureData',feat,'id.feature.txt')

    if not os.path.exists(os.path.split(outpath)[0]):
       os.makedirs(os.path.split(outpath)[0])

    print ('writing %s to %s' % (feat, outpath))
    fw = open(outpath,'w')
 
    for line in open(imsetfile):
        _id, _filename = line.strip().split()
        vec = extract_hsv36(_filename)
        fw.write('%s %s\n' % (_id, ' '.join(map(str, vec))))
  
    fw.close()



if __name__ == '__main__':
    rootpath = ROOT_PATH

    collection= sys.argv[1] 
    feat = sys.argv[2] # hsv36

    feat_extract(collection, feat)

