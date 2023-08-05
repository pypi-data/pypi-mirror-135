import ee

def panSharpenL8(image):
    rgb = image.select('B4', 'B3', 'B2')
    pan = image.select('B8')
    # Convert to HSV, swap in the pan band, and convert back to RGB.
    huesat = rgb.rgbToHsv().select('hue', 'saturation')
    upres = ee.Image.cat(huesat, pan).hsvToRgb()
    return image.addBands(upres)