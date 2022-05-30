import os
import moderngl as mgl
import numpy

from Utils.graphic_utils import *


def main():
    shader_path = './Shader/Test.glsl'

    context = create_contex_standalone()
    # cs = create_compute_shader(context, shader_path)
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

    tex = create_texture_with_color(context, 64, 64, (1, 1, 0, 1))
    tex = create_texture_with_img(context, './TestImage/Test.hdr')
    img = texture_to_img(tex)
    save_img('./OutPut/DD.jpg', img)

    # aaa = numpy.frombuffer(tex.read(), dtype='float32')
    # ##TODO:DELETE
    # print(aaa)


if __name__ == '__main__':
    main()
