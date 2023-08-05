import ee
import geemap

# NDVI function

def L8_add_NDVI (image):
    ndvi = image.normalizedDifference(['B5', 'B4'])
    return  image.addBands(ndvi.rename('ndvi'))

def S2_add_NDVI (image):
    ndvi = image.normalizedDifference(['B8', 'B4'])
    return  image.addBands(ndvi.rename('ndvi'))

# NDWI function

def L8_add_NDWI(image):
    ndwi = image.normalizedDifference(['B3', 'B5'])
    return image.addBands(ndwi.rename("ndwi"))

def S2_add_NDWI(image):
    ndwi = image.normalizedDifference(['B3', 'B8'])
    return image.addBands(ndwi.rename("ndwi"))

# EVI function

def L8_add_EVI (image):
    B2 = image.select('B2')
    B4 = image.select('B4')
    B5 = image.select('B5')
    B6 = image.select('B6')

    evi = 2.5* ((B5-B4)/(B5 + (6*B4)) - (7.5*B2) - 1)
    return  image.addBands(evi.rename('evi'))

def S2_add_EVI (image):
    B2 = image.select('B2')
    B4 = image.select('B4')
    B5 = image.select('B5')
    B6 = image.select('B6')

    evi = 2.5* ((B5-B4)/(B5 + (6*B4)) - (7.5*B2) - 1)
    return  image.addBands(evi.rename('evi'))

# Cloud Mask Function

def maskL8(image):
    qa = image.select('BQA')
    mask = qa.bitwiseAnd(1 << 4).eq(0)
    return image.updateMask(mask)

def maskS2clouds(image):
    cloudBitMask = ee.Number(2).pow(10).int()
    cirrusBitMask = ee.Number(2).pow(11).int()
    qa = image.select('QA60')
    # Both flags should be set to zero, indicating clear conditions.
    mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(
        qa.bitwiseAnd(cirrusBitMask).eq(0))
    return image.updateMask(mask)

#Pansharpening of Landsat-8

def panSharpenL8(image):
    rgb = image.select('B4', 'B3', 'B2')
    pan = image.select('B8')
    # Convert to HSV, swap in the pan band, and convert back to RGB.
    huesat = rgb.rgbToHsv().select('hue', 'saturation')
    upres = ee.Image.cat(huesat, pan).hsvToRgb()
    return image.addBands(upres)


