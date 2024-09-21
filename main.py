import math
import os
import numpy as np
import pyperclip
from Core.Utils.texture_utils import *
import Core.Function as func
from PIL import Image


def main():
    shader_path = 'Shader/CubeToPanorama.glsl'

    context = create_contex_standalone()
    cs = create_compute_shader(context, shader_path)
    for root, d, f_list in os.walk(r'G:\RND\AI\DataSet\FF_Style_Fix'):
        for f in f_list:
            img_in = create_texture_with_img(context, os.path.join(root, f))
            shader_path = os.getcwd() + "\\Shader\\Test.glsl"
            cs = create_compute_shader(context, shader_path)
            img_in.use(0)
            sampSource = context.sampler()
            sampSource.use(location=0)
            tex_out = create_texture_with_color(context, width=512, height=512)
            tex_out.bind_to_image(1)
            cs.run(math.ceil(tex_out.size[0] / 16), math.ceil(tex_out.size[1] / 16), 1)
            img = texture_to_img(tex_out)
            save_img(r'G:\RND\AI\DataSet\FF_Style_xx\\' + f, img)
            ##TODO:DELETE
            print("save：" + f)
            tex_out.release()
            img_in.release()
    cs.release()
    context.release()

    # cs['texture0'] = 0
    # texSource = create_texture_cube_with_img(context, [
    #     "./TestImage/Cube/PX.exr",
    #     "./TestImage/Cube/NX.exr",
    #     "./TestImage/Cube/PY.exr",
    #     "./TestImage/Cube/NY.exr",
    #     "./TestImage/Cube/PZ.exr",
    #     "./TestImage/Cube/NZ.exr"
    # ])
    #
    # # texSource = create_texture_cube_with_img(context, [
    # #         "./TestImage/Cube/RED.exr",
    # #         "./TestImage/Cube/RED.exr",
    # #         "./TestImage/Cube/GREEN.exr",
    # #         "./TestImage/Cube/GREEN.exr",
    # #         "./TestImage/Cube/BLUE.exr",
    # #         "./TestImage/Cube/BLUE.exr"
    # #     ])
    #
    # ##TODO:DELETE
    # print(texSource.dtype)
    #
    # texSource.use(location=0)
    # # sampSource = context.sampler()
    # # sampSource.use(location=0)
    # texDist = create_texture_with_color(context, width=2048, height=1024)
    # texDist.bind_to_image(1)
    # cs.run(math.ceil(texDist.size[0] / 16), math.ceil(texDist.size[1] / 16), 1)
    # img = texture_to_img(texDist)
    # show_img([img])
    # save_img('./OutPut/TextHDRI.hdr', img)
    # cs.release()
    # texDist.release()
    # texSource.release()
    # func.renderdoc_grid_to_panorama('./TestImage/gg.exr', './OutPut/reflect.hdr')

    # context = create_contex_standalone()
    # shader_path = os.getcwd() + "\\Shader\\Test.glsl"
    # cs = create_compute_shader(context, shader_path)
    # tex_out = create_texture_with_color(context, 1024, 1024)
    # tex_out.bind_to_image(1)
    # cs.run(math.ceil(tex_out.size[0] / 16), math.ceil(tex_out.size[1] / 16), 1)
    # img = texture_to_img(tex_out)
    # show_img([img])
    # save_img("./OutPut/Sphare123.exr", img)
    # cs.release()
    # tex_out.release()
    #
    # context.release()

    ##func.gen_blender_film_data()


# texDist = create_texture_with_color(context, width=512, height=128, init_color=(1, 0, 0, 1))
# texDist.bind_to_image(0, read=True, write=True)
# texDist.filter = mgl.NEAREST, mgl.NEAREST

# cs.run(math.ceil(texDist.size[0] / 1), math.ceil(texDist.size[1] / 1), 1)

##screate_texture(context, img_path)
# f = open("./Shader/Test.glsl")
# shaderCode = f.read()
#
# ctx = mgl.create_context(require=430, standalone=True)
# print(ctx)
# cs = ctx.compute_shader(shaderCode)
# cs['destTex'] = 0
# texDist = ctx.texture((256, 256), 4)
# texDist.filter = mgl.NEAREST, mgl.NEAREST
# texDist.bind_to_image(0, read=False, write=True)
# Image.open("")
# texSource = ctx.texture()
# cs.run(int(256 / 16), int(256 / 16))

def test1():
    context = create_contex_standalone()
    shader_path = r'F:\DevSSD\GitHub\ModernGLTool\Shader\Test2.glsl'
    cs = create_compute_shader(context, shader_path)
    dst = create_texture_with_color(context, 1024, 256)
    # orig = create_texture_with_img(context, r"E:\Proj\ART\ToneLut.exr")
    # orig.use(0)
    dst.bind_to_image(0)
    cs.run(math.ceil(dst.size[0] / 16), math.ceil(dst.size[1] / 16), 1)
    img = texture_to_img(dst)
    show_img([img])
    save_img(r"G:\RND\ColorBoard.exr", img)


def test():
    context = create_contex_standalone()
    p = r'D:\PC\Desktop\class'
    s = r'D:\PC\Desktop\class1'
    os.makedirs(s, exist_ok=True)
    shader_path = r'F:\DevSSD\GitHub\ModernGLTool\Shader\Test.glsl'
    cs = create_compute_shader(context, shader_path)
    for r, d, fl in os.walk(p):
        for f in fl:
            i1 = os.path.join(r, f)
            img1 = create_texture_with_img(context, i1)
            out_tex = create_texture_with_color(context, 768, 1024)
            out_tex.bind_to_image(0)
            img1.bind_to_image(1)
            cs.run(math.ceil(out_tex.size[0] / 16), math.ceil(out_tex.size[1] / 16), 1)
            out_img = texture_to_img(out_tex)
            save_img(os.path.join(s, f), out_img)

    # i2 = r'D:\PC\Desktop\ff\NiagaraBug\LocalSpace-ScaleNegative-TwoSide.jpg'

    # sampSource1 = context.sampler(texture= img1)
    # sampSource1.use(location=0)
    # img2 = create_texture_with_img(context, i2)
    # sampSource2 = context.sampler(texture=img2)
    # sampSource2.use(location=1)
    #

    # cs['texture0'] = 0
    # cs['texture1'] = 1
    # cs['texture2'] = 2
    # show_img([out_img])


def create_panorama():
    # img_path = [r"D:\PC\Desktop\ff\softcookies\origMask2.tga"]
    # save_path = r"D:\PC\Desktop\ff\softcookies\origMask2_param.tga"
    context = create_contex_standalone()
    base_dir = r"D:\PC\Desktop\ff\softcookies"
    img_name = ["origMask1.tga", "origMask2.tga"]
    save_dir = r"D:\PC\Desktop\ff\softcookies\ps"
    save_name = ["origMask1_panorama.tga", "origMask2_panorama.tga"]
    for i, name in enumerate(img_name):
        img_path = os.path.join(base_dir, name)
        save_path = os.path.join(save_dir, save_name[i])
        tex_cube = func.pic_list_to_cube(context, [img_path])
        if tex_cube:
            func.cube_to_panorama(context, tex_cube, save_path)


def create_tone():
    # img_path = [r"D:\PC\Desktop\ff\softcookies\origMask2.tga"]
    # save_path = r"D:\PC\Desktop\ff\softcookies\origMask2_param.tga"
    context = create_contex_standalone()
    base_dir = r"D:\PC\Desktop\ff\softcookies"
    img_name = ["origMask1.tga", "origMask2.tga"]
    save_dir = r"D:\PC\Desktop\ff\softcookies\ps"
    save_name = ["origMask1_panorama.tga", "origMask2_panorama.tga"]
    for i, name in enumerate(img_name):
        img_path = os.path.join(base_dir, name)
        save_path = os.path.join(save_dir, save_name[i])
        tex_cube = func.pic_list_to_cube(context, [img_path])
        if tex_cube:
            func.cube_to_panorama(context, tex_cube, save_path)


def conv_gloss_2_rough(path):
    file_path = path
    file_path1 = r"D:\User\Downloads\SkinTextConvert\T_Thd_F_Head_UT_M_cov.tga"
    dir_name = os.path.dirname(file_path)
    base_name = os.path.basename(file_path)
    file_name = base_name.split('.')[0]
    ext_name = base_name.split('.')[1]
    context = create_contex_standalone()
    shader_path = r'D:\Develop\ModernGLTool\Shader\GlossToRough.glsl'
    cs = create_compute_shader(context, shader_path)
    src_texture = create_texture_with_img(context, file_path)
    src_texture1 = create_texture_with_img(context, file_path1)
    dst_texture = create_texture_with_color(context, width=src_texture.width, height=src_texture.height)
    src_texture.bind_to_image(0)
    dst_texture.bind_to_image(1)
    src_texture1.bind_to_image(2)
    cs.run(int(src_texture.width / 16), int(src_texture.height / 16), 1)
    img = texture_to_img(dst_texture)
    save_path = os.path.join(dir_name, file_name + "_rough.tga")
    save_img(save_path, img)


def create_skin_lut(save_path):
    context = create_contex_standalone()
    dst_texture = create_texture_with_color(context, width=256, height=256)
    dst_texture.bind_to_image(0)
    shader_path = r'D:\Develop\ModernGLTool\Shader\SkinLut.glsl'
    cs = create_compute_shader(context, shader_path)
    cs.run(int(dst_texture.width / 16), int(dst_texture.height / 16), 1)
    img = texture_to_img(dst_texture)
    show_img([img])
    save_img(save_path, img)


def buffer_test(save_path):
    ids = [
        "52C0B839489724CB6BACED8C6AA19A12",
        "1D68A83D4FAACC4CD62F2AA501DEE149",
        "F00F80D24762D6590C4F16A5A1AE5376",
        "E7FA9CD844E5558FFC79B4866FE79D9F",
        "93919C7342C862024919D5ACA299DF6B",
        "87C71B43482FDBD1CBF23DA1CBE4127D",
        "A79DB48D477D04A6756C1DA1A2F6A912",
        "0783486240AD42E163407882D9526E74",
        "DA542B0040D26E646642D8A7BFECD514"
    ]

    context = create_contex_standalone()
    data = np.zeros(4 * 9, dtype=np.float32)
    c_buffer = context.buffer(data)
    c_buffer.bind_to_storage_buffer(0)
    shader_path = r'D:\Develop\ModernGLTool\Shader\ShGen.glsl'

    cs = create_compute_shader(context, shader_path)
    cs.run(1)
    c_buffer.read_into(data)
    ##TODO:DELETE
    print(data)

    final_list = []
    for i in range(3):
        for j in range(9):
            value = data[i + j * 4]
            # if j == 0:
            #     value = data[i+j*4] + data[i+6*4]*-0.315392
            # elif j == 6:
            #     value = data[i+j*4] * 0.315392 * 3.0
            # else:
            #     value = data[i+j*4]
            final_list.append(round(value, 5))

    r_str = "("
    r_str += ",".join(str(v) for v in final_list)
    r_str += ")"

    ##TODO:DELETE
    print(r_str)

    pyperclip.copy(r_str)


def encode_rgbm(img_path):
    context = create_contex_standalone()
    shader_path = r'D:\Develop\ModernGLTool\Shader\RGBMEncode.glsl'
    cs = create_compute_shader(context, shader_path)
    src_texture = create_texture_with_img(context, img_path)
    dst_texture = create_texture_with_color(context, width=src_texture.width, height=src_texture.height)
    src_texture.bind_to_image(0)
    dst_texture.bind_to_image(1)
    cs.run(int(src_texture.width / 16), int(src_texture.height / 16), 1)
    img = texture_to_img(dst_texture)
    save_path = r"D:\User\Downloads\Matcap\Test.tga"
    save_img(save_path, img)
    img = Image.open(r"D:\User\Downloads\Matcap\Test.tga")
    img = img.resize((256, 256))
    img.save(r"D:\User\Downloads\Matcap\Test.tga")


def linear_to_srgb(img_path):
    context = create_contex_standalone()
    shader_path = r'F:\DevF\Other\ModernGLTool\Shader\LinearToSRGB.glsl'
    cs = create_compute_shader(context, shader_path)
    src_texture = create_texture_with_img(context, img_path)
    dst_texture = create_texture_with_color(context, width=src_texture.width, height=src_texture.height)
    src_texture.bind_to_image(0)
    dst_texture.bind_to_image(1)
    cs.run(int(src_texture.width / 16), int(src_texture.height / 16), 1)
    img = texture_to_img(dst_texture)
    save_path = os.path.dirname(img_path) + "\\PTex.tga"
    save_img(save_path, img)
    # img = Image.open(r"D:\User\Downloads\Matcap\Test.tga")
    # img = img.resize((256, 256))
    # img.save(r"D:\User\Downloads\Matcap\Test.tga")





if __name__ == '__main__':
    ##create_skin_lut(r"D:\User\Downloads\SkinLut\SkinLut.tga")
    linear_to_srgb(r"D:\User\Downloads\Atest\face\ParamTex.tga")
   ## func.renderdoc_grid_to_panorama(r"D:\User\Downloads\Weapon\Env.exr", r"D:\User\Downloads\Weapon\Env_p.hdr")
