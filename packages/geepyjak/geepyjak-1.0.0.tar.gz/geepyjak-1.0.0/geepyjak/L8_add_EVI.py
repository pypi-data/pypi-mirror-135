import ee

def L8_add_EVI (image):
    B2 = image.select('B2')
    B4 = image.select('B4')
    B5 = image.select('B5')
    B6 = image.select('B6')

    evi = 2.5* ((B5-B4)/(B5 + (6*B4)) - (7.5*B2) - 1)
    return  image.addBands(evi.rename('evi'))