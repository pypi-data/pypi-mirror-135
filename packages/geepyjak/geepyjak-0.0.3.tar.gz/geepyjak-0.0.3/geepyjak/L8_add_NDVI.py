import ee

def L8_add_NDVI (image):
    ndvi = image.normalizedDifference(['B5', 'B4'])
    return  image.addBands(ndvi.rename('ndvi'))