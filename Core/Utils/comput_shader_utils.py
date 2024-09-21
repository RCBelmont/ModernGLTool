"""
FILE_NAME: comput_shader_utils.py
AUTHOR: RCB
CREATED: 2024/4/28-16:54
DESC: 
"""
import moderngl as mgl
from pathlib import Path


def create_compute_shader(context: mgl.Context, shader_file: str):
    '''
    创建一个计算着色器对象
    :param context:
    :param shader_file:
    :return:
    '''
    shader_path = Path(shader_file)
    if shader_path.exists() and shader_path.is_file():
        _shader_file = open(shader_path)
        code = _shader_file.read()
        _shader_file.close()
        cs_obj = context.compute_shader(code)

        return cs_obj
    else:
        raise Exception('Shader 不存在或路径错误：' + str(shader_path))


def create_compute_shader_width_code(context: mgl.Context, code: str):
    '''
    创建一个计算着色器对象
    :param context:
    :param shader_file:
    :return:
    '''
    cs_obj = context.compute_shader(code)
    return cs_obj


def bind_texture_to_shader(shader: mgl.ComputeShader, texture: mgl.Texture, location: int):
    '''
    将纹理绑定到着色器
    :param shader:
    :param texture:
    :param location:
    :return:
    '''
    texture.use(location)
    return shader