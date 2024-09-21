"""
FILE_NAME: LinearSRGBConvert.py
AUTHOR: RCB
CREATED: 2024/4/30-11:00
DESC: 
"""
import os.path

import Core as core
import Core.Utils.comput_shader_utils as csu
import Core.Utils.image_utils as iu
import Core.Utils.texture_utils as tu


def SRGBToLinear(src_path, dst_path) -> float:
    context = core.create_contex_standalone()
    cs = csu.create_compute_shader(context, os.path.dirname(__file__) + '\\LinearSRGBConvert.glsl')
    src_texture = tu.create_texture_with_img(context, src_path)
    dst_texture = tu.create_texture_with_color(context, width=src_texture.width, height=src_texture.height)
    src_texture.bind_to_image(0, read=True, write=False)
    dst_texture.bind_to_image(1, read=True, write=True)
    cs["LinToSRGB"] = False
    cs.run(int(dst_texture.width/16), int(dst_texture.height/16), 1)
    save_img = tu.texture_to_img(dst_texture)
    iu.save_img(dst_path, save_img)

    pass


def LinearToSRGB(linear: float) -> float:
    pass


if __name__ == '__main__':
    SRGBToLinear(r"D:\User\Downloads\T_ColorGrid.TGA",
                 r"D:\User\Downloads\T_ColorGrid_line.TGA")
    pass