

def search(query_vec, feat_file, topk=20):
    feat_dim = len(query_vec)

    reslist = []

    for line in open(feat_file):
        elems = line.strip().split()
        imgid = elems[0]
        del elems[0]
        vec = map(float, elems)
        assert(len(vec) == feat_dim)

        distance = 0
        #to-do: compute visual distanceance between the query vec and the vec in the database
        
        reslist.append((imgid, distance))

    reslist.sort(key=lambda v:(v[1],v[0]))

    return reslist



if __name__ == '__main__':
    import os

    query_vec = [1]*36

    from constant import ROOT_PATH

    collection = 'toydata'
    feature = 'hsv36'

    feat_file = os.path.join(ROOT_PATH, collection, 'FeatureData', feature, 'id.feature.txt')

    reslist = search(query_vec,feat_file)
    print reslist


