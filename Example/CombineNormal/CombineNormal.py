"""
FILE_NAME: CombineNormal.py
AUTHOR: RCB
CREATED: 2024/6/25-11:30
DESC: 
"""
"""
FILE_NAME: SpecGlossToMetallic.py
AUTHOR: RCB
CREATED: 2024/5/27-14:08
DESC: 
"""
import os
import Core as core
import Core.Utils.comput_shader_utils as csu
import Core.Utils.image_utils as iu
import Core.Utils.texture_utils as tu

if __name__ == '__main__':
    normal1 = r"D:\User\Documents\我的POPO\TEX\T_Makeup_Hero_F_Decalup_D16_N.tga"
    normal2 = r"D:\User\Downloads\T_Makeup_Hero_F_Glitter_02.TGA"
    UV_shuffix = ""
    ##UV_shuffix = "_UV2"

    context = core.create_contex_standalone()
    cs = csu.create_compute_shader(context, os.path.dirname(__file__) + '\\CombineNormal.glsl')
    out_texture = tu.create_texture_with_color(context, width=256, height=256)
    normal_tex1 = tu.create_texture_with_img(context, normal1)
    normal_tex2 = tu.create_texture_with_img(context, normal2)

    cs['normal1'] = 0
    cs['normal2'] = 1
    normal_tex1.use(location=0)
    normal_tex2.use(location=1)

    out_texture.bind_to_image(2, read=True, write=True)
    cs.run(int(out_texture.width / 16), int(out_texture.height / 16), 1)
    save_dir = os.path.join(os.path.dirname(normal1), "MixNormal")
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"Mix_Normal{UV_shuffix}.tga")
    img = tu.texture_to_img(out_texture)
    iu.save_img(save_path, img)



