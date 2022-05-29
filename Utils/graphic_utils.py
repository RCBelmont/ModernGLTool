import os
os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '1'
from pathlib import Path
import moderngl as mgl
from Utils.Image_lib import *
import matplotlib.image as mi
from PIL import features

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


def create_texture(context: mgl.Context, img_path: str):
    img = read_img('D:\\PC\\Pictures\\Test.jpg')
    save_img("D:\\PC\\Pictures\\OO.exr", img)
    
    



##  return context.texture(img.shape[:2], img.shape[2], img.tobytes(), dtype='f1')
