import os
import numpy

os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '1'
from pathlib import Path
import moderngl as mgl
from Utils.Image_lib import *
import Utils.format_define as fd


# region FormatUtil
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


def create_contex_standalone():
    return mgl.create_context(require=430, standalone=True)


def create_compute_shader(context: mgl.Context, shader_file: str):
    shader_path = Path(shader_file)
    if shader_path.exists() and shader_path.is_file():
        _shader_file = open(shader_path)
        code = _shader_file.read()
        _shader_file.close()
        return context.compute_shader(code)
    else:
        raise Exception('Shader 不存在或路径错误：' + str(shader_path))


def create_texture_base(context: mgl.Context, size, t_format=fd.RGBA32, data=None):
    dtype, cn = format_to_mdgl(t_format)
    return context.texture(size, cn, dtype=dtype, data=data)


def create_texture_with_img(context: mgl.Context, img_path: str) -> mgl.Texture:
    img = read_img(img_path)
    size_x, size_y, cn = img.shape
    img = to_float32(img)
    if cn == 3:
        img = numpy.insert(img, 3, 1, axis=2)
    ##TODO:DELETE
    print(img)
    
    i_format = get_img_format(img)
    assert (i_format != fd.Unknown)
    tex = create_texture_base(context, (size_y, size_x), i_format, img.tobytes())
    return tex


def create_texture_with_color(context: mgl.Context, width: int, height: int,
                              init_color: tuple = (0, 0, 0, 1)) -> mgl.Texture:
    a = numpy.zeros((width, height, 4), dtype="float32")
    ic_len = len(init_color)
    if ic_len > 0:
        a[:, :, 0] = init_color[0]

    if ic_len > 1:
        a[:, :, 1] = init_color[1]

    if ic_len > 2:
        a[:, :, 2] = init_color[2]

    if ic_len > 3:
        a[:, :, 3] = init_color[3]

    return create_texture_base(context, (width, height), fd.RGBA32, a.tobytes())


def texture_to_img(tex: mgl.Texture):
    data_array = numpy.frombuffer(tex.read(), dtype=mdgl_type_to_numpy(tex.dtype))
    data_array = data_array.copy()
    return data_array.reshape((tex.size[1], tex.size[0], tex.components))
