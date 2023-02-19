import cv2 as cv
import numpy as np
from pyzbar.pyzbar import decode


def translate_qr_code(image_stream):
    try:
        file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
        img = cv.imdecode(file_bytes, cv.IMREAD_COLOR)
        decoded_data = decode(img)
        # parse the decoded zbar data
        url = decoded_data[0].data.decode()
        return url
    except ImportError:
        return None
