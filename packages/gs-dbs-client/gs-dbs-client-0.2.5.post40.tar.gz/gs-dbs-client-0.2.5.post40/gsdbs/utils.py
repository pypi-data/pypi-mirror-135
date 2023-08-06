import base64

import blosc
import numpy as np


def gsNpCompressBase64WithShape(frame):
    bytes_array = frame.tostring()
    zframe = blosc.compress(bytes_array)
    b64frame = base64.b64encode((zframe))
    return b64frame.decode('utf-8'), frame.shape[0], frame.shape[1], frame.shape[2]


def gsNumpyDecompressBase64(b64frame, w, h, d):
    zframe = base64.b64decode(b64frame.encode('utf-8'))
    frame = np.frombuffer(blosc.decompress(zframe, True), dtype=np.uint8)
    frame.shape = (int(w), int(h), int(d))
    return frame
