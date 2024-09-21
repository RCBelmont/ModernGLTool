"""
FILE_NAME: graphic_utils.py
AUTHOR: RCB
CREATED: 2024-04-28-16:04
DESC:
"""

import os
import sys

import numpy
from pathlib import Path
import moderngl as mgl
import Core.Utils.image_utils as iu
import Core.Utils.format_define as fd


# region FormatConvert
def numpy_type_to_mdgl(dtype: str) -> str:
    if dtype == "float32":
        return "f4"
    if dtype == "uint8":
        return "f1"


def mdgl_type_to_numpy(dtype: str) -> str:
    if dtype == "f4":
        return "float32"
    if dtype == "f1":
        return "uint8"


def format_to_numpy(my_format: int) -> tuple:
    if my_format == fd.R8:
        return 'uint8', 1
    if my_format == fd.RG8:
        return 'uint8', 2
    if my_format == fd.RGB8:
        return 'uint8', 3
    if my_format == fd.RGBA8:
        return 'uint8', 4
    if my_format == fd.R32:
        return 'float32', 1
    if my_format == fd.RG32:
        return 'float32', 2
    if my_format == fd.RGB32:
        return 'float32', 3
    if my_format == fd.RGBA32:
        return 'float32', 4


def format_to_mdgl(my_format: int) -> tuple:
    if my_format == fd.R8:
        return 'f1', 1
    if my_format == fd.RG8:
        return 'f1', 2
    if my_format == fd.RGB8:
        return 'f1', 3
    if my_format == fd.RGBA8:
        return 'f1', 4
    if my_format == fd.R32:
        return 'f4', 1
    if my_format == fd.RG32:
        return 'f4', 2
    if my_format == fd.RGB32:
        return 'f4', 3
    if my_format == fd.RGBA32:
        return 'f4', 4


def get_img_format(img: numpy.array):
    _, _, cn = img.shape
    dt = img.dtype
    if dt == "float32":
        if cn == 1:
            return fd.R32
        if cn == 2:
            return fd.RG32
        if cn == 3:
            return fd.RGB32
        if cn == 4:
            return fd.RGBA32
    if dt == "uint8":
        if cn == 1:
            return fd.R8
        if cn == 2:
            return fd.RG8
        if cn == 3:
            return fd.RGB8
        if cn == 4:
            return fd.RGBA8
    return fd.Unknown


def get_tex_format(tex: mgl.Texture):
    cn = tex.components
    dt = tex.dtype
    if dt == "f4":
        if cn == 1:
            return fd.R32
        if cn == 2:
            return fd.RG32
        if cn == 3:
            return fd.RGB32
        if cn == 4:
            return fd.RGBA32
    if dt == "f1":
        if cn == 1:
            return fd.R8
        if cn == 2:
            return fd.RG8
        if cn == 3:
            return fd.RGB8
        if cn == 4:
            return fd.RGBA8
    return fd.Unknown


# endregion

def any_to_rgba32(img: numpy.ndarray) -> numpy.ndarray:
    size_x, size_y, cn = img.shape
    r_img = img.copy()
    if r_img.dtype != 'float32':
        r_img = iu.to_float32(r_img)
    if cn == 3:
        r_img = numpy.insert(r_img, 3, 1, axis=2)
    elif cn == 2:
        r_img = numpy.insert(r_img, 2, 0, axis=2)
        r_img = numpy.insert(r_img, 3, 1, axis=2)
    elif cn == 1:
        r_img = numpy.insert(r_img, 1, 0, axis=2)
        r_img = numpy.insert(r_img, 2, 0, axis=2)
        r_img = numpy.insert(r_img, 3, 1, axis=2)
    return r_img


# region Texture <-> Image
def texture_to_img(tex: mgl.Texture):
    '''
    2D纹理对象转图片对象
    :param tex:
    :return:
    '''
    data_array = numpy.frombuffer(tex.read(), dtype=mdgl_type_to_numpy(tex.dtype))
    data_array = data_array.copy()
    return data_array.reshape((tex.size[1], tex.size[0], tex.components))


def texture_cube_to_img(tex: mgl.TextureCube, face: int):
    '''
    立方体纹理对象转图片对象
    :param tex:
    :param face:
    :return:
    '''
    data_array = numpy.frombuffer(tex.read(face), dtype=mdgl_type_to_numpy(tex.dtype))
    data_array = data_array.copy()
    return data_array.reshape((tex.size[1], tex.size[0], tex.components))


def img_to_texture(context: mgl.Context, img: numpy.ndarray, RGBA32f=True):
    '''
    图片对象转2D纹理对象
    :param context:
    :param img:
    :param t_format:
    :return:
    '''
    size_x, size_y, cn = img.shape
    if RGBA32f:
        img = any_to_rgba32(img)
    i_format = get_img_format(img)
    assert (i_format != fd.Unknown)
    tex = create_texture_base(context, (size_y, size_x), i_format, img.tobytes())
    return tex


# endregion Texture <-> Image

def create_texture_base(context: mgl.Context, size, t_format=fd.RGBA32, data=None):
    '''
    创建一个Texture对象
    :param context:
    :param size:
    :param t_format:
    :param data:
    :return:
    '''
    dtype, cn = format_to_mdgl(t_format)
    return context.texture(size, cn, dtype=dtype, data=data)


def create_texture_with_img(context: mgl.Context, img_path: str, RGBA32f=True) -> mgl.Texture:
    '''
    根据图片文件生成一个Texture对象
    :param context:
    :param img_path:
    :return:
    '''
    img = iu.read_img(img_path)
    size_x, size_y, cn = img.shape
    if RGBA32f:
        img = any_to_rgba32(img)
    i_format = get_img_format(img)
    assert (i_format != fd.Unknown)
    tex = create_texture_base(context, (size_y, size_x), i_format, img.tobytes())
    return tex


def create_texture_with_color(context: mgl.Context, width: int, height: int,
                              color: tuple = (0, 0, 0, 1)) -> mgl.Texture:
    '''
    生成一个固定颜色的Texture对象，强制RGBA32
    :param context:
    :param width:
    :param height:
    :param init_color:
    :return:
    '''
    a = numpy.zeros((width, height, 4), dtype="float32")
    ic_len = len(color)
    if ic_len > 0:
        a[:, :, 0] = color[0]

    if ic_len > 1:
        a[:, :, 1] = color[1]

    if ic_len > 2:
        a[:, :, 2] = color[2]

    if ic_len > 3:
        a[:, :, 3] = color[3]

    return create_texture_base(context, (width, height), fd.RGBA32, a.tobytes())


# region TextureCube
# 0: Positive X
# 1: Negative X
# 2: Positive Y
# 3: Negative Y
# 4: Positive Z
# 5: Negative Z
def create_texture_cube_with_color(context: mgl.Context, size=64, color=(0, 0, 0, 1)):
    '''
    生成一个固定颜色的TextureCube对象
    :param context:
    :return:
    '''

    tex = context.texture_cube((size, size), 4, dtype='f4')
    color_array = numpy.zeros((size, size, 4), dtype='float32')
    ic_len = len(color)
    if ic_len > 0:
        color_array[:, :, 0] = color[0]

    if ic_len > 1:
        color_array[:, :, 1] = color[1]

    if ic_len > 2:
        color_array[:, :, 2] = color[2]

    if ic_len > 3:
        color_array[:, :, 3] = color[3]
    bytes_data = color_array.tobytes()
    for i in range(0, 6):
        tex.write(i, data=bytes_data)
    return tex


def create_texture_cube_with_img(context: mgl.Context, files: list):
    '''
    根据图片文件生成一个TextureCube对象
    :param context:
    :param files:
    :return:
    '''
    f_len = len(files)
    if f_len <= 0:
        raise Exception("Need Unless 1 Image File")
    first_img = iu.read_img(files[0])
    h, w, cn = first_img.shape
    if h != w:
        raise Exception("Source Image Must Be Square w = h")
    size = h
    image_bytes_list = []
    first_img = any_to_rgba32(first_img)
    image_bytes_list.append(first_img.tobytes())
    for i in range(1, f_len):
        img = iu.read_img(files[i])
        h, w, cn = img.shape
        if h != w:
            raise Exception("Source Image Must Be Square w = h")
        if h != size:
            raise Exception("Each Image Must Have Same Size")

        byte_data = any_to_rgba32(img).tobytes()
        image_bytes_list.append(byte_data)

    tex_cube = context.texture_cube((size, size), 4, dtype='f4')

    for i in range(0, 6):
        idx = i
        if idx > f_len - 1:
            idx = f_len - 1
        tex_cube.write(i, image_bytes_list[i])
    return tex_cube
# endregion
