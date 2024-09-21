"""
FILE_NAME: TextureMerger.py
AUTHOR: RCB
CREATED: 2024/9/19-15:23
DESC: 
"""
import os

import Core as core
import Core.Utils.comput_shader_utils as csu
import Core.Utils.image_utils as iu
import Core.Utils.texture_utils as tu

import moderngl as mgl
if __name__ == '__main__':
    context = core.create_contex_standalone()
    com_shader = csu.create_compute_shader(context, os.path.dirname(__file__) + '\\TextureMerger.glsl')



    t0 = tu.create_texture_with_img(context, r"D:\User\Downloads\T_ClothMud_D.TGA")
    t1 = tu.create_texture_with_img(context, r"D:\User\Downloads\T_Puddle_01_N.TGA")
    t2 = tu.create_texture_with_img(context, r"D:\User\Downloads\T_ClothMud_Noise.TGA")

    s1 = context.sampler(texture=t0)
    s2 = context.sampler(texture=t1)
    s3 = context.sampler(texture=t2)
    dst = tu.create_texture_with_color(context, 256, 256, (0, 0, 0, 1))


    s1.use(0)
    s2.use(1)
    s3.use(2)
    dst.bind_to_image(3, read=True, write=True)





    com_shader.run(int(dst.width / 16), int(dst.height / 16), 1)
    save_img = tu.texture_to_img(dst)
    iu.show_img([save_img])
    ##iu.save_img(r"D:\User\Downloads\T_ClothMud_Tex.tga", save_img)
