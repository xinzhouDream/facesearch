import sys
from database import StarInfo
from database import StarImage
from database import VideoInfo
from PIL import Image

def getMostSimId(imageFile):
    starImage = StarImage()

    # 获取所有图片的face_id集合
    featIds = starImage.getAllFeatId()
    #读取上传图片
    img = Image.open(imageFile)

    #TODO: get face id

    # 返回最相似的face_id
    return featIds[0]

def getSuggestion(imageFile):
    starInfo = StarInfo()
    starImage = StarImage()
    videoInfo = VideoInfo()
    info_list = {}
    most_sim_id = getMostSimId(imageFile)

    image_info = starImage.getRowByFeatId(most_sim_id)
    star_id = image_info[0]

    star_res = starInfo.getStarInfoById(star_id)
    video_res = videoInfo.getVideoInfoByStarId(star_id)

    sim_imge_id = image_info[1]

    print 'star_res:',star_res
    info_list['star_info']={'name': star_res[0][0],'description':star_res[0][1]}
    info_list['sim_id']=sim_imge_id
    info_list['video_info'] = []

    for video in video_res:
        info_list['video_info'].append(video)

    return info_list
