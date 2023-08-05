import ee

def S2_add_NDWI(image):
    ndwi = image.normalizedDifference(['B3', 'B8'])
    return image.addBands(ndwi.rename("ndwi"))
