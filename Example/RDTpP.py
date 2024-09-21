"""
FILE_NAME: NSHPramTo117Param.py
AUTHOR: RCB
CREATED: 2024/4/30-12:00
DESC:
"""
import os

import numpy
import numpy as np

import Core as core
import Core.Utils.comput_shader_utils as csu
import Core.Utils.image_utils as iu
import Core.Utils.texture_utils as tu


def renderdoc_grid_to_texture_cube(context, file: str):
    grid_img = iu.read_img(file)

    row, column, _ = grid_img.shape
    if row / column != 6:
        raise Exception('Image Size Error')
    data_list = numpy.split(grid_img, row / column)
    tex_cube = context.texture_cube(size=(column, column), components=4, dtype='f4')
    for i in range(0, len(data_list)):
        data = data_list[i]
        data = np.flipud(data)
        ##data = np.fliplr(data)
        data = tu.any_to_rgba32(data)
        tex_cube.write(i, data.tobytes())
    return tex_cube

if __name__ == '__main__':
    src_path = r"D:\User\Downloads\Weapon\Env.tga"
    dst_path = r"D:\User\Downloads\Weapon\Env_2.hdr"

    context = core.create_contex_standalone()
    cs = csu.create_compute_shader(context, os.path.dirname(__file__) + '\\RDTpP.glsl')
    src_texture = renderdoc_grid_to_texture_cube(context, src_path)
    dst_texture = tu.create_texture_with_color(context, width=128, height=64)
    src_texture.use(0)
    dst_texture.bind_to_image(1, read=True, write=True)
    cs.run(int(dst_texture.width / 16), int(dst_texture.height / 16), 1)
    save_img = tu.texture_to_img(dst_texture)
    ##TODO:DELETE
    print(dst_path)
    
    iu.save_img(dst_path, save_img)
