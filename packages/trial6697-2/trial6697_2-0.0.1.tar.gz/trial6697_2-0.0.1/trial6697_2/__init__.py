import ee

def L8_add_NDVI (image):
    ndvi = image.normalizedDifference(['B5', 'B4'])
    return  image.addBands(ndvi.rename('ndvi'))

def S2_add_NDVI (image):
    ndvi = image.normalizedDifference(['B8', 'B4'])
    return  image.addBands(ndvi.rename('ndvi'))