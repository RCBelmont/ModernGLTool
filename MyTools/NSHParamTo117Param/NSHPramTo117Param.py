"""
FILE_NAME: NSHPramTo117Param.py
AUTHOR: RCB
CREATED: 2024/4/30-12:00
DESC: 
"""
import os
import Core as core
import Core.Utils.comput_shader_utils as csu
import Core.Utils.image_utils as iu
import Core.Utils.texture_utils as tu


if __name__ == '__main__':
    src_path = r"D:\User\Downloads\T_Makeup_Hero_F_Iris_2.TGA"
    dst_path = r"D:\User\Downloads\T_Makeup_Hero_F_Iris_2_Test1.TGA"

    context = core.create_contex_standalone()
    cs = csu.create_compute_shader(context, os.path.dirname(__file__) + '\\temp.glsl')
    src_texture = tu.create_texture_with_img(context, src_path)
    dst_texture = tu.create_texture_with_color(context, width=src_texture.width, height=src_texture.height)
    src_texture.use(0)
    dst_texture.bind_to_image(1, read=True, write=True)
    cs.run(int(dst_texture.width / 16), int(dst_texture.height / 16), 1)
    save_img = tu.texture_to_img(dst_texture)
    iu.save_img(dst_path, save_img)
    ##iu.show_img([save_img])
