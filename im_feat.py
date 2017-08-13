#for an image, return feature vector

def extract_hsv36(imgfilename):
    
    #to-do: here implement your feature
    vec = [0] * 36

    return vec 


if __name__  == '__main__':
    imgfilename = 'test.jpg'
    vec = extract_hsv36(imgfilename)
    print vec

