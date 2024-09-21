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
    MainTex = r"D:\User\Documents\我的POPO\交接文件-程畅\服装\新建文件夹 (2)\T_M_23_Suit03_2UV02_D02.TGA"
    SpecGloss = r"D:\User\Documents\我的POPO\交接文件-程畅\服装\新建文件夹 (2)\T_M_23_Suit03_2UV02_S02.TGA"
    UV_shuffix = ""
    ##UV_shuffix = "_UV2"

    context = core.create_contex_standalone()
    cs = csu.create_compute_shader(context, os.path.dirname(__file__) + '\\SpecGlossToMetallic.glsl')
    main_texture = tu.create_texture_with_img(context, MainTex)
    spec_texture = tu.create_texture_with_img(context, SpecGloss)
    new_main_texture = tu.create_texture_with_color(context, width=spec_texture.width, height=spec_texture.height)
    mix_texture = tu.create_texture_with_color(context, width=spec_texture.width, height=spec_texture.height)

    cs['mainTex'] = 0
    cs['specTex'] = 1
    main_texture.use(location=0)
    spec_texture.use(location=1)

    new_main_texture.bind_to_image(2, read=True, write=True)
    mix_texture.bind_to_image(3, read=True, write=True)
    cs.run(int(mix_texture.width / 16), int(mix_texture.height / 16), 1)
    save_dir = os.path.join(os.path.dirname(MainTex), "MetallicConvert")
    os.makedirs(save_dir, exist_ok=True)
    if MainTex.__contains__("_2UV"):
        UV_shuffix = "_2UV"
    save_path1 = os.path.join(save_dir, f"New_MainTex{UV_shuffix}.tga")
    save_path2 = os.path.join(save_dir, f"Mix_Tex{UV_shuffix}.tga")
    save_img1 = tu.texture_to_img(new_main_texture)
    save_img2 = tu.texture_to_img(mix_texture)
    iu.save_img(save_path1, save_img1)
    iu.save_img(save_path2, save_img2)
