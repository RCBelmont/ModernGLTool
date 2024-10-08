import math

from Utils.graphic_utils import *


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


if __name__ == '__main__':
    main()
