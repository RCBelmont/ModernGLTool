import os

import numpy as np

os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '1'
import numpy
import matplotlib.image as mping
import cv2
import Utils.format_define as fd




def read_img(file_path: str) -> numpy.array:
    print("OpenImageAt: " + file_path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        if file_path.endswith('.hdr') or file_path.endswith('.exr'):
            img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
            _, _, cn = img.shape
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
            return img
        else:
            img = mping.imread(file_path)
            return img

    else:
        raise Exception("图片文件路径错误" + file_path)


def save_img(file_path: str, img: numpy.array):
    if file_path.endswith('.hdr'):
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        cv2.imwrite(file_path, img)
    elif file_path.endswith('.exr'):
        img = to_float32(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA)
        cv2.imwrite(file_path, img)
    else:
        img = to_uint8(img)
        mping.imsave(file_path, img)


def to_float32(data):
    dt = data.dtype
    if dt == 'float32':
        return data
    if dt == 'uint8':
        data = numpy.asarray(data, 'float32')
        data /= 255.0
        return data
    raise Exception("to_float32 cannot handle type" + str(dt))


def to_uint8(data):
    dt = data.dtype
    if dt == 'uint8':
        return data
    if dt == 'float32':
        data *= 255.0
        data = data.clip(min=0, max=255)
        data = numpy.asarray(data, 'uint8')
        return data
    raise Exception("to_uint8 cannot handle type" + str(dt))
