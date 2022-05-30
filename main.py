import os
import moderngl as mgl
import numpy

from Utils.graphic_utils import *


def main():
    shader_path = './Shader/Test.glsl'

    context = create_contex_standalone()
    cs = create_compute_shader(context, shader_path)
    texSource = create_texture_with_img(context, "./TestImage/Test.png")
    texDist = create_texture_with_color(context, width=512, height=128)
    texDist.bind_to_image(0, read=True, write=True)
    texDist.filter = mgl.NEAREST, mgl.NEAREST

    cs.run(int(texDist.size[0] / 16) + 1, int(texDist.size[1] / 16) + 1, 1)
    save_img("./OutPut/DD.png", texture_to_img(texDist))
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
