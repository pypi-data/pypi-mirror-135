import ee

def L8_add_NDWI(image):
    ndwi = image.normalizedDifference(['B3', 'B5'])
    return image.addBands(ndwi.rename("ndwi"))