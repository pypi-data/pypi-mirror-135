import ee

def maskL8(image):
    qa = image.select('BQA')
    mask = qa.bitwiseAnd(1 << 4).eq(0)
    return image.updateMask(mask)
